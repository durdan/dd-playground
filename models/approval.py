from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

class ApprovalStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"

class OperationType(Enum):
    MERGE = "merge"
    DEPLOY = "deploy"

@dataclass
class ApprovalRequest:
    id: str
    operation_type: OperationType
    target: str  # branch name, environment, etc.
    requester: str
    description: str
    status: ApprovalStatus
    created_at: datetime
    reviewed_at: Optional[datetime] = None
    reviewer: Optional[str] = None
    review_comment: Optional[str] = None
    metadata: Optional[dict] = None

    def can_transition_to(self, new_status: ApprovalStatus) -> bool:
        """Check if status transition is valid"""
        valid_transitions = {
            ApprovalStatus.PENDING: [ApprovalStatus.APPROVED, ApprovalStatus.REJECTED],
            ApprovalStatus.APPROVED: [ApprovalStatus.COMPLETED],
            ApprovalStatus.REJECTED: [],
            ApprovalStatus.COMPLETED: []
        }
        return new_status in valid_transitions.get(self.status, [])