"""Tool base class and implementations."""

from typing import Dict, Any, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class ToolConfig:
    """Configuration for a tool."""
    name: str
    description: str
    parameters: Dict[str, Any] = None
    required_permissions: list = None

    def __post_init__(self):
        if self.parameters is None:
            self.parameters = {}
        if self.required_permissions is None:
            self.required_permissions = []


class Tool(ABC):
    """Base tool class."""
    
    def __init__(self, config: ToolConfig):
        self.config = config
        self._validate_config()
    
    def _validate_config(self):
        """Validate tool configuration."""
        if not self.config.name:
            raise ValueError("Tool name is required")
        if not self.config.description:
            raise ValueError("Tool description is required")
    
    @abstractmethod
    def execute(self, **kwargs) -> Any:
        """Execute the tool with given parameters."""
        pass
    
    def validate_parameters(self, **kwargs) -> bool:
        """Validate input parameters."""
        # Basic validation - can be overridden
        return True
    
    def __str__(self):
        return f"Tool({self.config.name})"