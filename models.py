from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

class ValidationStatus(str, Enum):
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"

class TaskType(str, Enum):
    FEATURE = "feature"
    BUGFIX = "bugfix"
    REFACTOR = "refactor"
    SECURITY = "security"

class Task(BaseModel):
    id: str
    title: str
    description: str
    task_type: TaskType
    requirements: List[str] = Field(default_factory=list)
    proposed_solution: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ValidationResult(BaseModel):
    agent_name: str
    status: ValidationStatus
    message: str
    details: Dict[str, Any] = Field(default_factory=dict)
    suggestions: List[str] = Field(default_factory=list)

class VerificationReport(BaseModel):
    task_id: str
    overall_status: ValidationStatus
    results: List[ValidationResult]
    final_recommendations: List[str] = Field(default_factory=list)