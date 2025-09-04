from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from crewai import Agent, Task, Crew, Process
from crewai.llm import LLM
import logging

logger = logging.getLogger(__name__)

@dataclass
class AgentConfig:
    """Configuration for a CrewAI agent with provider settings."""
    role: str
    goal: str
    backstory: str
    provider: str
    model: str
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    verbose: bool = True
    allow_delegation: bool = False

class ProviderLLMWrapper(LLM):
    """Wrapper to make provider manager compatible with CrewAI's LLM interface."""
    
    def __init__(self, provider_manager, provider: str, model: str, **kwargs):
        self.provider_manager = provider_manager
        self.provider = provider
        self.model = model
        self.config = kwargs
        super().__init__()
    
    def call(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Convert CrewAI messages to provider manager format and get response."""
        try:
            # Convert messages to simple prompt for now
            # In production, you might want more sophisticated message handling
            prompt = self._messages_to_prompt(messages)
            
            response = self.provider_manager.generate_response(
                prompt=prompt,
                provider=self.provider,
                model=self.model,
                **{**self.config, **kwargs}
            )
            
            return response.get('content', '') if isinstance(response, dict) else str(response)
            
        except Exception as e:
            logger.error(f"Error calling {self.provider} provider: {e}")
            raise
    
    def _messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """Convert CrewAI message format to simple prompt."""
        prompt_parts = []
        for msg in messages:
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            if role == 'system':
                prompt_parts.append(f"System: {content}")
            elif role == 'user':
                prompt_parts.append(f"Human: {content}")
            elif role == 'assistant':
                prompt_parts.append(f"Assistant: {content}")
        return "\n\n".join(prompt_parts)

class MultiProviderCrewManager:
    """Manages CrewAI crews with multiple LLM providers."""
    
    def __init__(self, provider_manager):
        self.provider_manager = provider_manager
        self._validate_provider_manager()
    
    def _validate_provider_manager(self):
        """Ensure provider manager has required methods."""
        required_methods = ['generate_response', 'get_available_providers']
        for method in required_methods:
            if not hasattr(self.provider_manager, method):
                raise ValueError(f"Provider manager missing required method: {method}")
    
    def create_agent(self, config: AgentConfig) -> Agent:
        """Create a CrewAI agent with specified provider."""
        if not self._is_provider_available(config.provider):
            raise ValueError(f"Provider '{config.provider}' not available")
        
        # Create LLM wrapper for the specified provider
        llm = ProviderLLMWrapper(
            provider_manager=self.provider_manager,
            provider=config.provider,
            model=config.model,
            temperature=config.temperature,
            max_tokens=config.max_tokens
        )
        
        return Agent(
            role=config.role,
            goal=config.goal,
            backstory=config.backstory,
            llm=llm,
            verbose=config.verbose,
            allow_delegation=config.allow_delegation
        )
    
    def create_crew(self, 
                   agent_configs: List[AgentConfig], 
                   tasks: List[Dict[str, Any]],
                   process: Process = Process.sequential,
                   verbose: bool = True) -> 'MultiProviderCrew':
        """Create a crew with agents using different providers."""
        if not agent_configs:
            raise ValueError("At least one agent configuration required")
        
        if not tasks:
            raise ValueError("At least one task required")
        
        # Create agents
        agents = [self.create_agent(config) for config in agent_configs]
        
        # Create tasks
        crew_tasks = []
        for i, task_config in enumerate(tasks):
            if 'agent' not in task_config:
                # Assign to first agent if not specified
                task_config['agent'] = agents[0]
            elif isinstance(task_config['agent'], int):
                # Allow agent specification by index
                if 0 <= task_config['agent'] < len(agents):
                    task_config['agent'] = agents[task_config['agent']]
                else:
                    raise ValueError(f"Invalid agent index: {task_config['agent']}")
            
            crew_tasks.append(Task(**task_config))
        
        return MultiProviderCrew(
            agents=agents,
            tasks=crew_tasks,
            process=process,
            verbose=verbose,
            provider_manager=self.provider_manager
        )
    
    def _is_provider_available(self, provider: str) -> bool:
        """Check if provider is available."""
        try:
            available = self.provider_manager.get_available_providers()
            return provider in available
        except Exception:
            # Fallback: try common providers
            return provider.lower() in ['claude', 'openai', 'bedrock']
    
    def get_provider_info(self) -> Dict[str, Any]:
        """Get information about available providers."""
        try:
            return {
                'available_providers': self.provider_manager.get_available_providers(),
                'default_models': {
                    'claude': 'claude-3-sonnet-20240229',
                    'openai': 'gpt-4',
                    'bedrock': 'anthropic.claude-3-sonnet-20240229-v1:0'
                }
            }
        except Exception as e:
            logger.warning(f"Could not get provider info: {e}")
            return {'available_providers': [], 'default_models': {}}

class MultiProviderCrew(Crew):
    """Extended Crew class with provider management capabilities."""
    
    def __init__(self, *args, provider_manager=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.provider_manager = provider_manager
    
    def kickoff(self, inputs: Optional[Dict[str, Any]] = None) -> str:
        """Execute the crew with enhanced error handling."""
        try:
            logger.info(f"Starting crew execution with {len(self.agents)} agents")
            result = super().kickoff(inputs)
            logger.info("Crew execution completed successfully")
            return result
        except Exception as e:
            logger.error(f"Crew execution failed: {e}")
            raise
    
    def get_agent_providers(self) -> Dict[str, str]:
        """Get provider information for each agent."""
        providers = {}
        for i, agent in enumerate(self.agents):
            if hasattr(agent, 'llm') and hasattr(agent.llm, 'provider'):
                providers[f"agent_{i}_{agent.role}"] = agent.llm.provider
        return providers

# Convenience functions
def create_mixed_analysis_crew(provider_manager, 
                             analyst_provider: str = "claude",
                             writer_provider: str = "openai") -> MultiProviderCrew:
    """Create a pre-configured crew for analysis and writing tasks."""
    
    manager = MultiProviderCrewManager(provider_manager)
    
    agent_configs = [
        AgentConfig(
            role="Senior Data Analyst",
            goal="Analyze data and extract meaningful insights",
            backstory="You are an experienced data analyst with expertise in finding patterns and trends in complex datasets.",
            provider=analyst_provider,
            model="claude-3-sonnet-20240229" if analyst_provider == "claude" else "gpt-4",
            temperature=0.3
        ),
        AgentConfig(
            role="Technical Writer",
            goal="Create clear, engaging reports from analysis results",
            backstory="You are a skilled technical writer who excels at translating complex analysis into accessible reports.",
            provider=writer_provider,
            model="gpt-4" if writer_provider == "openai" else "claude-3-sonnet-20240229",
            temperature=0.7
        )
    ]
    
    tasks = [
        {
            "description": "Analyze the provided data and identify key insights, trends, and patterns. Focus on actionable findings.",
            "agent": 0,  # Data Analyst
            "expected_output": "A detailed analysis report with key findings and recommendations"
        },
        {
            "description": "Transform the analysis results into a clear, executive-friendly report with visualizations suggestions.",
            "agent": 1,  # Technical Writer
            "expected_output": "A polished report suitable for stakeholders"
        }
    ]
    
    return manager.create_crew(agent_configs, tasks)