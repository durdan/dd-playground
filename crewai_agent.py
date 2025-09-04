from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from crewai import Agent
from crewai_tools import BaseTool


@dataclass
class AgentConfig:
    """Configuration for a CrewAI agent."""
    role: str
    goal: str
    backstory: str
    verbose: bool = True
    allow_delegation: bool = False
    tools: Optional[List[BaseTool]] = None
    llm_config: Optional[Dict[str, Any]] = None


class CrewAIAgentManager:
    """Manages CrewAI agents with validation and lifecycle."""
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
    
    def create_agent(self, agent_id: str, config: AgentConfig) -> Agent:
        """Create and register a new CrewAI agent."""
        if not agent_id or not agent_id.strip():
            raise ValueError("Agent ID cannot be empty")
        
        if not config.role or not config.goal or not config.backstory:
            raise ValueError("Agent role, goal, and backstory are required")
        
        if agent_id in self.agents:
            raise ValueError(f"Agent with ID '{agent_id}' already exists")
        
        try:
            agent = Agent(
                role=config.role,
                goal=config.goal,
                backstory=config.backstory,
                verbose=config.verbose,
                allow_delegation=config.allow_delegation,
                tools=config.tools or []
            )
            
            self.agents[agent_id] = agent
            return agent
            
        except Exception as e:
            raise RuntimeError(f"Failed to create agent '{agent_id}': {str(e)}")
    
    def get_agent(self, agent_id: str) -> Agent:
        """Retrieve an agent by ID."""
        if agent_id not in self.agents:
            raise KeyError(f"Agent '{agent_id}' not found")
        return self.agents[agent_id]
    
    def list_agents(self) -> List[str]:
        """List all registered agent IDs."""
        return list(self.agents.keys())
    
    def remove_agent(self, agent_id: str) -> None:
        """Remove an agent."""
        if agent_id not in self.agents:
            raise KeyError(f"Agent '{agent_id}' not found")
        del self.agents[agent_id]