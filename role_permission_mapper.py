from typing import Set
from .role import Role, Permission

class RolePermissionMapper:
    """Maps roles to their allowed permissions"""
    
    _ROLE_PERMISSIONS = {
        Role.USER: {Permission.READ, Permission.WRITE},
        Role.ADMIN: {Permission.READ, Permission.WRITE, Permission.DELETE, Permission.MANAGE_USERS}
    }
    
    @classmethod
    def get_permissions(cls, role: Role) -> Set[Permission]:
        """Get all permissions for a given role"""
        if role is None:
            raise ValueError("Role cannot be None")
        
        return cls._ROLE_PERMISSIONS.get(role, set())