"""Agent base class and implementations."""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class AgentConfig:
    """Configuration for an agent."""
    name: str
    role: str
    goal: str
    backstory: str
    tools: List[str] = None
    llm_config: Dict[str, Any] = None
    max_iterations: int = 10
    verbose: bool = False

    def __post_init__(self):
        if self.tools is None:
            self.tools = []
        if self.llm_config is None:
            self.llm_config = {}


class Agent(ABC):
    """Base agent class."""
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.tools = []
        self._validate_config()
    
    def _validate_config(self):
        """Validate agent configuration."""
        if not self.config.name:
            raise ValueError("Agent name is required")
        if not self.config.role:
            raise ValueError("Agent role is required")
        if not self.config.goal:
            raise ValueError("Agent goal is required")
    
    @abstractmethod
    def execute_task(self, task: 'Task') -> Dict[str, Any]:
        """Execute a task and return results."""
        pass
    
    def add_tool(self, tool: 'Tool'):
        """Add a tool to the agent."""
        self.tools.append(tool)
    
    def __str__(self):
        return f"Agent({self.config.name}, {self.config.role})"