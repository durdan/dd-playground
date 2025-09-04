class CrewAIError(Exception):
    """Base exception for CrewAI CLI operations"""
    pass


class CrewNotFoundError(CrewAIError):
    """Raised when a crew cannot be found"""
    pass


class InvalidConfigError(CrewAIError):
    """Raised when crew configuration is invalid"""
    pass