from dataclasses import dataclass
from typing import List, Dict, Any, Optional

@dataclass
class PlanTask:
    """Represents a single task in a plan."""
    description: str
    expected_output: Optional[str] = None
    dependencies: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class Plan:
    """Represents a complete execution plan."""
    name: str
    description: str
    tasks: List[PlanTask]
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class AgentConfig:
    """Configuration for a CrewAI agent."""
    role: str
    goal: str
    backstory: str = ""
    tools: List[str] = None
    verbose: bool = False
    
    def __post_init__(self):
        if self.tools is None:
            self.tools = []

@dataclass
class CrewConfig:
    """Configuration for CrewAI orchestration."""
    agents: List[AgentConfig]
    verbose: bool = False