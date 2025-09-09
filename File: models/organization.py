from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum

class OrganizationStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

@dataclass
class Organization:
    id: Optional[int]
    name: str
    description: Optional[str]
    status: OrganizationStatus
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    
    def __post_init__(self):
        if not self.name or len(self.name.strip()) < 2:
            raise ValueError("Organization name must be at least 2 characters")