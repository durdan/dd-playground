from crewai import Task
from agents import CodeReviewAgents
from models import ReviewType

class ReviewTasks:
    @staticmethod
    def create_security_task(code_content: str, file_path: str) -> Task:
        return Task(
            description=f"""
            Review the following code for security vulnerabilities:
            
            File: {file_path}
            Code:
            {code_content}
            
            Focus on:
            - Input validation and sanitization
            - Authentication and authorization flaws
            - SQL injection, XSS, CSRF vulnerabilities
            - Sensitive data exposure
            - Insecure cryptographic practices
            
            Provide specific line numbers, severity levels, and actionable suggestions.
            """,
            agent=CodeReviewAgents.security_agent(),
            expected_output="Detailed security analysis with specific issues, line numbers, and remediation suggestions"
        )
    
    @staticmethod
    def create_quality_task(code_content: str, file_path: str) -> Task:
        return Task(
            description=f"""
            Review the following code for quality and maintainability:
            
            File: {file_path}
            Code:
            {code_content}
            
            Focus on:
            - Code structure and organization
            - Naming conventions and readability
            - DRY principle violations
            - SOLID principle adherence
            - Error handling patterns
            - Documentation and comments
            
            Provide specific improvements and best practice recommendations.
            """,
            agent=CodeReviewAgents.quality_agent(),
            expected_output="Comprehensive quality assessment with improvement suggestions and best practices"
        )
    
    @staticmethod
    def create_performance_task(code_content: str, file_path: str) -> Task:
        return Task(
            description=f"""
            Review the following code for performance issues:
            
            File: {file_path}
            Code:
            {code_content}
            
            Focus on:
            - Algorithm efficiency and complexity
            - Memory usage and potential leaks
            - Database query optimization
            - Caching opportunities
            - Resource management
            - Scalability concerns
            
            Provide specific optimization recommendations with expected impact.
            """,
            agent=CodeReviewAgents.performance_agent(),
            expected_output="Performance analysis with optimization opportunities and impact estimates"
        )