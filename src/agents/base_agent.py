from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

class AgentStatus(Enum):
    IDLE = "idle"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"

@dataclass
class AgentResponse:
    content: str
    status: AgentStatus
    metadata: Dict[str, Any]
    errors: Optional[list] = None
    
    def is_valid(self) -> bool:
        return self.status != AgentStatus.ERROR and not self.errors

class AgentError(Exception):
    def __init__(self, message: str, agent_type: str, details: Dict[str, Any] = None):
        super().__init__(message)
        self.agent_type = agent_type
        self.details = details or {}

class AIAgent(ABC):
    def __init__(self, name: str, config: Dict[str, Any] = None):
        self.name = name
        self.config = config or {}
        self.status = AgentStatus.IDLE
    
    @abstractmethod
    def process(self, input_data: str, context: Dict[str, Any] = None) -> AgentResponse:
        """Process input and return response"""
        pass
    
    def validate_input(self, input_data: str) -> None:
        """Validate input data"""
        if not input_data or not input_data.strip():
            raise AgentError("Input data cannot be empty", self.name)
    
    def _create_response(self, content: str, status: AgentStatus, 
                        metadata: Dict[str, Any] = None, errors: list = None) -> AgentResponse:
        return AgentResponse(
            content=content,
            status=status,
            metadata=metadata or {},
            errors=errors
        )