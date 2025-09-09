from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum

class Role(Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"
    VIEWER = "viewer"

@dataclass
class UserOrganization:
    id: Optional[int]
    user_id: int
    organization_id: int
    role: Role
    joined_at: Optional[datetime]
    
    def __post_init__(self):
        if not self.user_id or not self.organization_id:
            raise ValueError("User ID and Organization ID are required")