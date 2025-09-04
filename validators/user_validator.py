import re
from typing import Dict, Any
from exceptions import ValidationError

class UserValidator:
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    @classmethod
    def validate_create(cls, data: Dict[str, Any]) -> None:
        """Validate user creation data"""
        cls._validate_name(data.get('name'))
        cls._validate_email(data.get('email'))
    
    @classmethod
    def validate_update(cls, data: Dict[str, Any]) -> None:
        """Validate user update data"""
        if 'name' in data:
            cls._validate_name(data['name'])
        if 'email' in data:
            cls._validate_email(data['email'])
    
    @classmethod
    def _validate_name(cls, name: Any) -> None:
        if not name or not isinstance(name, str) or not name.strip():
            raise ValidationError("Name is required and must be a non-empty string")
        if len(name.strip()) > 100:
            raise ValidationError("Name must be 100 characters or less")
    
    @classmethod
    def _validate_email(cls, email: Any) -> None:
        if not email or not isinstance(email, str):
            raise ValidationError("Email is required and must be a string")
        if not cls.EMAIL_PATTERN.match(email):
            raise ValidationError("Invalid email format")