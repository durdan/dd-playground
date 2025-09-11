class UserException(Exception):
    """Base exception for user operations"""
    pass

class UserNotFoundError(UserException):
    """Raised when user is not found"""
    pass

class UserAlreadyExistsError(UserException):
    """Raised when trying to create duplicate user"""
    pass

class InvalidCredentialsError(UserException):
    """Raised when authentication fails"""
    pass