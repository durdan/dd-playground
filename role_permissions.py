from enum import Enum
from typing import Set, Optional


class Role(Enum):
    USER = "user"
    ADMIN = "admin"


class Permission(Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    MANAGE_USERS = "manage_users"


class RolePermissions:
    """Maps roles to their allowed permissions."""
    
    _ROLE_PERMISSIONS = {
        Role.USER: {Permission.READ, Permission.WRITE},
        Role.ADMIN: {Permission.READ, Permission.WRITE, Permission.DELETE, Permission.MANAGE_USERS}
    }
    
    @classmethod
    def get_permissions(cls, role: Role) -> Set[Permission]:
        """Get all permissions for a given role."""
        if not isinstance(role, Role):
            raise ValueError(f"Invalid role: {role}")
        return cls._ROLE_PERMISSIONS[role].copy()


class User:
    """Represents a user with a role."""
    
    def __init__(self, username: str, role: Role):
        if not username or not username.strip():
            raise ValueError("Username cannot be empty")
        if not isinstance(role, Role):
            raise ValueError(f"Invalid role: {role}")
        
        self.username = username.strip()
        self.role = role


class PermissionChecker:
    """Service to check user permissions."""
    
    def __init__(self):
        self.role_permissions = RolePermissions()
    
    def has_permission(self, user: User, permission: Permission) -> bool:
        """Check if user has a specific permission."""
        if not isinstance(user, User):
            raise ValueError("Invalid user")
        if not isinstance(permission, Permission):
            raise ValueError(f"Invalid permission: {permission}")
        
        user_permissions = self.role_permissions.get_permissions(user.role)
        return permission in user_permissions
    
    def require_permission(self, user: User, permission: Permission) -> None:
        """Raise exception if user lacks permission."""
        if not self.has_permission(user, permission):
            raise PermissionError(f"User '{user.username}' with role '{user.role.value}' lacks permission '{permission.value}'")
    
    def get_user_permissions(self, user: User) -> Set[Permission]:
        """Get all permissions for a user."""
        if not isinstance(user, User):
            raise ValueError("Invalid user")
        return self.role_permissions.get_permissions(user.role)