import docker
from typing import Dict, Optional, List
import logging

logger = logging.getLogger(__name__)

class DockerManager:
    def __init__(self):
        try:
            self.client = docker.from_env()
        except Exception as e:
            raise RuntimeError(f"Failed to connect to Docker: {e}")
    
    def run_security_tool(self, image: str, command: List[str], 
                         volumes: Dict[str, Dict] = None, 
                         environment: Dict[str, str] = None) -> tuple[str, str]:
        """Run a security tool in a Docker container"""
        try:
            container = self.client.containers.run(
                image=image,
                command=command,
                volumes=volumes or {},
                environment=environment or {},
                remove=True,
                detach=False,
                stdout=True,
                stderr=True
            )
            return container.decode('utf-8'), ""
        except docker.errors.ContainerError as e:
            logger.error(f"Container error: {e}")
            return "", str(e)
        except Exception as e:
            logger.error(f"Docker execution error: {e}")
            return "", str(e)
    
    def pull_image(self, image: str) -> bool:
        """Pull Docker image if not exists"""
        try:
            self.client.images.pull(image)
            return True
        except Exception as e:
            logger.error(f"Failed to pull image {image}: {e}")
            return False
    
    def cleanup_containers(self, label_filter: str = None):
        """Clean up stopped containers"""
        try:
            filters = {"status": "exited"}
            if label_filter:
                filters["label"] = label_filter
            
            containers = self.client.containers.list(all=True, filters=filters)
            for container in containers:
                container.remove()
        except Exception as e:
            logger.error(f"Cleanup error: {e}")