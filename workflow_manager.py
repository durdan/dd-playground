import json
import os
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict


class WorkflowState(Enum):
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class WorkflowStep:
    name: str
    status: str
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    error: Optional[str] = None
    output: Optional[Dict[str, Any]] = None


class WorkflowManager:
    def __init__(self, state_file: str = ".crewai_workflow_state.json"):
        self.state_file = state_file
        self.state = WorkflowState.IDLE
        self.steps: Dict[str, WorkflowStep] = {}
        self.current_step: Optional[str] = None
        self.load_state()

    def load_state(self) -> None:
        """Load workflow state from file."""
        if not os.path.exists(self.state_file):
            return
        
        try:
            with open(self.state_file, 'r') as f:
                data = json.load(f)
                self.state = WorkflowState(data.get('state', 'idle'))
                self.current_step = data.get('current_step')
                
                steps_data = data.get('steps', {})
                self.steps = {
                    name: WorkflowStep(**step_data) 
                    for name, step_data in steps_data.items()
                }
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Warning: Could not load workflow state: {e}")

    def save_state(self) -> None:
        """Save workflow state to file."""
        data = {
            'state': self.state.value,
            'current_step': self.current_step,
            'steps': {name: asdict(step) for name, step in self.steps.items()}
        }
        
        with open(self.state_file, 'w') as f:
            json.dump(data, f, indent=2)

    def add_step(self, step_name: str) -> None:
        """Add a new step to the workflow."""
        if step_name in self.steps:
            raise ValueError(f"Step '{step_name}' already exists")
        
        self.steps[step_name] = WorkflowStep(name=step_name, status="pending")
        self.save_state()

    def start_step(self, step_name: str) -> None:
        """Start executing a workflow step."""
        if step_name not in self.steps:
            raise ValueError(f"Step '{step_name}' not found")
        
        if self.state == WorkflowState.RUNNING:
            raise ValueError("Workflow is already running")
        
        self.current_step = step_name
        self.state = WorkflowState.RUNNING
        self.steps[step_name].status = "running"
        self.steps[step_name].start_time = datetime.now().isoformat()
        self.steps[step_name].error = None
        self.save_state()

    def complete_step(self, step_name: str, output: Optional[Dict[str, Any]] = None) -> None:
        """Mark a step as completed."""
        if step_name not in self.steps:
            raise ValueError(f"Step '{step_name}' not found")
        
        self.steps[step_name].status = "completed"
        self.steps[step_name].end_time = datetime.now().isoformat()
        self.steps[step_name].output = output
        self.current_step = None
        self.state = WorkflowState.IDLE
        self.save_state()

    def fail_step(self, step_name: str, error: str) -> None:
        """Mark a step as failed."""
        if step_name not in self.steps:
            raise ValueError(f"Step '{step_name}' not found")
        
        self.steps[step_name].status = "failed"
        self.steps[step_name].end_time = datetime.now().isoformat()
        self.steps[step_name].error = error
        self.current_step = None
        self.state = WorkflowState.FAILED
        self.save_state()

    def rerun_step(self, step_name: str) -> None:
        """Rerun a specific workflow step."""
        if step_name not in self.steps:
            raise ValueError(f"Step '{step_name}' not found")
        
        if self.state == WorkflowState.RUNNING:
            raise ValueError("Cannot rerun step while workflow is running")
        
        # Reset step state
        self.steps[step_name].status = "pending"
        self.steps[step_name].start_time = None
        self.steps[step_name].end_time = None
        self.steps[step_name].error = None
        self.steps[step_name].output = None
        
        self.save_state()
        print(f"Step '{step_name}' has been reset and is ready to rerun")

    def stop_workflow(self) -> None:
        """Stop the currently running workflow."""
        if self.state != WorkflowState.RUNNING:
            raise ValueError("No workflow is currently running")
        
        if self.current_step:
            self.steps[self.current_step].status = "stopped"
            self.steps[self.current_step].end_time = datetime.now().isoformat()
        
        self.current_step = None
        self.state = WorkflowState.PAUSED
        self.save_state()
        print("Workflow has been stopped")

    def get_status(self) -> Dict[str, Any]:
        """Get current workflow status."""
        return {
            'state': self.state.value,
            'current_step': self.current_step,
            'total_steps': len(self.steps),
            'completed_steps': len([s for s in self.steps.values() if s.status == "completed"]),
            'failed_steps': len([s for s in self.steps.values() if s.status == "failed"]),
            'steps': {name: asdict(step) for name, step in self.steps.items()}
        }

    def list_steps(self) -> List[str]:
        """List all available steps."""
        return list(self.steps.keys())