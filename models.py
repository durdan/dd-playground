from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, Any, List, Optional
import uuid

class ApprovalStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class HumanApprovalRequest:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    operation_type: str = ""
    description: str = ""
    risk_level: RiskLevel = RiskLevel.LOW
    context: Dict[str, Any] = field(default_factory=dict)
    requested_at: datetime = field(default_factory=datetime.now)
    expires_at: datetime = field(default_factory=lambda: datetime.now() + timedelta(hours=24))
    status: ApprovalStatus = ApprovalStatus.PENDING
    approved_by: Optional[str] = None
    rejection_reason: Optional[str] = None

@dataclass
class SafetyRule:
    name: str
    max_value: float
    metric_key: str
    description: str = ""

@dataclass
class OperationResult:
    success: bool
    operation_id: str
    message: str
    requires_approval: bool = False
    approval_request_id: Optional[str] = None
    safety_violations: List[str] = field(default_factory=list)