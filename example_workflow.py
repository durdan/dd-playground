"""Example workflow to demonstrate the workflow management system."""

import time
from workflow_manager import WorkflowManager


def simulate_workflow():
    """Simulate a workflow with multiple steps."""
    wm = WorkflowManager()
    
    # Add workflow steps
    steps = ["data_collection", "data_processing", "model_training", "evaluation"]
    
    for step in steps:
        try:
            wm.add_step(step)
        except ValueError:
            pass  # Step already exists
    
    print("Workflow initialized with steps:", steps)
    print("You can now use:")
    print("  python cli_commands.py /crewai rerun <step_name>")
    print("  python cli_commands.py /crewai stop")
    print("  python cli_commands.py /crewai status")
    
    # Simulate running a step
    try:
        wm.start_step("data_collection")
        print("\nStarted data_collection step...")
        time.sleep(2)  # Simulate work
        wm.complete_step("data_collection", {"records": 1000})
        print("Completed data_collection step")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    simulate_workflow()