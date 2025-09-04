from typing import List, Optional, Tuple
from sandbox_mode import SandboxMode, Operation, SandboxSuggestion

class SandboxService:
    def __init__(self, repository):
        self._repository = repository
        self._sandbox = SandboxMode(repository.load_sandbox_state())
    
    def toggle_sandbox(self) -> bool:
        new_state = self._sandbox.toggle()
        self._repository.save_sandbox_state(new_state)
        return new_state
    
    def get_sandbox_status(self) -> bool:
        return self._sandbox.enabled
    
    def execute_operation(self, operation: Operation) -> Tuple[bool, Optional[SandboxSuggestion]]:
        """
        Execute operation if allowed, return suggestion if blocked.
        Returns: (success, suggestion)
        """
        if not operation:
            raise ValueError("Operation cannot be None")
            
        if self._sandbox.is_operation_allowed(operation):
            return True, None
        
        suggestion = self._sandbox.get_suggestion(operation)
        return False, suggestion
    
    def validate_operations(self, operations: List[Operation]) -> List[SandboxSuggestion]:
        """Validate multiple operations and return suggestions for blocked ones."""
        if not operations:
            return []
            
        suggestions = []
        for op in operations:
            if not self._sandbox.is_operation_allowed(op):
                suggestion = self._sandbox.get_suggestion(op)
                if suggestion:
                    suggestions.append(suggestion)
        
        return suggestions