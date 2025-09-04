from dataclasses import dataclass
from enum import Enum
from typing import List, Callable, Dict, Any
from datetime import datetime, timedelta
import logging

class Frequency(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class MaintenanceTask:
    id: str
    name: str
    description: str
    frequency: Frequency
    task_function: Callable[[], bool]
    owner: str
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    status: TaskStatus = TaskStatus.PENDING

class MaintenanceScheduler:
    def __init__(self):
        self.tasks: Dict[str, MaintenanceTask] = {}
        self.logger = logging.getLogger(__name__)
    
    def add_task(self, task: MaintenanceTask) -> None:
        if not task.id or not task.name:
            raise ValueError("Task ID and name are required")
        
        if not callable(task.task_function):
            raise ValueError("Task function must be callable")
        
        task.next_run = self._calculate_next_run(task.frequency)
        self.tasks[task.id] = task
    
    def run_due_tasks(self) -> Dict[str, bool]:
        results = {}
        now = datetime.now()
        
        for task_id, task in self.tasks.items():
            if task.next_run and now >= task.next_run:
                results[task_id] = self._execute_task(task)
        
        return results
    
    def _execute_task(self, task: MaintenanceTask) -> bool:
        self.logger.info(f"Starting maintenance task: {task.name}")
        task.status = TaskStatus.RUNNING
        
        try:
            success = task.task_function()
            task.status = TaskStatus.COMPLETED if success else TaskStatus.FAILED
            task.last_run = datetime.now()
            task.next_run = self._calculate_next_run(task.frequency, task.last_run)
            
            self.logger.info(f"Task {task.name} {'completed' if success else 'failed'}")
            return success
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            self.logger.error(f"Task {task.name} failed with error: {e}")
            return False
    
    def _calculate_next_run(self, frequency: Frequency, from_date: Optional[datetime] = None) -> datetime:
        base_date = from_date or datetime.now()
        
        if frequency == Frequency.DAILY:
            return base_date + timedelta(days=1)
        elif frequency == Frequency.WEEKLY:
            return base_date + timedelta(weeks=1)
        elif frequency == Frequency.MONTHLY:
            return base_date + timedelta(days=30)
        elif frequency == Frequency.QUARTERLY:
            return base_date + timedelta(days=90)
        
        raise ValueError(f"Unknown frequency: {frequency}")
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")
        
        task = self.tasks[task_id]
        return {
            "id": task.id,
            "name": task.name,
            "status": task.status.value,
            "last_run": task.last_run,
            "next_run": task.next_run,
            "owner": task.owner
        }