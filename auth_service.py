import hashlib
from typing import Optional
from models import User
from jwt_auth import JWTAuth

class AuthService:
    def __init__(self):
        self.jwt_auth = JWTAuth()
        # Demo users - in production, use proper database
        self.users = {
            'admin': User(1, 'admin', self._hash_password('admin123'), 'admin'),
            'user': User(2, 'user', self._hash_password('user123'), 'user')
        }
    
    def _hash_password(self, password: str) -> str:
        """Simple password hashing - use bcrypt in production"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate(self, username: str, password: str) -> Optional[str]:
        """Authenticate user and return JWT token"""
        if not username or not password:
            raise ValueError("Username and password are required")
        
        user = self.users.get(username)
        if not user or user.password_hash != self._hash_password(password):
            return None
        
        return self.jwt_auth.generate_token(user.id, user.username, user.role)
    
    def get_user(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.users.get(username)