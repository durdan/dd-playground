from dataclasses import dataclass
from typing import Optional
import re
from datetime import datetime

@dataclass
class User:
    """User model with validation."""
    id: Optional[int]
    email: str
    name: str
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validate user data after initialization."""
        self._validate_email()
        self._validate_name()
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def _validate_email(self):
        """Validate email format."""
        if not self.email or not isinstance(self.email, str):
            raise ValueError("Email is required and must be a string")
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, self.email.strip()):
            raise ValueError("Invalid email format")
        
        self.email = self.email.strip().lower()
    
    def _validate_name(self):
        """Validate name."""
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Name is required and must be a string")
        
        self.name = self.name.strip()
        if len(self.name) < 2:
            raise ValueError("Name must be at least 2 characters long")
        if len(self.name) > 100:
            raise ValueError("Name must be less than 100 characters")