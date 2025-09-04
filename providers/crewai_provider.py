"""CrewAI provider implementation."""

from typing import Dict, Any, Optional, List
from dataclasses import asdict

try:
    from crewai import Agent, Task, Crew
    from crewai.llm import LLM
    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False

from .base_provider import BaseProvider
from .openai_provider import OpenAIProvider
from .anthropic_provider import AnthropicProvider


class CrewAIProvider(BaseProvider):
    """CrewAI provider for multi-agent workflows."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize CrewAI provider with configuration."""
        if not CREWAI_AVAILABLE:
            raise ImportError("CrewAI is not installed. Install with: pip install crewai")
        
        super().__init__(config)
        
        # Get underlying LLM provider
        llm_provider = config['llm_provider']
        llm_config = config['llm_config']
        
        if llm_provider == 'openai':
            self.llm_provider = OpenAIProvider(llm_config)
        elif llm_provider == 'anthropic':
            self.llm_provider = AnthropicProvider(llm_config)
        else:
            raise ValueError(f"Unsupported LLM provider for CrewAI: {llm_provider}")
        
        # Store CrewAI-specific config
        self.agent_verbose = config.get('agent_verbose', True)
        self.task_verbose = config.get('task_verbose', True)
        self.crew_verbose = config.get('crew_verbose', True)
        self.max_execution_time = config.get('max_execution_time', 300)
        self.max_retry_attempts = config.get('max_retry_attempts', 3)
        self.researcher_config = config.get('researcher_config')
        self.writer_config = config.get('writer_config')
    
    def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate response using CrewAI multi-agent workflow."""
        try:
            # Create LLM instance for CrewAI
            llm = self._create_crewai_llm()
            
            # Create agents
            researcher = self._create_researcher_agent(llm)
            writer = self._create_writer_agent(llm)
            
            # Create tasks
            research_task = Task(
                description=f"Research the following topic thoroughly: {prompt}",
                agent=researcher,
                expected_output="A comprehensive research report with key findings and insights"
            )
            
            writing_task = Task(
                description="Based on the research findings, create a well-structured and engaging response",
                agent=writer,
                expected_output="A clear, well-written response that addresses the original query",
                context=[research_task]
            )
            
            # Create and execute crew
            crew = Crew(
                agents=[researcher, writer],
                tasks=[research_task, writing_task],
                verbose=self.crew_verbose,
                max_execution_time=self.max_execution_time,
                max_retry_limit=self.max_retry_attempts
            )
            
            result = crew.kickoff()
            return str(result)
            
        except Exception as e:
            raise RuntimeError(f"CrewAI generation failed: {str(e)}")
    
    def _create_crewai_llm(self):
        """Create LLM instance for CrewAI based on the underlying provider."""
        llm_config = self.config['llm_config']
        
        if self.config['llm_provider'] == 'openai':
            return LLM(
                model=f"openai/{llm_config['model']}",
                api_key=llm_config['api_key'],
                temperature=llm_config.get('temperature', 0.7),
                max_tokens=llm_config.get('max_tokens', 2000)
            )
        elif self.config['llm_provider'] == 'anthropic':
            return LLM(
                model=f"anthropic/{llm_config['model']}",
                api_key=llm_config['api_key'],
                temperature=llm_config.get('temperature', 0.7),
                max_tokens=llm_config.get('max_tokens', 2000)
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {self.config['llm_provider']}")
    
    def _create_researcher_agent(self, llm) -> Agent:
        """Create researcher agent."""
        config = self.researcher_config
        return Agent(
            role=config.role,
            goal=config.goal,
            backstory=config.backstory or f"You are a {config.role} with deep expertise in research and analysis.",
            verbose=config.verbose,
            allow_delegation=config.allow_delegation,
            llm=llm
        )
    
    def _create_writer_agent(self, llm) -> Agent:
        """Create writer agent."""
        config = self.writer_config
        return Agent(
            role=config.role,
            goal=config.goal,
            backstory=config.backstory or f"You are a {config.role} skilled in creating engaging content.",
            verbose=config.verbose,
            allow_delegation=config.allow_delegation,
            llm=llm
        )
    
    def validate_config(self) -> None:
        """Validate CrewAI provider configuration."""
        required_fields = ['llm_provider', 'llm_config', 'researcher_config', 'writer_config']
        for field in required_fields:
            if field not in self.config:
                raise ValueError(f"Missing required CrewAI config field: {field}")
        
        # Validate underlying LLM provider config
        self.llm_provider.validate_config()