from dataclasses import dataclass
from typing import Dict, Any, List, Optional
from crewai import Crew, Task, Agent
from crewai_agent import CrewAIAgentManager


@dataclass
class TaskConfig:
    """Configuration for a CrewAI task."""
    description: str
    agent_id: str
    expected_output: str
    tools: Optional[List] = None


@dataclass
class CrewConfig:
    """Configuration for a CrewAI crew."""
    agents: List[str]  # Agent IDs
    tasks: List[TaskConfig]
    verbose: bool = True
    process_type: str = "sequential"  # sequential or hierarchical


class CrewAICrewManager:
    """Manages CrewAI crews and task execution."""
    
    def __init__(self, agent_manager: CrewAIAgentManager):
        self.agent_manager = agent_manager
        self.crews: Dict[str, Crew] = {}
    
    def create_crew(self, crew_id: str, config: CrewConfig) -> Crew:
        """Create and register a new CrewAI crew."""
        if not crew_id or not crew_id.strip():
            raise ValueError("Crew ID cannot be empty")
        
        if crew_id in self.crews:
            raise ValueError(f"Crew with ID '{crew_id}' already exists")
        
        if not config.agents:
            raise ValueError("Crew must have at least one agent")
        
        if not config.tasks:
            raise ValueError("Crew must have at least one task")
        
        try:
            # Validate and collect agents
            agents = []
            for agent_id in config.agents:
                agent = self.agent_manager.get_agent(agent_id)
                agents.append(agent)
            
            # Create tasks
            tasks = []
            for task_config in config.tasks:
                agent = self.agent_manager.get_agent(task_config.agent_id)
                task = Task(
                    description=task_config.description,
                    agent=agent,
                    expected_output=task_config.expected_output,
                    tools=task_config.tools or []
                )
                tasks.append(task)
            
            # Create crew
            crew = Crew(
                agents=agents,
                tasks=tasks,
                verbose=config.verbose,
                process=config.process_type
            )
            
            self.crews[crew_id] = crew
            return crew
            
        except Exception as e:
            raise RuntimeError(f"Failed to create crew '{crew_id}': {str(e)}")
    
    def execute_crew(self, crew_id: str, inputs: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a crew and return results."""
        if crew_id not in self.crews:
            raise KeyError(f"Crew '{crew_id}' not found")
        
        try:
            crew = self.crews[crew_id]
            result = crew.kickoff(inputs=inputs or {})
            
            return {
                "crew_id": crew_id,
                "status": "completed",
                "result": str(result),
                "inputs": inputs or {}
            }
            
        except Exception as e:
            return {
                "crew_id": crew_id,
                "status": "failed",
                "error": str(e),
                "inputs": inputs or {}
            }
    
    def get_crew(self, crew_id: str) -> Crew:
        """Retrieve a crew by ID."""
        if crew_id not in self.crews:
            raise KeyError(f"Crew '{crew_id}' not found")
        return self.crews[crew_id]
    
    def list_crews(self) -> List[str]:
        """List all registered crew IDs."""
        return list(self.crews.keys())