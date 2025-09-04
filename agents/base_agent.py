from crewai import Agent
from config.settings import config


class BaseAgent:
    """Base class for creating CrewAI agents with common configuration."""
    
    def __init__(self, role: str, goal: str, backstory: str, **kwargs):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.kwargs = kwargs
    
    def create_agent(self) -> Agent:
        """Create and return a CrewAI Agent instance."""
        return Agent(
            role=self.role,
            goal=self.goal,
            backstory=self.backstory,
            verbose=config.log_level == "DEBUG",
            **self.kwargs
        )


class ResearchAgent(BaseAgent):
    """Agent specialized in research tasks."""
    
    def __init__(self):
        super().__init__(
            role="Research Specialist",
            goal="Conduct thorough research and provide accurate information",
            backstory="You are an expert researcher with years of experience in gathering and analyzing information from various sources."
        )


class WriterAgent(BaseAgent):
    """Agent specialized in writing tasks."""
    
    def __init__(self):
        super().__init__(
            role="Content Writer",
            goal="Create engaging and well-structured written content",
            backstory="You are a skilled writer who can adapt your writing style to different audiences and purposes."
        )