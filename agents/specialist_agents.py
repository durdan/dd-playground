from crewai import Agent
from typing import Dict, Any

class SpecialistAgentFactory:
    """Factory for creating specialized code review agents"""
    
    @staticmethod
    def create_security_agent() -> Agent:
        return Agent(
            role="Security Code Reviewer",
            goal="Identify security vulnerabilities and potential threats in code",
            backstory="""You are a cybersecurity expert with deep knowledge of common 
            vulnerabilities like OWASP Top 10, injection attacks, authentication flaws, 
            and secure coding practices.""",
            verbose=True,
            allow_delegation=False
        )
    
    @staticmethod
    def create_performance_agent() -> Agent:
        return Agent(
            role="Performance Code Reviewer",
            goal="Analyze code for performance bottlenecks and optimization opportunities",
            backstory="""You are a performance optimization specialist who understands 
            algorithmic complexity, memory usage, database queries, and system scalability.""",
            verbose=True,
            allow_delegation=False
        )
    
    @staticmethod
    def create_architecture_agent() -> Agent:
        return Agent(
            role="Architecture Code Reviewer",
            goal="Evaluate code structure, design patterns, and architectural decisions",
            backstory="""You are a software architect with expertise in design patterns, 
            SOLID principles, clean code, and system design best practices.""",
            verbose=True,
            allow_delegation=False
        )
    
    @staticmethod
    def create_testing_agent() -> Agent:
        return Agent(
            role="Testing Code Reviewer",
            goal="Assess test coverage, quality, and testing best practices",
            backstory="""You are a QA engineer and testing expert who understands unit testing, 
            integration testing, test-driven development, and testing frameworks.""",
            verbose=True,
            allow_delegation=False
        )
    
    @classmethod
    def create_all_agents(cls) -> Dict[str, Agent]:
        return {
            "security": cls.create_security_agent(),
            "performance": cls.create_performance_agent(),
            "architecture": cls.create_architecture_agent(),
            "testing": cls.create_testing_agent()
        }