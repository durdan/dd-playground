from crewai import Task
from typing import Optional


class BaseTask:
    """Base class for creating CrewAI tasks."""
    
    def __init__(self, description: str, expected_output: str, agent=None):
        self.description = description
        self.expected_output = expected_output
        self.agent = agent
    
    def create_task(self, agent=None) -> Task:
        """Create and return a CrewAI Task instance."""
        task_agent = agent or self.agent
        if not task_agent:
            raise ValueError("Agent must be provided either in constructor or create_task method")
        
        return Task(
            description=self.description,
            expected_output=self.expected_output,
            agent=task_agent
        )


class ResearchTask(BaseTask):
    """Task for research activities."""
    
    def __init__(self, topic: str):
        super().__init__(
            description=f"Research the topic: {topic}. Gather comprehensive information from reliable sources.",
            expected_output="A detailed research report with key findings, sources, and insights."
        )


class WritingTask(BaseTask):
    """Task for writing activities."""
    
    def __init__(self, content_type: str, topic: str):
        super().__init__(
            description=f"Write a {content_type} about {topic}. Ensure it's engaging and well-structured.",
            expected_output=f"A well-written {content_type} that is informative and engaging."
        )