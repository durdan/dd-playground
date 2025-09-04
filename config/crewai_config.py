"""CrewAI-specific configuration management."""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class CrewAIAgentConfig:
    """Configuration for a CrewAI agent."""
    role: str
    goal: str
    backstory: Optional[str] = None
    verbose: bool = True
    allow_delegation: bool = False


@dataclass
class CrewAIConfig:
    """CrewAI configuration settings."""
    enabled: bool
    default_llm_provider: str
    agent_verbose: bool
    task_verbose: bool
    crew_verbose: bool
    max_execution_time: int
    max_retry_attempts: int
    
    # Agent configurations
    researcher_config: CrewAIAgentConfig
    writer_config: CrewAIAgentConfig
    
    @classmethod
    def from_env(cls) -> 'CrewAIConfig':
        """Create CrewAI configuration from environment variables."""
        return cls(
            enabled=os.getenv('CREWAI_ENABLED', 'false').lower() == 'true',
            default_llm_provider=os.getenv('CREWAI_DEFAULT_LLM_PROVIDER', 'openai'),
            agent_verbose=os.getenv('CREWAI_AGENT_VERBOSE', 'true').lower() == 'true',
            task_verbose=os.getenv('CREWAI_TASK_VERBOSE', 'true').lower() == 'true',
            crew_verbose=os.getenv('CREWAI_CREW_VERBOSE', 'true').lower() == 'true',
            max_execution_time=int(os.getenv('CREWAI_MAX_EXECUTION_TIME', '300')),
            max_retry_attempts=int(os.getenv('CREWAI_MAX_RETRY_ATTEMPTS', '3')),
            researcher_config=CrewAIAgentConfig(
                role=os.getenv('CREWAI_RESEARCHER_ROLE', 'Senior Research Analyst'),
                goal=os.getenv('CREWAI_RESEARCHER_GOAL', 'Uncover cutting-edge developments in AI and data science'),
                backstory=os.getenv('CREWAI_RESEARCHER_BACKSTORY'),
                verbose=os.getenv('CREWAI_AGENT_VERBOSE', 'true').lower() == 'true'
            ),
            writer_config=CrewAIAgentConfig(
                role=os.getenv('CREWAI_WRITER_ROLE', 'Tech Content Strategist'),
                goal=os.getenv('CREWAI_WRITER_GOAL', 'Craft compelling content on tech advancements'),
                backstory=os.getenv('CREWAI_WRITER_BACKSTORY'),
                verbose=os.getenv('CREWAI_AGENT_VERBOSE', 'true').lower() == 'true'
            )
        )
    
    def validate(self) -> None:
        """Validate CrewAI configuration."""
        if self.enabled:
            if self.default_llm_provider not in ['openai', 'anthropic']:
                raise ValueError(f"Invalid CrewAI LLM provider: {self.default_llm_provider}")
            
            if self.max_execution_time <= 0:
                raise ValueError("CrewAI max execution time must be positive")
            
            if self.max_retry_attempts < 0:
                raise ValueError("CrewAI max retry attempts cannot be negative")
            
            if not self.researcher_config.role.strip():
                raise ValueError("CrewAI researcher role cannot be empty")
            
            if not self.writer_config.role.strip():
                raise ValueError("CrewAI writer role cannot be empty")