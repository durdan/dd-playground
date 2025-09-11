import hashlib
import secrets
import uuid
from datetime import datetime
from typing import List, Optional
from models.user import User
from repositories.user_repository import UserRepository
from exceptions.user_exceptions import UserNotFoundError, InvalidCredentialsError

class UserService:
    def __init__(self, repository: UserRepository):
        self._repository = repository
    
    def create_user(self, username: str, email: str, password: str) -> User:
        self._validate_password_strength(password)
        
        user_id = str(uuid.uuid4())
        password_hash = self._hash_password(password)
        
        user = User(
            id=user_id,
            username=username.strip(),
            email=email.strip().lower(),
            password_hash=password_hash,
            created_at=datetime.utcnow()
        )
        
        return self._repository.save(user)
    
    def authenticate(self, username_or_email: str, password: str) -> User:
        user = (self._repository.find_by_username(username_or_email) or 
                self._repository.find_by_email(username_or_email))
        
        if not user or not user.is_active:
            raise InvalidCredentialsError("Invalid credentials")
        
        if not self._verify_password(password, user.password_hash):
            raise InvalidCredentialsError("Invalid credentials")
        
        return user
    
    def get_user(self, user_id: str) -> User:
        user = self._repository.find_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User with id {user_id} not found")
        return user
    
    def update_user(self, user_id: str, username: Optional[str] = None, 
                   email: Optional[str] = None) -> User:
        user = self.get_user(user_id)
        
        if username:
            user.username = username.strip()
        if email:
            user.email = email.strip().lower()
        
        # Re-validate after updates
        user._validate()
        
        return self._repository.save(user)
    
    def deactivate_user(self, user_id: str) -> User:
        user = self.get_user(user_id)
        user.is_active = False
        return self._repository.save(user)
    
    def list_users(self) -> List[User]:
        return self._repository.find_all()
    
    def _hash_password(self, password: str) -> str:
        salt = secrets.token_hex(16)
        password_hash = hashlib.pbkdf2_hmac('sha256', 
                                          password.encode('utf-8'), 
                                          salt.encode('utf-8'), 
                                          100000)
        return f"{salt}:{password_hash.hex()}"
    
    def _verify_password(self, password: str, stored_hash: str) -> bool:
        try:
            salt, hash_hex = stored_hash.split(':')
            password_hash = hashlib.pbkdf2_hmac('sha256',
                                              password.encode('utf-8'),
                                              salt.encode('utf-8'),
                                              100000)
            return password_hash.hex() == hash_hex
        except ValueError:
            return False
    
    def _validate_password_strength(self, password: str):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(c.isupper() for c in password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in password):
            raise ValueError("Password must contain at least one digit")