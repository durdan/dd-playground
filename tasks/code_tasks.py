from crewai import Task
from typing import Dict, Any

class CodeGenerationTasks:
    @staticmethod
    def create_architecture_task(agent, requirements: str) -> Task:
        return Task(
            description=f"""
            Analyze the following requirements and create a detailed software architecture:
            
            Requirements: {requirements}
            
            Your output should include:
            1. High-level architecture overview
            2. Component breakdown with responsibilities
            3. Interface definitions
            4. Data flow and dependencies
            5. Technology stack recommendations
            6. File structure and organization
            
            Focus on maintainability, scalability, and testability.
            """,
            agent=agent,
            expected_output="Detailed architecture document with component specifications"
        )
    
    @staticmethod
    def create_implementation_task(agent, architecture: str) -> Task:
        return Task(
            description=f"""
            Based on the following architecture, implement the complete solution:
            
            Architecture: {architecture}
            
            Requirements:
            - Follow the architectural design exactly
            - Implement proper error handling and validation
            - Add comprehensive docstrings and comments
            - Follow language-specific best practices
            - Ensure code is modular and testable
            - Include configuration management where needed
            
            Provide complete, working code for all components.
            """,
            agent=agent,
            expected_output="Complete implementation with all necessary files and code"
        )
    
    @staticmethod
    def create_review_task(agent, code: str) -> Task:
        return Task(
            description=f"""
            Review the following code implementation for:
            
            Code to review: {code}
            
            Review criteria:
            1. Code quality and readability
            2. Security vulnerabilities
            3. Performance issues
            4. Error handling completeness
            5. Adherence to best practices
            6. Potential bugs or edge cases
            7. Documentation quality
            
            Provide specific feedback and improvement suggestions.
            """,
            agent=agent,
            expected_output="Detailed code review with specific improvement recommendations"
        )
    
    @staticmethod
    def create_testing_task(agent, code: str, architecture: str) -> Task:
        return Task(
            description=f"""
            Create comprehensive tests for the following implementation:
            
            Code: {code}
            Architecture: {architecture}
            
            Create:
            1. Unit tests for all functions/methods
            2. Integration tests for component interactions
            3. Edge case and error condition tests
            4. Performance tests where applicable
            5. Mock objects for external dependencies
            
            Ensure high test coverage and meaningful assertions.
            """,
            agent=agent,
            expected_output="Complete test suite with unit and integration tests"
        )