from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Optional
from datetime import datetime

class Role(Enum):
    TECH_LEAD = "tech_lead"
    MAINTAINER = "maintainer"
    REVIEWER = "reviewer"
    STAKEHOLDER = "stakeholder"

class Priority(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class TeamMember:
    name: str
    email: str
    roles: List[Role]
    backup: Optional[str] = None

@dataclass
class Decision:
    id: str
    title: str
    description: str
    priority: Priority
    proposed_by: str
    approved_by: List[str]
    status: str
    created_at: datetime
    decision_date: Optional[datetime] = None

class GovernanceManager:
    def __init__(self):
        self.team_members: Dict[str, TeamMember] = {}
        self.decisions: Dict[str, Decision] = {}
        self.approval_matrix = {
            Priority.CRITICAL: [Role.TECH_LEAD],
            Priority.HIGH: [Role.TECH_LEAD, Role.MAINTAINER],
            Priority.MEDIUM: [Role.MAINTAINER],
            Priority.LOW: [Role.MAINTAINER, Role.REVIEWER]
        }
    
    def add_team_member(self, member: TeamMember) -> None:
        if not member.name or not member.email:
            raise ValueError("Name and email are required")
        self.team_members[member.name] = member
    
    def propose_decision(self, decision: Decision) -> str:
        if not decision.title or not decision.proposed_by:
            raise ValueError("Title and proposer are required")
        
        decision.status = "pending"
        decision.created_at = datetime.now()
        self.decisions[decision.id] = decision
        return decision.id
    
    def approve_decision(self, decision_id: str, approver: str) -> bool:
        if decision_id not in self.decisions:
            raise ValueError(f"Decision {decision_id} not found")
        
        decision = self.decisions[decision_id]
        required_roles = self.approval_matrix.get(decision.priority, [])
        
        approver_member = self.team_members.get(approver)
        if not approver_member:
            raise ValueError(f"Approver {approver} not found")
        
        has_required_role = any(role in approver_member.roles for role in required_roles)
        if not has_required_role:
            raise ValueError(f"Approver lacks required role for {decision.priority.value} priority")
        
        if approver not in decision.approved_by:
            decision.approved_by.append(approver)
        
        # Check if we have enough approvals
        if len(decision.approved_by) >= len(required_roles):
            decision.status = "approved"
            decision.decision_date = datetime.now()
            return True
        
        return False
    
    def get_pending_decisions(self) -> List[Decision]:
        return [d for d in self.decisions.values() if d.status == "pending"]