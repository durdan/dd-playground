from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import re

@dataclass
class User:
    email: str
    password_hash: str
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        self.validate()
    
    def validate(self):
        """Validate user data"""
        if not self.email or not isinstance(self.email, str):
            raise ValueError("Email is required and must be a string")
        
        if not self._is_valid_email(self.email):
            raise ValueError("Invalid email format")
        
        if not self.password_hash or not isinstance(self.password_hash, str):
            raise ValueError("Password hash is required and must be a string")
        
        if len(self.password_hash) < 8:
            raise ValueError("Password hash too short")
    
    def _is_valid_email(self, email: str) -> bool:
        """Basic email validation"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None