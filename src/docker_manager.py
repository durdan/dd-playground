import docker
from typing import List, Dict, Any

class DockerManager:
    def __init__(self):
        self.client = docker.from_env()
    
    def get_running_containers(self) -> List[Dict[str, Any]]:
        """Get list of running containers"""
        containers = []
        for container in self.client.containers.list():
            containers.append({
                'id': container.id,
                'name': container.name,
                'image': container.image.tags[0] if container.image.tags else 'unknown',
                'status': container.status
            })
        return containers
    
    def get_images(self) -> List[Dict[str, Any]]:
        """Get list of Docker images"""
        images = []
        for image in self.client.images.list():
            images.append({
                'id': image.id,
                'tags': image.tags,
                'size': image.attrs.get('Size', 0)
            })
        return images
    
    def execute_command(self, container_id: str, command: str) -> str:
        """Execute command in container"""
        try:
            container = self.client.containers.get(container_id)
            result = container.exec_run(command)
            return result.output.decode('utf-8')
        except Exception as e:
            return f"Error executing command: {str(e)}"
    
    def inspect_container(self, container_id: str) -> Dict[str, Any]:
        """Get detailed container information"""
        try:
            container = self.client.containers.get(container_id)
            return container.attrs
        except docker.errors.NotFound:
            return {}