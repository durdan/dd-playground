from crewai import Agent
from typing import List

class CodeReviewAgents:
    @staticmethod
    def security_agent() -> Agent:
        return Agent(
            role="Security Code Reviewer",
            goal="Identify security vulnerabilities and potential threats in code",
            backstory="""You are an expert security engineer with deep knowledge of 
            common vulnerabilities like OWASP Top 10, injection attacks, authentication 
            flaws, and secure coding practices.""",
            verbose=True,
            allow_delegation=False
        )
    
    @staticmethod
    def quality_agent() -> Agent:
        return Agent(
            role="Code Quality Reviewer",
            goal="Assess code quality, maintainability, and adherence to best practices",
            backstory="""You are a senior software engineer focused on clean code, 
            design patterns, SOLID principles, and maintainable architecture. You 
            identify code smells and suggest improvements.""",
            verbose=True,
            allow_delegation=False
        )
    
    @staticmethod
    def performance_agent() -> Agent:
        return Agent(
            role="Performance Code Reviewer",
            goal="Identify performance bottlenecks and optimization opportunities",
            backstory="""You are a performance optimization expert who identifies 
            inefficient algorithms, memory leaks, database query issues, and 
            scalability problems.""",
            verbose=True,
            allow_delegation=False
        )