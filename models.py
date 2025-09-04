from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class AgentRole(str, Enum):
    TASK_VERIFIER = "task_verifier"
    CODE_REVIEWER = "code_reviewer"
    TEST_GENERATOR = "test_generator"

class TaskRequest(BaseModel):
    id: str
    description: str
    code: Optional[str] = None
    requirements: List[str] = []
    context: Dict[str, Any] = {}

class AgentResponse(BaseModel):
    agent_role: AgentRole
    status: TaskStatus
    result: Dict[str, Any]
    feedback: List[str] = []
    suggestions: List[str] = []
    errors: List[str] = []

class WorkflowResult(BaseModel):
    task_id: str
    status: TaskStatus
    verification_result: Optional[AgentResponse] = None
    review_result: Optional[AgentResponse] = None
    test_result: Optional[AgentResponse] = None
    final_output: Dict[str, Any] = {}