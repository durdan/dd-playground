from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import re

@dataclass
class User:
    id: int
    name: str
    email: str
    created_at: datetime
    
    def __post_init__(self):
        if not self.name or not self.name.strip():
            raise ValueError("Name cannot be empty")
        if not self._is_valid_email(self.email):
            raise ValueError("Invalid email format")
    
    def _is_valid_email(self, email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

@dataclass
class Organization:
    id: int
    name: str
    description: str
    created_at: datetime
    
    def __post_init__(self):
        if not self.name or not self.name.strip():
            raise ValueError("Organization name cannot be empty")

@dataclass
class UserOrganization:
    user_id: int
    organization_id: int
    joined_at: datetime