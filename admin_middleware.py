from functools import wraps
from flask import request, jsonify, g
from jwt_auth import JWTAuth

class AdminMiddleware:
    def __init__(self):
        self.jwt_auth = JWTAuth()
    
    def require_admin(self, f):
        """Decorator to protect admin routes"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Extract token from Authorization header
            auth_header = request.headers.get('Authorization')
            token = self.jwt_auth.extract_token_from_header(auth_header)
            
            if not token:
                return jsonify({'error': 'Authorization token required'}), 401
            
            # Decode and validate token
            payload = self.jwt_auth.decode_token(token)
            if not payload:
                return jsonify({'error': 'Invalid or expired token'}), 401
            
            # Check admin role
            user_role = payload.get('role')
            if user_role != 'admin':
                return jsonify({'error': 'Admin access required'}), 403
            
            # Store user info in Flask's g object for use in route handlers
            g.current_user = {
                'user_id': payload.get('user_id'),
                'username': payload.get('username'),
                'role': payload.get('role')
            }
            
            return f(*args, **kwargs)
        
        return decorated_function

# Global middleware instance
admin_middleware = AdminMiddleware()