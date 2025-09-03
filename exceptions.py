class UserError(Exception):
    """Base exception for user operations"""
    pass

class ValidationError(UserError):
    """Raised when user input is invalid"""
    pass

class UserNotFoundError(UserError):
    """Raised when user doesn't exist"""
    pass

class UserAlreadyExistsError(UserError):
    """Raised when trying to create user with existing email"""
    pass