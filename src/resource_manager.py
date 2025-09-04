import time
import threading
from typing import Dict, List
from dataclasses import dataclass, field
from datetime import datetime, timedelta

@dataclass
class ResourceLimits:
    max_containers: int = 5
    max_memory_per_container: str = "512m"
    max_cpu_per_container: float = 1.0
    max_execution_time: int = 300  # seconds
    cleanup_interval: int = 60  # seconds

@dataclass
class ContainerInfo:
    container_id: str
    created_at: datetime
    resource_usage: Dict[str, Any] = field(default_factory=dict)

class ResourceManager:
    def __init__(self, limits: ResourceLimits):
        self.limits = limits
        self.active_containers: Dict[str, ContainerInfo] = {}
        self.lock = threading.Lock()
        self._start_cleanup_thread()
    
    def can_create_container(self) -> bool:
        """Check if new container can be created within limits."""
        with self.lock:
            return len(self.active_containers) < self.limits.max_containers
    
    def register_container(self, container_id: str):
        """Register new container for tracking."""
        with self.lock:
            self.active_containers[container_id] = ContainerInfo(
                container_id=container_id,
                created_at=datetime.now()
            )
    
    def unregister_container(self, container_id: str):
        """Remove container from tracking."""
        with self.lock:
            self.active_containers.pop(container_id, None)
    
    def get_expired_containers(self) -> List[str]:
        """Get containers that exceeded execution time limit."""
        cutoff_time = datetime.now() - timedelta(seconds=self.limits.max_execution_time)
        
        with self.lock:
            return [
                info.container_id 
                for info in self.active_containers.values()
                if info.created_at < cutoff_time
            ]
    
    def _start_cleanup_thread(self):
        """Start background cleanup thread."""
        def cleanup_loop():
            while True:
                try:
                    expired = self.get_expired_containers()
                    for container_id in expired:
                        self._force_cleanup_container(container_id)
                    time.sleep(self.limits.cleanup_interval)
                except Exception as e:
                    print(f"Cleanup thread error: {e}")
        
        thread = threading.Thread(target=cleanup_loop, daemon=True)
        thread.start()
    
    def _force_cleanup_container(self, container_id: str):
        """Force cleanup of expired container."""
        try:
            import docker
            client = docker.from_env()
            container = client.containers.get(container_id)
            container.kill()
            container.remove()
            self.unregister_container(container_id)
            print(f"Force cleaned up expired container: {container_id}")
        except Exception as e:
            print(f"Failed to cleanup container {container_id}: {e}")