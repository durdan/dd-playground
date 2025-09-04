from datetime import datetime
from typing import Optional

from .services import CrewAIService


class RunCommand:
    def __init__(self):
        self.service = CrewAIService()
    
    def execute(self, crew_name: str, config_path: Optional[str] = None) -> None:
        """Execute a crew"""
        if not crew_name.strip():
            raise ValueError("Crew name cannot be empty")
        
        crew = self.service.load_crew_config(crew_name, config_path)
        self.service.execute_crew(crew)
        print(f"Crew '{crew_name}' completed successfully")


class PlanCommand:
    def __init__(self):
        self.service = CrewAIService()
    
    def execute(self, crew_name: str, config_path: Optional[str] = None) -> None:
        """Show execution plan for a crew"""
        if not crew_name.strip():
            raise ValueError("Crew name cannot be empty")
        
        crew = self.service.load_crew_config(crew_name, config_path)
        plan = self.service.get_execution_plan(crew)
        
        for line in plan:
            print(line)


class StatusCommand:
    def __init__(self):
        self.service = CrewAIService()
    
    def execute(self, crew_name: Optional[str] = None) -> None:
        """Show crew execution status"""
        executions = self.service.get_crew_status(crew_name)
        
        if not executions:
            if crew_name:
                print(f"No execution found for crew '{crew_name}'")
            else:
                print("No crew executions found")
            return
        
        for name, execution in executions.items():
            print(f"Crew: {name}")
            print(f"  Status: {execution.status.value}")
            
            if execution.started_at:
                started = datetime.fromtimestamp(execution.started_at)
                print(f"  Started: {started.strftime('%Y-%m-%d %H:%M:%S')}")
            
            if execution.completed_at:
                completed = datetime.fromtimestamp(execution.completed_at)
                print(f"  Completed: {completed.strftime('%Y-%m-%d %H:%M:%S')}")
            
            if execution.error_message:
                print(f"  Error: {execution.error_message}")
            
            print()