from datetime import datetime
from typing import Dict, List, Any
from models.user import User
from validators.user_validator import UserValidator
from repositories.user_repository import UserRepository

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    def create_user(self, data: Dict[str, Any]) -> User:
        """Create a new user with validation"""
        UserValidator.validate_create(data)
        
        user = User(
            id=0,  # Will be set by repository
            name=data['name'].strip(),
            email=data['email'].strip().lower(),
            created_at=datetime.now()
        )
        
        return self.repository.create(user)
    
    def get_user(self, user_id: int) -> User:
        """Get user by ID"""
        return self.repository.get_by_id(user_id)
    
    def get_all_users(self) -> List[User]:
        """Get all users"""
        return self.repository.get_all()
    
    def update_user(self, user_id: int, data: Dict[str, Any]) -> User:
        """Update user with validation"""
        UserValidator.validate_update(data)
        
        existing_user = self.repository.get_by_id(user_id)
        
        updated_user = User(
            id=existing_user.id,
            name=data.get('name', existing_user.name).strip(),
            email=data.get('email', existing_user.email).strip().lower(),
            created_at=existing_user.created_at
        )
        
        return self.repository.update(user_id, updated_user)
    
    def delete_user(self, user_id: int) -> None:
        """Delete user by ID"""
        self.repository.delete(user_id)