from crewai import Task
from agents.specialist_agents import SpecialistAgentFactory
from typing import List, Dict

class ReviewTaskFactory:
    """Factory for creating specialized review tasks"""
    
    def __init__(self):
        self.agents = SpecialistAgentFactory.create_all_agents()
    
    def create_security_task(self, code_content: str, file_paths: List[str]) -> Task:
        return Task(
            description=f"""
            Perform a comprehensive security review of the provided code:
            Files: {', '.join(file_paths)}
            
            Code to review:
            {code_content}
            
            Focus on:
            - Input validation and sanitization
            - Authentication and authorization flaws
            - SQL injection and XSS vulnerabilities
            - Insecure data handling
            - Cryptographic issues
            
            Provide findings with severity levels and specific recommendations.
            """,
            agent=self.agents["security"],
            expected_output="Detailed security analysis with findings, severity levels, and recommendations"
        )
    
    def create_performance_task(self, code_content: str, file_paths: List[str]) -> Task:
        return Task(
            description=f"""
            Analyze the code for performance issues and optimization opportunities:
            Files: {', '.join(file_paths)}
            
            Code to review:
            {code_content}
            
            Focus on:
            - Algorithmic complexity (Big O analysis)
            - Memory usage and leaks
            - Database query optimization
            - Caching opportunities
            - Resource management
            
            Provide specific performance recommendations with impact assessment.
            """,
            agent=self.agents["performance"],
            expected_output="Performance analysis with bottlenecks identified and optimization suggestions"
        )
    
    def create_architecture_task(self, code_content: str, file_paths: List[str]) -> Task:
        return Task(
            description=f"""
            Review the code architecture and design patterns:
            Files: {', '.join(file_paths)}
            
            Code to review:
            {code_content}
            
            Focus on:
            - SOLID principles adherence
            - Design pattern usage
            - Code organization and modularity
            - Separation of concerns
            - Maintainability and extensibility
            
            Provide architectural recommendations for improvement.
            """,
            agent=self.agents["architecture"],
            expected_output="Architectural analysis with design recommendations and refactoring suggestions"
        )
    
    def create_testing_task(self, code_content: str, file_paths: List[str]) -> Task:
        return Task(
            description=f"""
            Evaluate testing practices and coverage:
            Files: {', '.join(file_paths)}
            
            Code to review:
            {code_content}
            
            Focus on:
            - Test coverage analysis
            - Test quality and effectiveness
            - Testing best practices
            - Missing test scenarios
            - Test maintainability
            
            Provide testing recommendations and suggest additional test cases.
            """,
            agent=self.agents["testing"],
            expected_output="Testing analysis with coverage assessment and test improvement recommendations"
        )