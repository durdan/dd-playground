from typing import Dict, List, Optional
from models.user import User
from exceptions import UserNotFoundError, UserAlreadyExistsError

class UserRepository:
    def __init__(self):
        self._users: Dict[int, User] = {}
        self._email_index: Dict[str, int] = {}
        self._next_id = 1
    
    def create(self, user: User) -> User:
        """Create a new user"""
        if user.email in self._email_index:
            raise UserAlreadyExistsError(f"User with email {user.email} already exists")
        
        user.id = self._next_id
        self._users[user.id] = user
        self._email_index[user.email] = user.id
        self._next_id += 1
        return user
    
    def get_by_id(self, user_id: int) -> User:
        """Get user by ID"""
        if user_id not in self._users:
            raise UserNotFoundError(f"User with id {user_id} not found")
        return self._users[user_id]
    
    def get_all(self) -> List[User]:
        """Get all users"""
        return list(self._users.values())
    
    def update(self, user_id: int, user: User) -> User:
        """Update existing user"""
        if user_id not in self._users:
            raise UserNotFoundError(f"User with id {user_id} not found")
        
        old_user = self._users[user_id]
        
        # Update email index if email changed
        if old_user.email != user.email:
            if user.email in self._email_index:
                raise UserAlreadyExistsError(f"User with email {user.email} already exists")
            del self._email_index[old_user.email]
            self._email_index[user.email] = user_id
        
        user.id = user_id
        self._users[user_id] = user
        return user
    
    def delete(self, user_id: int) -> None:
        """Delete user by ID"""
        if user_id not in self._users:
            raise UserNotFoundError(f"User with id {user_id} not found")
        
        user = self._users[user_id]
        del self._email_index[user.email]
        del self._users[user_id]