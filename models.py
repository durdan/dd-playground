from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

class FeatureStatus(Enum):
    INTAKE = "intake"
    IN_DEVELOPMENT = "in_development"
    IN_TESTING = "in_testing"
    READY_FOR_RELEASE = "ready_for_release"
    RELEASED = "released"

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class Feature:
    id: str
    title: str
    description: str
    priority: Priority
    status: FeatureStatus
    created_at: datetime
    updated_at: datetime
    assignee: Optional[str] = None
    estimated_hours: Optional[int] = None
    
    def update_status(self, new_status: FeatureStatus):
        self.status = new_status
        self.updated_at = datetime.now()

@dataclass
class Release:
    id: str
    version: str
    features: List[str]  # feature IDs
    created_at: datetime
    target_date: Optional[datetime] = None
    is_ready: bool = False