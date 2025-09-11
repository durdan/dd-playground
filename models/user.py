from dataclasses import dataclass
from typing import Optional
import re
from datetime import datetime

@dataclass
class User:
    id: str
    username: str
    email: str
    password_hash: str
    created_at: datetime
    is_active: bool = True
    
    def __post_init__(self):
        self._validate()
    
    def _validate(self):
        if not self.username or len(self.username.strip()) < 3:
            raise ValueError("Username must be at least 3 characters")
        
        if not self._is_valid_email(self.email):
            raise ValueError("Invalid email format")
        
        if not self.password_hash:
            raise ValueError("Password hash cannot be empty")
    
    def _is_valid_email(self, email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))