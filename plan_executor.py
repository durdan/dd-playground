import json
import yaml
from typing import Dict, Any, Optional
from pathlib import Path
import logging

from .crew_orchestrator import CrewOrchestrator

logger = logging.getLogger(__name__)

class PlanExecutor:
    """Executes plans with optional CrewAI orchestration."""
    
    def __init__(self, use_crew: bool = False, crew_config: Optional[Dict[str, Any]] = None):
        self.use_crew = use_crew
        self.crew_orchestrator = None
        
        if use_crew:
            if not crew_config:
                crew_config = self._get_default_crew_config()
            self.crew_orchestrator = CrewOrchestrator(crew_config)
    
    def execute_plan(self, plan_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a plan with optional CrewAI orchestration."""
        if not plan_data:
            raise ValueError("Plan data cannot be empty")
        
        tasks = plan_data.get('tasks', [])
        if not tasks:
            raise ValueError("Plan must contain tasks")
        
        if self.use_crew and self.crew_orchestrator:
            logger.info("Executing plan with CrewAI orchestration")
            return self.crew_orchestrator.execute_plan_tasks(tasks)
        else:
            logger.info("Executing plan without orchestration")
            return self._execute_sequential(tasks)
    
    def execute_plan_file(self, plan_file: Path) -> Dict[str, Any]:
        """Execute plan from file."""
        if not plan_file.exists():
            raise FileNotFoundError(f"Plan file not found: {plan_file}")
        
        plan_data = self._load_plan_file(plan_file)
        return self.execute_plan(plan_data)
    
    def _load_plan_file(self, plan_file: Path) -> Dict[str, Any]:
        """Load plan from JSON or YAML file."""
        content = plan_file.read_text()
        
        if plan_file.suffix.lower() in ['.yml', '.yaml']:
            return yaml.safe_load(content)
        elif plan_file.suffix.lower() == '.json':
            return json.loads(content)
        else:
            raise ValueError(f"Unsupported plan file format: {plan_file.suffix}")
    
    def _execute_sequential(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute tasks sequentially without CrewAI."""
        completed = 0
        results = []
        
        for task in tasks:
            try:
                # Basic task execution - extend as needed
                result = {
                    'task': task.get('description', 'Unknown task'),
                    'status': 'completed',
                    'output': f"Executed: {task.get('description', 'task')}"
                }
                results.append(result)
                completed += 1
            except Exception as e:
                results.append({
                    'task': task.get('description', 'Unknown task'),
                    'status': 'failed',
                    'error': str(e)
                })
        
        return {
            'status': 'success' if completed == len(tasks) else 'partial',
            'tasks_completed': completed,
            'total_tasks': len(tasks),
            'results': results
        }
    
    def _get_default_crew_config(self) -> Dict[str, Any]:
        """Default crew configuration."""
        return {
            'agents': [
                {
                    'role': 'Task Executor',
                    'goal': 'Execute plan tasks efficiently',
                    'backstory': 'An experienced task executor focused on completing objectives.',
                    'verbose': True
                }
            ],
            'verbose': True
        }