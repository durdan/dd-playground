"""Task definitions and management."""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class TaskStatus(Enum):
    """Task execution status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class TaskConfig:
    """Configuration for a task."""
    name: str
    description: str
    expected_output: str
    agent_role: Optional[str] = None
    dependencies: List[str] = None
    tools_required: List[str] = None
    context: Dict[str, Any] = None

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.tools_required is None:
            self.tools_required = []
        if self.context is None:
            self.context = {}


class Task:
    """Task execution and management."""
    
    def __init__(self, config: TaskConfig):
        self.config = config
        self.status = TaskStatus.PENDING
        self.result = None
        self.error = None
        self._validate_config()
    
    def _validate_config(self):
        """Validate task configuration."""
        if not self.config.name:
            raise ValueError("Task name is required")
        if not self.config.description:
            raise ValueError("Task description is required")
        if not self.config.expected_output:
            raise ValueError("Task expected output is required")
    
    def mark_in_progress(self):
        """Mark task as in progress."""
        self.status = TaskStatus.IN_PROGRESS
    
    def mark_completed(self, result: Any):
        """Mark task as completed with result."""
        self.status = TaskStatus.COMPLETED
        self.result = result
    
    def mark_failed(self, error: str):
        """Mark task as failed with error."""
        self.status = TaskStatus.FAILED
        self.error = error
    
    def is_ready(self, completed_tasks: List[str]) -> bool:
        """Check if task dependencies are satisfied."""
        return all(dep in completed_tasks for dep in self.config.dependencies)
    
    def __str__(self):
        return f"Task({self.config.name}, {self.status.value})"