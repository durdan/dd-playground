from typing import List, Dict, Any, Optional
from .agent import Agent
from .task import Task
from .exceptions import CrewError, AgentError

class Crew:
    """Manages a crew of agents and orchestrates task execution"""
    
    def __init__(self, name: str, agents: List[Agent]):
        if not name or not name.strip():
            raise CrewError("Crew name cannot be empty")
        if not agents:
            raise CrewError("Crew must have at least one agent")
        
        self.name = name
        self.agents = {agent.name: agent for agent in agents}
        self.task_queue: List[Task] = []
        self.completed_tasks: List[Dict[str, Any]] = []
    
    def add_agent(self, agent: Agent):
        """Add an agent to the crew"""
        if agent.name in self.agents:
            raise CrewError(f"Agent {agent.name} already exists in crew")
        self.agents[agent.name] = agent
    
    def assign_task(self, task: Task, agent_name: Optional[str] = None) -> Dict[str, Any]:
        """Assign task to specific agent or find suitable agent"""
        if agent_name:
            if agent_name not in self.agents:
                raise CrewError(f"Agent {agent_name} not found in crew")
            agent = self.agents[agent_name]
        else:
            agent = self._find_suitable_agent(task)
        
        if not agent:
            raise CrewError(f"No suitable agent found for task {task.id}")
        
        try:
            result = agent.execute_task(task.to_dict())
            self.completed_tasks.append({
                'task': task,
                'agent': agent.name,
                'result': result
            })
            return result
        except Exception as e:
            raise CrewError(f"Task execution failed: {str(e)}")
    
    def _find_suitable_agent(self, task: Task) -> Optional[Agent]:
        """Find agent suitable for the task based on role"""
        if task.required_role:
            for agent in self.agents.values():
                if agent.role.lower() == task.required_role.lower():
                    return agent
        
        # Return first available agent if no role requirement
        return next(iter(self.agents.values())) if self.agents else None
    
    def get_crew_status(self) -> Dict[str, Any]:
        """Get current crew status"""
        return {
            'name': self.name,
            'agents': [agent.get_capabilities() for agent in self.agents.values()],
            'tasks_completed': len(self.completed_tasks),
            'tasks_in_queue': len(self.task_queue)
        }