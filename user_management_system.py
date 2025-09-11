from user_service import UserService
from repository import InMemoryUserRepository
from user import User
from typing import List

class UserManagementSystem:
    """Main facade for user management operations."""
    
    def __init__(self, repository=None):
        """Initialize with optional custom repository."""
        if repository is None:
            repository = InMemoryUserRepository()
        self._service = UserService(repository)
    
    def create_user(self, email: str, name: str) -> User:
        """Create a new user."""
        return self._service.create_user(email, name)
    
    def get_user(self, user_id: int) -> User:
        """Get user by ID."""
        return self._service.get_user_by_id(user_id)
    
    def find_user_by_email(self, email: str) -> User:
        """Find user by email."""
        return self._service.get_user_by_email(email)
    
    def list_all_users(self) -> List[User]:
        """Get all users."""
        return self._service.get_all_users()
    
    def update_user(self, user_id: int, email: str = None, name: str = None) -> User:
        """Update user information."""
        return self._service.update_user(user_id, email, name)
    
    def delete_user(self, user_id: int) -> bool:
        """Delete user."""
        return self._service.delete_user(user_id)