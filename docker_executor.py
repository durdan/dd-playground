import subprocess
import json
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class DockerResult:
    exit_code: int
    stdout: str
    stderr: str
    success: bool

class DockerExecutor:
    def __init__(self, image: str, working_dir: str = "/workspace"):
        self.image = image
        self.working_dir = working_dir
    
    def run_command(self, command: List[str], volumes: Optional[Dict[str, str]] = None, 
                   env_vars: Optional[Dict[str, str]] = None) -> DockerResult:
        """Execute command in Docker container"""
        if not command:
            raise ValueError("Command cannot be empty")
        
        docker_cmd = [
            "docker", "run", "--rm",
            "-w", self.working_dir
        ]
        
        # Add volume mounts
        if volumes:
            for host_path, container_path in volumes.items():
                docker_cmd.extend(["-v", f"{host_path}:{container_path}"])
        
        # Add environment variables
        if env_vars:
            for key, value in env_vars.items():
                docker_cmd.extend(["-e", f"{key}={value}"])
        
        docker_cmd.append(self.image)
        docker_cmd.extend(command)
        
        try:
            result = subprocess.run(
                docker_cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            return DockerResult(
                exit_code=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr,
                success=result.returncode == 0
            )
        except subprocess.TimeoutExpired:
            raise RuntimeError("Docker command timed out after 5 minutes")
        except Exception as e:
            raise RuntimeError(f"Failed to execute Docker command: {e}")