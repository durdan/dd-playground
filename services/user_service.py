import hashlib
from typing import List, Optional
from models.user import User
from repositories.user_repository import UserRepository

class UserService:
    def __init__(self, repository: UserRepository):
        self._repository = repository
    
    def create_user(self, username: str, email: str, password: str) -> User:
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        
        password_hash = self._hash_password(password)
        user = User(id=None, username=username, email=email, password_hash=password_hash)
        
        return self._repository.save(user)
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        if user_id <= 0:
            raise ValueError("User ID must be positive")
        return self._repository.find_by_id(user_id)
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        if not username or not username.strip():
            raise ValueError("Username cannot be empty")
        return self._repository.find_by_username(username.strip())
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = self.get_user_by_username(username)
        if not user or not user.is_active:
            return None
        
        password_hash = self._hash_password(password)
        return user if user.password_hash == password_hash else None
    
    def update_user(self, user_id: int, username: str = None, email: str = None) -> Optional[User]:
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        
        # Create updated user for validation
        updated_user = User(
            id=user.id,
            username=username if username is not None else user.username,
            email=email if email is not None else user.email,
            password_hash=user.password_hash,
            created_at=user.created_at,
            is_active=user.is_active
        )
        
        return self._repository.save(updated_user)
    
    def deactivate_user(self, user_id: int) -> bool:
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        user.is_active = False
        self._repository.save(user)
        return True
    
    def delete_user(self, user_id: int) -> bool:
        return self._repository.delete(user_id)
    
    def list_users(self, active_only: bool = False) -> List[User]:
        users = self._repository.find_all()
        return [u for u in users if not active_only or u.is_active]
    
    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()