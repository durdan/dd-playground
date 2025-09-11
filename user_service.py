from typing import List, Optional
from user import User
from repository import UserRepository
from exceptions import UserNotFoundError, UserAlreadyExistsError, ValidationError

class UserService:
    """Business logic layer for user management."""
    
    def __init__(self, repository: UserRepository):
        self._repository = repository
    
    def create_user(self, email: str, name: str) -> User:
        """Create a new user with validation."""
        try:
            # Create user object (validation happens in __post_init__)
            user = User(id=None, email=email, name=name)
        except ValueError as e:
            raise ValidationError(str(e))
        
        # Check if user already exists
        existing_user = self._repository.get_by_email(user.email)
        if existing_user:
            raise UserAlreadyExistsError(f"User with email {user.email} already exists")
        
        return self._repository.create(user)
    
    def get_user_by_id(self, user_id: int) -> User:
        """Get user by ID."""
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValidationError("User ID must be a positive integer")
        
        user = self._repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User with ID {user_id} not found")
        
        return user
    
    def get_user_by_email(self, email: str) -> User:
        """Get user by email."""
        if not email or not isinstance(email, str):
            raise ValidationError("Email is required and must be a string")
        
        user = self._repository.get_by_email(email)
        if not user:
            raise UserNotFoundError(f"User with email {email} not found")
        
        return user
    
    def get_all_users(self) -> List[User]:
        """Get all users."""
        return self._repository.get_all()
    
    def update_user(self, user_id: int, email: str = None, name: str = None) -> User:
        """Update user with validation."""
        # Get existing user
        existing_user = self.get_user_by_id(user_id)
        
        # Prepare updated data
        updated_email = email if email is not None else existing_user.email
        updated_name = name if name is not None else existing_user.name
        
        # Check email uniqueness if email is being changed
        if email and email != existing_user.email:
            if self._repository.get_by_email(email):
                raise UserAlreadyExistsError(f"User with email {email} already exists")
        
        try:
            # Create updated user object (validation happens in __post_init__)
            updated_user = User(
                id=user_id,
                email=updated_email,
                name=updated_name,
                created_at=existing_user.created_at
            )
        except ValueError as e:
            raise ValidationError(str(e))
        
        return self._repository.update(updated_user)
    
    def delete_user(self, user_id: int) -> bool:
        """Delete user by ID."""
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValidationError("User ID must be a positive integer")
        
        # Check if user exists
        if not self._repository.get_by_id(user_id):
            raise UserNotFoundError(f"User with ID {user_id} not found")
        
        return self._repository.delete(user_id)