class UserManagementError(Exception):
    """Base exception for user management operations"""
    pass

class ValidationError(UserManagementError):
    """Raised when input validation fails"""
    pass

class NotFoundError(UserManagementError):
    """Raised when requested resource is not found"""
    pass

class PermissionError(UserManagementError):
    """Raised when user lacks required permissions"""
    pass

class DuplicateError(UserManagementError):
    """Raised when trying to create duplicate resource"""
    pass