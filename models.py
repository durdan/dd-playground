from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum

class OperationType(Enum):
    CHAT = "chat"
    COMPLETION = "completion"
    EMBEDDING = "embedding"
    FUNCTION_CALL = "function_call"

class BudgetStatus(Enum):
    ACTIVE = "active"
    WARNING = "warning"
    EXCEEDED = "exceeded"
    SUSPENDED = "suspended"

@dataclass
class AgentUsage:
    agent_id: str
    agent_name: str
    operation_type: OperationType
    model: str
    input_tokens: int
    output_tokens: int
    cost: float
    timestamp: datetime
    crew_operation_id: Optional[str] = None
    metadata: Dict = field(default_factory=dict)

@dataclass
class CrewOperation:
    operation_id: str
    crew_name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    total_cost: float = 0.0
    agent_usages: List[AgentUsage] = field(default_factory=list)
    status: str = "running"

@dataclass
class Budget:
    budget_id: str
    name: str
    limit: float
    spent: float = 0.0
    period_start: datetime = field(default_factory=datetime.now)
    period_end: Optional[datetime] = None
    status: BudgetStatus = BudgetStatus.ACTIVE
    alert_threshold: float = 0.8  # 80% threshold
    agents: List[str] = field(default_factory=list)  # Empty = all agents