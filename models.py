from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional
from datetime import datetime

class MilestoneStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress" 
    COMPLETED = "completed"
    FAILED = "failed"

class QualityGateType(Enum):
    CODE_REVIEW = "code_review"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    SECURITY = "security"
    PERFORMANCE = "performance"

@dataclass
class QualityGate:
    name: str
    gate_type: QualityGateType
    required: bool = True
    crew_agent: str = ""
    criteria: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.name.strip():
            raise ValueError("Quality gate name cannot be empty")

@dataclass
class ValidationResult:
    gate_name: str
    passed: bool
    score: float
    feedback: str
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class Milestone:
    id: str
    name: str
    description: str
    quality_gates: List[QualityGate]
    status: MilestoneStatus = MilestoneStatus.PENDING
    validation_results: List[ValidationResult] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    
    def __post_init__(self):
        if not self.id.strip() or not self.name.strip():
            raise ValueError("Milestone ID and name are required")
        if not self.quality_gates:
            raise ValueError("At least one quality gate is required")

@dataclass
class PRContext:
    branch: str
    files_changed: List[str]
    diff: str
    description: str
    metadata: Dict[str, Any] = field(default_factory=dict)