from typing import Dict, Any, Optional
from dataclasses import dataclass
from .exceptions import TaskError

@dataclass
class Task:
    """Represents a task to be executed by agents"""
    id: str
    description: str
    input_data: Dict[str, Any]
    required_role: Optional[str] = None
    sop: Optional[str] = None
    priority: int = 1
    
    def __post_init__(self):
        if not self.id.strip():
            raise TaskError("Task ID cannot be empty")
        if not self.description.strip():
            raise TaskError("Task description cannot be empty")
        if self.priority < 1:
            raise TaskError("Task priority must be >= 1")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary for agent execution"""
        return {
            'id': self.id,
            'description': self.description,
            'input': self.input_data,
            'sop': self.sop,
            'priority': self.priority
        }