from typing import List, Dict, Any, Optional
from crewai import Agent, Task, Crew
from crewai.tools import BaseTool
import logging

logger = logging.getLogger(__name__)

class CrewOrchestrator:
    """Orchestrates CrewAI agents to execute plan tasks."""
    
    def __init__(self, crew_config: Dict[str, Any]):
        self.crew_config = crew_config
        self.agents = self._create_agents()
        self.crew = self._create_crew()
    
    def _create_agents(self) -> List[Agent]:
        """Create agents from configuration."""
        agents = []
        
        for agent_config in self.crew_config.get('agents', []):
            agent = Agent(
                role=agent_config['role'],
                goal=agent_config['goal'],
                backstory=agent_config.get('backstory', ''),
                tools=self._load_tools(agent_config.get('tools', [])),
                verbose=agent_config.get('verbose', False)
            )
            agents.append(agent)
        
        return agents
    
    def _load_tools(self, tool_names: List[str]) -> List[BaseTool]:
        """Load tools by name. Extend this for custom tools."""
        # Basic implementation - extend with actual tool loading
        return []
    
    def _create_crew(self) -> Crew:
        """Create crew from agents."""
        return Crew(
            agents=self.agents,
            verbose=self.crew_config.get('verbose', False)
        )
    
    def execute_plan_tasks(self, plan_tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute plan tasks using CrewAI orchestration."""
        if not plan_tasks:
            raise ValueError("No tasks provided to execute")
        
        crew_tasks = self._convert_to_crew_tasks(plan_tasks)
        
        try:
            result = self.crew.kickoff(tasks=crew_tasks)
            return {
                'status': 'success',
                'result': result,
                'tasks_completed': len(crew_tasks)
            }
        except Exception as e:
            logger.error(f"Crew execution failed: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'tasks_completed': 0
            }
    
    def _convert_to_crew_tasks(self, plan_tasks: List[Dict[str, Any]]) -> List[Task]:
        """Convert plan tasks to CrewAI tasks."""
        crew_tasks = []
        
        for i, task_data in enumerate(plan_tasks):
            # Assign agent round-robin style
            agent = self.agents[i % len(self.agents)] if self.agents else None
            
            task = Task(
                description=task_data.get('description', f"Task {i+1}"),
                agent=agent,
                expected_output=task_data.get('expected_output', 'Task completion')
            )
            crew_tasks.append(task)
        
        return crew_tasks