from typing import Dict, Any, List
from sandbox_mode import Operation, OperationType
from sandbox_service import SandboxService

class SandboxController:
    def __init__(self, service: SandboxService):
        self._service = service
    
    def toggle_sandbox(self) -> Dict[str, Any]:
        """Toggle sandbox mode and return status."""
        try:
            new_state = self._service.toggle_sandbox()
            return {
                'success': True,
                'sandbox_enabled': new_state,
                'message': f"Sandbox mode {'enabled' if new_state else 'disabled'}"
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_status(self) -> Dict[str, Any]:
        """Get current sandbox status."""
        return {
            'sandbox_enabled': self._service.get_sandbox_status()
        }
    
    def execute_operation(self, operation_data: Dict[str, str]) -> Dict[str, Any]:
        """Execute an operation, returning result or suggestion."""
        try:
            # Validate input
            if not operation_data.get('type') or not operation_data.get('target'):
                return {
                    'success': False,
                    'error': 'Operation type and target are required'
                }
            
            op_type = OperationType(operation_data['type'])
            operation = Operation(
                type=op_type,
                description=operation_data.get('description', ''),
                target=operation_data['target']
            )
            
            success, suggestion = self._service.execute_operation(operation)
            
            if success:
                return {
                    'success': True,
                    'message': f"Operation {operation.type.value} on {operation.target} completed"
                }
            else:
                return {
                    'success': False,
                    'blocked': True,
                    'suggestion': {
                        'alternative': suggestion.safe_alternative,
                        'explanation': suggestion.explanation
                    }
                }
                
        except ValueError as e:
            return {
                'success': False,
                'error': f"Invalid operation: {e}"
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }