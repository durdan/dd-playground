from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum
import re
from datetime import datetime
from exceptions import ValidationError

class Role(Enum):
    ADMIN = "admin"
    MEMBER = "member"
    VIEWER = "viewer"

@dataclass
class User:
    id: str
    email: str
    name: str
    role: Role = Role.MEMBER
    organization_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True

    def __post_init__(self):
        self._validate()

    def _validate(self):
        if not self.id or not self.id.strip():
            raise ValidationError("User ID cannot be empty")
        
        if not self.email or not self._is_valid_email(self.email):
            raise ValidationError("Invalid email format")
        
        if not self.name or not self.name.strip():
            raise ValidationError("User name cannot be empty")
        
        if not isinstance(self.role, Role):
            raise ValidationError("Invalid role")

    def _is_valid_email(self, email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def has_permission(self, required_role: Role) -> bool:
        role_hierarchy = {Role.VIEWER: 1, Role.MEMBER: 2, Role.ADMIN: 3}
        return role_hierarchy[self.role] >= role_hierarchy[required_role]

@dataclass
class Organization:
    id: str
    name: str
    description: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True

    def __post_init__(self):
        self._validate()

    def _validate(self):
        if not self.id or not self.id.strip():
            raise ValidationError("Organization ID cannot be empty")
        
        if not self.name or not self.name.strip():
            raise ValidationError("Organization name cannot be empty")