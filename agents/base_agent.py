from abc import ABC, abstractmethod
from models import TaskRequest, AgentResponse, AgentRole

class BaseAgent(ABC):
    def __init__(self, role: AgentRole):
        self.role = role
    
    @abstractmethod
    def process(self, request: TaskRequest) -> AgentResponse:
        """Process a task request and return response"""
        pass
    
    def _create_response(self, status, result, feedback=None, suggestions=None, errors=None):
        """Helper to create standardized responses"""
        return AgentResponse(
            agent_role=self.role,
            status=status,
            result=result,
            feedback=feedback or [],
            suggestions=suggestions or [],
            errors=errors or []
        )