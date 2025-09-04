from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime


class WorkflowStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AgentConfig(BaseModel):
    """Configuration for a CrewAI agent."""
    role: str
    goal: str
    backstory: str
    tools: List[str] = Field(default_factory=list)
    verbose: bool = True


class TaskConfig(BaseModel):
    """Configuration for a CrewAI task."""
    description: str
    agent: str
    expected_output: str
    tools: List[str] = Field(default_factory=list)


class WorkflowRequest(BaseModel):
    """Request to execute a CrewAI workflow."""
    workflow_id: str
    agents: List[AgentConfig]
    tasks: List[TaskConfig]
    max_iterations: Optional[int] = None
    timeout: Optional[int] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class WorkflowResult(BaseModel):
    """Result of a CrewAI workflow execution."""
    workflow_id: str
    status: WorkflowStatus
    started_at: datetime
    completed_at: Optional[datetime] = None
    results: Dict[str, Any] = Field(default_factory=dict)
    error_message: Optional[str] = None
    execution_time: Optional[float] = None