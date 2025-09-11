from typing import Dict, Any, List, Optional
from services.user_service import UserService

class UserController:
    def __init__(self, user_service: UserService):
        self._user_service = user_service
    
    def create_user(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            username = data.get('username', '').strip()
            email = data.get('email', '').strip()
            password = data.get('password', '')
            
            if not all([username, email, password]):
                return {'error': 'Username, email, and password are required', 'status': 400}
            
            user = self._user_service.create_user(username, email, password)
            return {
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'created_at': user.created_at.isoformat(),
                    'is_active': user.is_active
                },
                'status': 201
            }
        except ValueError as e:
            return {'error': str(e), 'status': 400}
        except Exception as e:
            return {'error': 'Internal server error', 'status': 500}
    
    def get_user(self, user_id: int) -> Dict[str, Any]:
        try:
            user = self._user_service.get_user_by_id(user_id)
            if not user:
                return {'error': 'User not found', 'status': 404}
            
            return {
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'created_at': user.created_at.isoformat(),
                    'is_active': user.is_active
                },
                'status': 200
            }
        except ValueError as e:
            return {'error': str(e), 'status': 400}
        except Exception as e:
            return {'error': 'Internal server error', 'status': 500}
    
    def login(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            username = data.get('username', '').strip()
            password = data.get('password', '')
            
            if not username or not password:
                return {'error': 'Username and password are required', 'status': 400}
            
            user = self._user_service.authenticate_user(username, password)
            if not user:
                return {'error': 'Invalid credentials', 'status': 401}
            
            return {
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                },
                'status': 200
            }
        except Exception as e:
            return {'error': 'Internal server error', 'status': 500}