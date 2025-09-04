"""Crew orchestration and management."""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import logging

from .agent import Agent
from .task import Task, TaskStatus


@dataclass
class CrewConfig:
    """Configuration for a crew."""
    name: str
    description: str
    agents: List[Agent]
    tasks: List[Task]
    process_type: str = "sequential"  # sequential, hierarchical, parallel
    verbose: bool = False
    max_retries: int = 3

    def __post_init__(self):
        if not self.agents:
            raise ValueError("Crew must have at least one agent")
        if not self.tasks:
            raise ValueError("Crew must have at least one task")


class Crew:
    """Crew execution engine."""
    
    def __init__(self, config: CrewConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self._validate_config()
    
    def _validate_config(self):
        """Validate crew configuration."""
        if not self.config.name:
            raise ValueError("Crew name is required")
        
        # Validate agent-task assignments
        agent_roles = {agent.config.role for agent in self.config.agents}
        for task in self.config.tasks:
            if task.config.agent_role and task.config.agent_role not in agent_roles:
                raise ValueError(f"Task {task.config.name} requires agent role {task.config.agent_role} not found in crew")
    
    def execute(self) -> Dict[str, Any]:
        """Execute all tasks in the crew."""
        if self.config.process_type == "sequential":
            return self._execute_sequential()
        elif self.config.process_type == "parallel":
            return self._execute_parallel()
        else:
            raise ValueError(f"Unsupported process type: {self.config.process_type}")
    
    def _execute_sequential(self) -> Dict[str, Any]:
        """Execute tasks sequentially."""
        results = {}
        completed_tasks = []
        
        for task in self.config.tasks:
            if not task.is_ready(completed_tasks):
                task.mark_failed(f"Dependencies not satisfied: {task.config.dependencies}")
                continue
            
            agent = self._find_agent_for_task(task)
            if not agent:
                task.mark_failed(f"No suitable agent found for role: {task.config.agent_role}")
                continue
            
            try:
                task.mark_in_progress()
                result = agent.execute_task(task)
                task.mark_completed(result)
                results[task.config.name] = result
                completed_tasks.append(task.config.name)
                
                if self.config.verbose:
                    self.logger.info(f"Completed task: {task.config.name}")
                    
            except Exception as e:
                task.mark_failed(str(e))
                self.logger.error(f"Task {task.config.name} failed: {e}")
                if self.config.verbose:
                    raise
        
        return {
            "crew_name": self.config.name,
            "completed_tasks": len(completed_tasks),
            "total_tasks": len(self.config.tasks),
            "results": results
        }
    
    def _execute_parallel(self) -> Dict[str, Any]:
        """Execute tasks in parallel (placeholder for future implementation)."""
        # For now, fall back to sequential
        self.logger.warning("Parallel execution not yet implemented, falling back to sequential")
        return self._execute_sequential()
    
    def _find_agent_for_task(self, task: Task) -> Optional[Agent]:
        """Find the best agent for a task."""
        if task.config.agent_role:
            for agent in self.config.agents:
                if agent.config.role == task.config.agent_role:
                    return agent
        
        # Return first available agent if no specific role required
        return self.config.agents[0] if self.config.agents else None
    
    def get_status(self) -> Dict[str, Any]:
        """Get current crew execution status."""
        task_statuses = {task.config.name: task.status.value for task in self.config.tasks}
        return {
            "crew_name": self.config.name,
            "task_statuses": task_statuses,
            "agents_count": len(self.config.agents)
        }