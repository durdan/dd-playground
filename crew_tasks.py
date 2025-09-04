from crewai import Task
from typing import Dict, Any

class TestCrewTasks:
    """CrewAI tasks for test generation workflow"""
    
    @staticmethod
    def create_planning_task(code_analysis: Dict[str, Any]) -> Task:
        return Task(
            description=f"""
            Analyze the provided code and create a comprehensive test plan.
            
            Code Analysis:
            - Functions: {code_analysis.get('functions', [])}
            - Classes: {code_analysis.get('classes', [])}
            - Complexity Score: {code_analysis.get('complexity_score', 0)}
            
            Create a test plan that includes:
            1. Test categories (unit, integration, edge cases)
            2. Priority levels for each test
            3. Coverage targets
            4. Special testing considerations
            
            Output should be a structured test plan.
            """,
            expected_output="Detailed test plan with categorized test scenarios and priorities"
        )
    
    @staticmethod
    def create_writing_task(test_plan: str) -> Task:
        return Task(
            description=f"""
            Based on the test plan, write comprehensive test code using pytest.
            
            Test Plan:
            {test_plan}
            
            Requirements:
            1. Use pytest framework
            2. Include fixtures where appropriate
            3. Write clear, descriptive test names
            4. Add docstrings explaining test purpose
            5. Include both positive and negative test cases
            6. Use proper assertions
            
            Generate complete, runnable test code.
            """,
            expected_output="Complete pytest test suite with proper structure and coverage"
        )
    
    @staticmethod
    def create_review_task(test_code: str) -> Task:
        return Task(
            description=f"""
            Review the generated test code for quality and completeness.
            
            Test Code to Review:
            {test_code}
            
            Review Criteria:
            1. Code quality and readability
            2. Test coverage completeness
            3. Proper use of testing patterns
            4. Edge case coverage
            5. Maintainability
            
            Provide feedback and improved version if needed.
            """,
            expected_output="Quality review with feedback and improved test code if necessary"
        )