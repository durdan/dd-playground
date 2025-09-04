from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Dict, Optional, Set

class RolloutStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress" 
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"

class RepositoryTier(Enum):
    PILOT = "pilot"
    CANARY = "canary"
    PRODUCTION = "production"

@dataclass
class Repository:
    name: str
    tier: RepositoryTier
    metadata: Dict[str, str] = field(default_factory=dict)
    last_deployment: Optional[datetime] = None
    health_score: float = 1.0  # 0.0 to 1.0
    
    def is_healthy(self, min_score: float = 0.8) -> bool:
        return self.health_score >= min_score

@dataclass
class Phase:
    name: str
    target_percentage: float
    min_success_rate: float
    wait_time_hours: int
    required_tiers: Set[RepositoryTier] = field(default_factory=set)
    max_failures: int = 0
    
    def __post_init__(self):
        if not 0 <= self.target_percentage <= 100:
            raise ValueError("target_percentage must be between 0 and 100")
        if not 0 <= self.min_success_rate <= 1:
            raise ValueError("min_success_rate must be between 0 and 1")

@dataclass
class RolloutState:
    rollout_id: str
    current_phase: int
    status: RolloutStatus
    deployed_repos: Set[str] = field(default_factory=set)
    failed_repos: Set[str] = field(default_factory=set)
    phase_start_time: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)