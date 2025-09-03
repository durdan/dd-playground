from models.user import User, UserValidator, UserValidationError
from services.password_service import PasswordService
from repositories.user_repository import UserRepository

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.password_service = PasswordService()
    
    def create_user(self, email: str, password: str) -> User:
        """Create a new user with validation and password hashing"""
        # Validate input
        UserValidator.validate_email(email)
        UserValidator.validate_password(password)
        
        # Hash password
        password_hash = self.password_service.hash_password(password)
        
        # Create user
        user = User(email=email, password_hash=password_hash)
        return self.user_repository.create(user)
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        user = self.user_repository.find_by_email(email)
        if user and self.password_service.verify_password(password, user.password_hash):
            return user
        return None
    
    def change_password(self, user_id: int, old_password: str, new_password: str) -> bool:
        """Change user's password after verifying old password"""
        user = self.user_repository.find_by_id(user_id)
        if not user:
            return False
        
        # Verify old password
        if not self.password_service.verify_password(old_password, user.password_hash):
            return False
        
        # Validate new password
        UserValidator.validate_password(new_password)
        
        # Hash and update new password
        new_password_hash = self.password_service.hash_password(new_password)
        return self.user_repository.update_password(user_id, new_password_hash)