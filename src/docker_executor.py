import docker
import json
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from pathlib import Path

@dataclass
class ContainerConfig:
    image: str
    command: List[str]
    environment: Dict[str, str]
    volumes: Dict[str, Dict[str, str]]
    mem_limit: str = "512m"
    cpu_limit: float = 1.0
    network_mode: str = "none"
    read_only: bool = True

class DockerExecutor:
    def __init__(self):
        self.client = docker.from_env()
        self.logger = logging.getLogger(__name__)
        
    def create_container(self, config: ContainerConfig, name: str) -> docker.models.containers.Container:
        """Create isolated container with security constraints."""
        try:
            container = self.client.containers.create(
                image=config.image,
                command=config.command,
                environment=config.environment,
                volumes=config.volumes,
                mem_limit=config.mem_limit,
                nano_cpus=int(config.cpu_limit * 1e9),
                network_mode=config.network_mode,
                read_only=config.read_only,
                name=name,
                detach=True,
                remove=False,  # Manual cleanup for better control
                security_opt=["no-new-privileges:true"],
                cap_drop=["ALL"],
                user="1000:1000"
            )
            self.logger.info(f"Created container {name}")
            return container
        except docker.errors.APIError as e:
            self.logger.error(f"Failed to create container {name}: {e}")
            raise
    
    def execute_task(self, container: docker.models.containers.Container, 
                    task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute task in isolated container."""
        try:
            # Write task data to container
            task_json = json.dumps(task_data)
            container.put_archive("/tmp", self._create_tar_data("task.json", task_json))
            
            # Start container
            container.start()
            
            # Wait for completion with timeout
            result = container.wait(timeout=300)  # 5 minute timeout
            
            # Get output
            logs = container.logs().decode('utf-8')
            
            # Get result file if exists
            output_data = {}
            try:
                archive, _ = container.get_archive("/tmp/result.json")
                result_json = self._extract_from_tar(archive, "result.json")
                output_data = json.loads(result_json)
            except docker.errors.NotFound:
                output_data = {"logs": logs}
            
            return {
                "exit_code": result["StatusCode"],
                "output": output_data,
                "logs": logs
            }
            
        except Exception as e:
            self.logger.error(f"Task execution failed: {e}")
            return {
                "exit_code": -1,
                "output": {},
                "logs": f"Execution error: {str(e)}"
            }
        finally:
            self._cleanup_container(container)
    
    def _create_tar_data(self, filename: str, content: str) -> bytes:
        """Create tar archive with file content."""
        import tarfile
        import io
        
        tar_buffer = io.BytesIO()
        with tarfile.open(fileobj=tar_buffer, mode='w') as tar:
            info = tarfile.TarInfo(name=filename)
            info.size = len(content.encode())
            tar.addfile(info, io.BytesIO(content.encode()))
        
        tar_buffer.seek(0)
        return tar_buffer.read()
    
    def _extract_from_tar(self, archive, filename: str) -> str:
        """Extract file content from tar archive."""
        import tarfile
        import io
        
        tar_buffer = io.BytesIO()
        for chunk in archive:
            tar_buffer.write(chunk)
        tar_buffer.seek(0)
        
        with tarfile.open(fileobj=tar_buffer, mode='r') as tar:
            member = tar.getmember(filename)
            return tar.extractfile(member).read().decode()
    
    def _cleanup_container(self, container: docker.models.containers.Container):
        """Clean up container resources."""
        try:
            container.stop(timeout=10)
            container.remove()
            self.logger.info(f"Cleaned up container {container.name}")
        except Exception as e:
            self.logger.warning(f"Cleanup failed for {container.name}: {e}")