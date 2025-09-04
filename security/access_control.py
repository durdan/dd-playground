from enum import Enum
from typing import Set, Dict, Optional
from dataclasses import dataclass

class Permission(Enum):
    READ_PII = "read_pii"
    WRITE_PII = "write_pii"
    DELETE_PII = "delete_pii"
    AUDIT_ACCESS = "audit_access"
    ADMIN = "admin"

class Role(Enum):
    USER = "user"
    ANALYST = "analyst"
    ADMIN = "admin"
    DPO = "data_protection_officer"  # Data Protection Officer

@dataclass
class User:
    user_id: str
    role: Role
    permissions: Set[Permission]

class AccessControl:
    def __init__(self):
        self.role_permissions = {
            Role.USER: {Permission.READ_PII},
            Role.ANALYST: {Permission.READ_PII, Permission.WRITE_PII},
            Role.ADMIN: {Permission.READ_PII, Permission.WRITE_PII, Permission.DELETE_PII, Permission.ADMIN},
            Role.DPO: {Permission.READ_PII, Permission.WRITE_PII, Permission.DELETE_PII, Permission.AUDIT_ACCESS, Permission.ADMIN}
        }
        self.users: Dict[str, User] = {}
    
    def create_user(self, user_id: str, role: Role) -> User:
        """Create user with role-based permissions"""
        if not user_id:
            raise ValueError("User ID cannot be empty")
        
        permissions = self.role_permissions.get(role, set())
        user = User(user_id=user_id, role=role, permissions=permissions)
        self.users[user_id] = user
        return user
    
    def check_permission(self, user_id: str, permission: Permission) -> bool:
        """Check if user has specific permission"""
        user = self.users.get(user_id)
        if not user:
            return False
        return permission in user.permissions
    
    def require_permission(self, user_id: str, permission: Permission) -> None:
        """Raise exception if user lacks permission"""
        if not self.check_permission(user_id, permission):
            raise PermissionError(f"User {user_id} lacks permission: {permission.value}")