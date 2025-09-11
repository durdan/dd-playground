class UserManagementError(Exception):
    """Base exception for user management system."""
    pass

class UserNotFoundError(UserManagementError):
    """Raised when user is not found."""
    pass

class UserAlreadyExistsError(UserManagementError):
    """Raised when trying to create a user that already exists."""
    pass

class ValidationError(UserManagementError):
    """Raised when user data validation fails."""
    pass