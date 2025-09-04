import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from .models import CrewExecution, CrewStatus


class StatusManager:
    def __init__(self, storage_path: str = ".crewai_status.json"):
        self.storage_path = Path(storage_path)
    
    def save_execution(self, execution: CrewExecution) -> None:
        """Save crew execution status to storage"""
        data = self._load_data()
        
        execution_data = {
            'status': execution.status.value,
            'started_at': execution.started_at,
            'completed_at': execution.completed_at,
            'error_message': execution.error_message
        }
        
        data[execution.crew_name] = execution_data
        self._save_data(data)
    
    def get_executions(self, crew_name: Optional[str] = None) -> Dict[str, CrewExecution]:
        """Get execution status for crew(s)"""
        data = self._load_data()
        
        if crew_name:
            if crew_name not in data:
                return {}
            data = {crew_name: data[crew_name]}
        
        executions = {}
        for name, exec_data in data.items():
            executions[name] = CrewExecution(
                crew_name=name,
                status=CrewStatus(exec_data['status']),
                started_at=exec_data.get('started_at'),
                completed_at=exec_data.get('completed_at'),
                error_message=exec_data.get('error_message')
            )
        
        return executions
    
    def _load_data(self) -> dict:
        """Load data from storage file"""
        if not self.storage_path.exists():
            return {}
        
        try:
            with open(self.storage_path) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    
    def _save_data(self, data: dict) -> None:
        """Save data to storage file"""
        try:
            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            raise RuntimeError(f"Failed to save status: {e}")