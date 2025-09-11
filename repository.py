from abc import ABC, abstractmethod
from typing import List, Optional
from user import User

class UserRepository(ABC):
    """Abstract repository interface for user data access."""
    
    @abstractmethod
    def create(self, user: User) -> User:
        """Create a new user."""
        pass
    
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        pass
    
    @abstractmethod
    def get_all(self) -> List[User]:
        """Get all users."""
        pass
    
    @abstractmethod
    def update(self, user: User) -> User:
        """Update existing user."""
        pass
    
    @abstractmethod
    def delete(self, user_id: int) -> bool:
        """Delete user by ID."""
        pass

class InMemoryUserRepository(UserRepository):
    """In-memory implementation of user repository."""
    
    def __init__(self):
        self._users = {}
        self._next_id = 1
    
    def create(self, user: User) -> User:
        """Create a new user with auto-generated ID."""
        user.id = self._next_id
        self._users[user.id] = user
        self._next_id += 1
        return user
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return self._users.get(user_id)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        email = email.lower().strip()
        for user in self._users.values():
            if user.email == email:
                return user
        return None
    
    def get_all(self) -> List[User]:
        """Get all users."""
        return list(self._users.values())
    
    def update(self, user: User) -> User:
        """Update existing user."""
        if user.id not in self._users:
            return None
        self._users[user.id] = user
        return user
    
    def delete(self, user_id: int) -> bool:
        """Delete user by ID."""
        if user_id in self._users:
            del self._users[user_id]
            return True
        return False