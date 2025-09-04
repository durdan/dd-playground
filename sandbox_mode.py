from enum import Enum
from dataclasses import dataclass
from typing import List, Optional

class OperationType(Enum):
    READ = "read"
    WRITE = "write" 
    DELETE = "delete"
    MODIFY = "modify"

@dataclass
class Operation:
    type: OperationType
    description: str
    target: str

@dataclass
class SandboxSuggestion:
    original_operation: Operation
    safe_alternative: str
    explanation: str

class SandboxMode:
    def __init__(self, enabled: bool = False):
        self._enabled = enabled
        self._blocked_operations = {
            OperationType.WRITE,
            OperationType.DELETE, 
            OperationType.MODIFY
        }
    
    @property
    def enabled(self) -> bool:
        return self._enabled
    
    def toggle(self) -> bool:
        self._enabled = not self._enabled
        return self._enabled
    
    def enable(self) -> None:
        self._enabled = True
    
    def disable(self) -> None:
        self._enabled = False
    
    def is_operation_allowed(self, operation: Operation) -> bool:
        if not self._enabled:
            return True
        return operation.type not in self._blocked_operations
    
    def get_suggestion(self, operation: Operation) -> Optional[SandboxSuggestion]:
        if self.is_operation_allowed(operation):
            return None
            
        suggestions = {
            OperationType.WRITE: f"Use 'preview {operation.target}' to see what would be written",
            OperationType.DELETE: f"Use 'list {operation.target}' to see what would be deleted", 
            OperationType.MODIFY: f"Use 'diff {operation.target}' to see proposed changes"
        }
        
        return SandboxSuggestion(
            original_operation=operation,
            safe_alternative=suggestions.get(operation.type, "Use read-only equivalent"),
            explanation=f"Sandbox mode prevents {operation.type.value} operations"
        )