from crewai import Crew
from typing import List
from agents.base_agent import BaseAgent
from tasks.base_task import BaseTask
from config.settings import config


class BaseCrew:
    """Base class for creating and managing CrewAI crews."""
    
    def __init__(self, agents: List[BaseAgent], tasks: List[BaseTask]):
        self.agents = [agent.create_agent() for agent in agents]
        self.tasks = []
        
        # Create tasks and assign agents
        for i, task in enumerate(tasks):
            agent = self.agents[i % len(self.agents)]  # Round-robin assignment
            self.tasks.append(task.create_task(agent))
    
    def create_crew(self) -> Crew:
        """Create and return a CrewAI Crew instance."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=config.log_level == "DEBUG"
        )
    
    def kickoff(self):
        """Execute the crew's tasks."""
        crew = self.create_crew()
        return crew.kickoff()


class ContentCreationCrew(BaseCrew):
    """Specialized crew for content creation tasks."""
    
    def __init__(self, topic: str):
        from agents.base_agent import ResearchAgent, WriterAgent
        from tasks.base_task import ResearchTask, WritingTask
        
        agents = [ResearchAgent(), WriterAgent()]
        tasks = [
            ResearchTask(topic),
            WritingTask("article", topic)
        ]
        
        super().__init__(agents, tasks)