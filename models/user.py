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
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()

class UserValidationError(Exception):
    pass

class UserValidator:
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    @staticmethod
    def validate_email(email: str) -> None:
        if not email or not isinstance(email, str):
            raise UserValidationError("Email is required")
        
        if not UserValidator.EMAIL_PATTERN.match(email):
            raise UserValidationError("Invalid email format")
    
    @staticmethod
    def validate_password(password: str) -> None:
        if not password or not isinstance(password, str):
            raise UserValidationError("Password is required")
        
        if len(password) < 8:
            raise UserValidationError("Password must be at least 8 characters")
        
        if not any(c.isupper() for c in password):
            raise UserValidationError("Password must contain at least one uppercase letter")
        
        if not any(c.islower() for c in password):
            raise UserValidationError("Password must contain at least one lowercase letter")
        
        if not any(c.isdigit() for c in password):
            raise UserValidationError("Password must contain at least one digit")