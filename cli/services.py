import json
import time
from pathlib import Path
from typing import Dict, List, Optional

from .exceptions import CrewNotFoundError, InvalidConfigError
from .models import Agent, Crew, CrewExecution, CrewStatus, Task
from .storage import StatusManager


class CrewAIService:
    def __init__(self):
        self.status_manager = StatusManager()
    
    def load_crew_config(self, crew_name: str, config_path: Optional[str] = None) -> Crew:
        """Load crew configuration from file or default location"""
        if config_path:
            config_file = Path(config_path)
        else:
            config_file = Path(f"crews/{crew_name}.json")
        
        if not config_file.exists():
            raise CrewNotFoundError(f"Crew configuration not found: {config_file}")
        
        try:
            with open(config_file) as f:
                data = json.load(f)
            
            agents = [Agent(**agent_data) for agent_data in data.get('agents', [])]
            tasks = [Task(**task_data) for task_data in data.get('tasks', [])]
            
            return Crew(name=crew_name, agents=agents, tasks=tasks)
            
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            raise InvalidConfigError(f"Invalid crew configuration: {e}")
    
    def execute_crew(self, crew: Crew) -> None:
        """Execute a crew (mock implementation)"""
        execution = CrewExecution(
            crew_name=crew.name,
            status=CrewStatus.RUNNING,
            started_at=time.time()
        )
        
        self.status_manager.save_execution(execution)
        
        try:
            # Mock execution - simulate work
            print(f"Starting crew '{crew.name}' with {len(crew.agents)} agents...")
            
            for task in crew.tasks:
                print(f"Executing task: {task.name}")
                time.sleep(0.5)  # Simulate work
            
            execution.status = CrewStatus.COMPLETED
            execution.completed_at = time.time()
            
        except Exception as e:
            execution.status = CrewStatus.FAILED
            execution.error_message = str(e)
            raise
        
        finally:
            self.status_manager.save_execution(execution)
    
    def get_execution_plan(self, crew: Crew) -> List[str]:
        """Generate execution plan for a crew"""
        plan = [f"Execution plan for crew '{crew.name}':"]
        plan.append(f"Agents ({len(crew.agents)}):")
        
        for agent in crew.agents:
            plan.append(f"  - {agent.name} ({agent.role}): {agent.goal}")
        
        plan.append(f"Tasks ({len(crew.tasks)}):")
        for i, task in enumerate(crew.tasks, 1):
            deps = f" (depends on: {', '.join(task.dependencies)})" if task.dependencies else ""
            plan.append(f"  {i}. {task.name} -> {task.agent}{deps}")
        
        return plan
    
    def get_crew_status(self, crew_name: Optional[str] = None) -> Dict[str, CrewExecution]:
        """Get status of specific crew or all crews"""
        return self.status_manager.get_executions(crew_name)