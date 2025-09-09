from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from enum import Enum

class UserStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

@dataclass
class User:
    id: Optional[int]
    email: str
    password_hash: str
    first_name: str
    last_name: str
    status: UserStatus
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    
    def __post_init__(self):
        if not self.email or '@' not in self.email:
            raise ValueError("Valid email is required")
        if not self.first_name or not self.last_name:
            raise ValueError("First name and last name are required")