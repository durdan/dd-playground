class CrewAIError(Exception):
    """Base exception for CrewAI system"""
    pass

class AgentError(CrewAIError):
    """Agent-related errors"""
    pass

class PolicyViolationError(CrewAIError):
    """Policy violation errors"""
    pass

class TaskError(CrewAIError):
    """Task-related errors"""
    pass

class CrewError(CrewAIError):
    """Crew management errors"""
    pass