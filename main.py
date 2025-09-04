#!/usr/bin/env python3
from sandbox_repository import SandboxRepository
from sandbox_service import SandboxService
from sandbox_controller import SandboxController
from sandbox_mode import Operation, OperationType

def main():
    # Setup
    repo = SandboxRepository("demo_sandbox.json")
    service = SandboxService(repo)
    controller = SandboxController(service)
    
    print("=== Sandbox Mode Demo ===")
    
    # Show initial status
    status = controller.get_status()
    print(f"Initial sandbox status: {'ON' if status['sandbox_enabled'] else 'OFF'}")
    
    # Toggle sandbox on
    result = controller.toggle_sandbox()
    print(f"\n{result['message']}")
    
    # Try some operations
    operations = [
        {'type': 'read', 'target': 'config.txt', 'description': 'Read config file'},
        {'type': 'write', 'target': 'data.txt', 'description': 'Write user data'},
        {'type': 'delete', 'target': 'temp.log', 'description': 'Delete temp file'}
    ]
    
    print("\n=== Testing Operations ===")
    for op_data in operations:
        result = controller.execute_operation(op_data)
        print(f"\nOperation: {op_data['type']} {op_data['target']}")
        
        if result['success']:
            print(f"✓ {result['message']}")
        elif result.get('blocked'):
            print(f"✗ Blocked: {result['suggestion']['explanation']}")
            print(f"  Suggestion: {result['suggestion']['alternative']}")
        else:
            print(f"✗ Error: {result['error']}")
    
    # Toggle sandbox off
    print("\n" + "="*30)
    result = controller.toggle_sandbox()
    print(f"{result['message']}")
    
    # Try write operation again
    write_op = {'type': 'write', 'target': 'data.txt', 'description': 'Write user data'}
    result = controller.execute_operation(write_op)
    print(f"\nRetrying write operation:")
    print(f"✓ {result['message']}" if result['success'] else f"✗ {result['error']}")
    
    # Cleanup
    repo.clear_config()

if __name__ == "__main__":
    main()