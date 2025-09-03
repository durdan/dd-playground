import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from config import Config

class JWTAuth:
    def __init__(self):
        self.secret_key = Config.JWT_SECRET_KEY
        self.algorithm = Config.JWT_ALGORITHM
        self.expiration_hours = Config.JWT_EXPIRATION_HOURS
    
    def generate_token(self, user_id: int, username: str, role: str) -> str:
        """Generate JWT token for authenticated user"""
        if not user_id or not username or not role:
            raise ValueError("User ID, username, and role are required")
        
        payload = {
            'user_id': user_id,
            'username': username,
            'role': role,
            'exp': datetime.utcnow() + timedelta(hours=self.expiration_hours),
            'iat': datetime.utcnow()
        }
        
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def decode_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Decode and validate JWT token"""
        if not token:
            return None
            
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def extract_token_from_header(self, auth_header: str) -> Optional[str]:
        """Extract token from Authorization header"""
        if not auth_header:
            return None
            
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return None
            
        return parts[1]