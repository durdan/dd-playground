from .user import User
from .role import Permission
from .role_permission_mapper import RolePermissionMapper

class PermissionChecker:
    """Service to check user permissions"""
    
    def __init__(self):
        self.mapper = RolePermissionMapper()
    
    def has_permission(self, user: User, permission: Permission) -> bool:
        """Check if user has a specific permission"""
        if user is None:
            raise ValueError("User cannot be None")
        if permission is None:
            raise ValueError("Permission cannot be None")
            
        user_permissions = self.mapper.get_permissions(user.role)
        return permission in user_permissions
    
    def check_permission(self, user: User, permission: Permission) -> None:
        """Check permission and raise exception if not allowed"""
        if not self.has_permission(user, permission):
            raise PermissionError(f"User '{user.username}' with role '{user.role.value}' does not have '{permission.value}' permission")