from typing import Dict, Any, List
from services.user_service import UserService
from exceptions.user_exceptions import UserException

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
                'user': self._serialize_user(user),
                'status': 201
            }
        except UserException as e:
            return {'error': str(e), 'status': 409}
        except ValueError as e:
            return {'error': str(e), 'status': 400}
    
    def authenticate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            username_or_email = data.get('username_or_email', '').strip()
            password = data.get('password', '')
            
            if not all([username_or_email, password]):
                return {'error': 'Username/email and password are required', 'status': 400}
            
            user = self._user_service.authenticate(username_or_email, password)
            return {
                'user': self._serialize_user(user),
                'status': 200
            }
        except UserException as e:
            return {'error': str(e), 'status': 401}
    
    def get_user(self, user_id: str) -> Dict[str, Any]:
        try:
            user = self._user_service.get_user(user_id)
            return {
                'user': self._serialize_user(user),
                'status': 200
            }
        except UserException as e:
            return {'error': str(e), 'status': 404}
    
    def list_users(self) -> Dict[str, Any]:
        users = self._user_service.list_users()
        return {
            'users': [self._serialize_user(user) for user in users],
            'status': 200
        }
    
    def _serialize_user(self, user) -> Dict[str, Any]:
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at.isoformat(),
            'is_active': user.is_active
        }