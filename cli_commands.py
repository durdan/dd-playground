import argparse
import sys
from typing import List
from workflow_manager import WorkflowManager


class CrewAICLI:
    def __init__(self):
        self.workflow_manager = WorkflowManager()

    def rerun_command(self, step_name: str) -> None:
        """Handle /crewai rerun <step> command."""
        try:
            available_steps = self.workflow_manager.list_steps()
            
            if not available_steps:
                print("No workflow steps found. Please initialize a workflow first.")
                return
            
            if step_name not in available_steps:
                print(f"Error: Step '{step_name}' not found.")
                print(f"Available steps: {', '.join(available_steps)}")
                return
            
            self.workflow_manager.rerun_step(step_name)
            print(f"Successfully reset step '{step_name}' for rerun")
            
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def stop_command(self) -> None:
        """Handle /crewai stop command."""
        try:
            self.workflow_manager.stop_workflow()
            
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def status_command(self) -> None:
        """Show current workflow status."""
        status = self.workflow_manager.get_status()
        
        print(f"Workflow State: {status['state']}")
        print(f"Current Step: {status['current_step'] or 'None'}")
        print(f"Progress: {status['completed_steps']}/{status['total_steps']} steps completed")
        
        if status['failed_steps'] > 0:
            print(f"Failed Steps: {status['failed_steps']}")
        
        if status['steps']:
            print("\nSteps:")
            for name, step in status['steps'].items():
                status_icon = {
                    'pending': '⏳',
                    'running': '🔄',
                    'completed': '✅',
                    'failed': '❌',
                    'stopped': '⏹️'
                }.get(step['status'], '❓')
                
                print(f"  {status_icon} {name}: {step['status']}")
                if step['error']:
                    print(f"    Error: {step['error']}")

    def parse_and_execute(self, args: List[str]) -> None:
        """Parse command line arguments and execute appropriate command."""
        if not args or args[0] != '/crewai':
            print("Usage: /crewai <command> [args]")
            return
        
        if len(args) < 2:
            print("Available commands: rerun <step>, stop, status")
            return
        
        command = args[1].lower()
        
        if command == 'rerun':
            if len(args) < 3:
                print("Usage: /crewai rerun <step_name>")
                return
            step_name = args[2]
            self.rerun_command(step_name)
            
        elif command == 'stop':
            self.stop_command()
            
        elif command == 'status':
            self.status_command()
            
        else:
            print(f"Unknown command: {command}")
            print("Available commands: rerun <step>, stop, status")


def main():
    """Main CLI entry point."""
    cli = CrewAICLI()
    
    if len(sys.argv) < 2:
        print("Usage: python cli_commands.py /crewai <command> [args]")
        print("Commands:")
        print("  /crewai rerun <step>  - Rerun a specific workflow step")
        print("  /crewai stop          - Stop the currently running workflow")
        print("  /crewai status        - Show workflow status")
        return
    
    cli.parse_and_execute(sys.argv[1:])


if __name__ == "__main__":
    main()