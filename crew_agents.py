from crewai import Agent, Task, Crew
from crewai.tools import tool
from models import PullRequest, ReviewResult, ReviewComment, ReviewStatus
from typing import List
import os

class PRReviewCrew:
    def __init__(self, openai_api_key: str):
        os.environ["OPENAI_API_KEY"] = openai_api_key
        self.code_reviewer = self._create_code_reviewer()
        self.security_analyst = self._create_security_analyst()
        self.automation_manager = self._create_automation_manager()
    
    def _create_code_reviewer(self) -> Agent:
        return Agent(
            role="Senior Code Reviewer",
            goal="Review code quality, best practices, and maintainability",
            backstory="You are an experienced software engineer who reviews code for quality, "
                     "readability, performance, and adherence to best practices.",
            verbose=True,
            allow_delegation=False
        )
    
    def _create_security_analyst(self) -> Agent:
        return Agent(
            role="Security Analyst",
            goal="Identify security vulnerabilities and potential risks",
            backstory="You are a cybersecurity expert who specializes in identifying "
                     "security vulnerabilities, potential exploits, and security best practices.",
            verbose=True,
            allow_delegation=False
        )
    
    def _create_automation_manager(self) -> Agent:
        return Agent(
            role="Automation Manager",
            goal="Decide on automation actions like auto-merge based on review results",
            backstory="You are responsible for making decisions about automated actions "
                     "based on code review results and repository policies.",
            verbose=True,
            allow_delegation=False
        )
    
    def review_pr(self, pr: PullRequest) -> ReviewResult:
        """Orchestrate multi-agent PR review"""
        
        # Create tasks for each agent
        code_review_task = Task(
            description=f"""
            Review the following pull request for code quality:
            
            Title: {pr.title}
            Description: {pr.body}
            Author: {pr.author}
            Files changed: {len(pr.files)}
            
            Files and changes:
            {self._format_files_for_review(pr.files)}
            
            Provide specific feedback on:
            1. Code quality and readability
            2. Best practices adherence
            3. Potential bugs or issues
            4. Performance considerations
            
            Format your response as structured feedback with specific line references where applicable.
            """,
            agent=self.code_reviewer,
            expected_output="Detailed code review with specific feedback and suggestions"
        )
        
        security_review_task = Task(
            description=f"""
            Analyze the following pull request for security issues:
            
            Title: {pr.title}
            Files and changes:
            {self._format_files_for_review(pr.files)}
            
            Look for:
            1. Security vulnerabilities
            2. Potential data leaks
            3. Authentication/authorization issues
            4. Input validation problems
            5. Dependency security issues
            
            Provide specific security recommendations.
            """,
            agent=self.security_analyst,
            expected_output="Security analysis with identified risks and recommendations"
        )
        
        automation_task = Task(
            description=f"""
            Based on the code review and security analysis, decide on automation actions:
            
            PR Details:
            - Author: {pr.author}
            - Files changed: {len(pr.files)}
            - Total changes: {sum(f.changes for f in pr.files)}
            
            Consider:
            1. Are there any critical issues that block auto-merge?
            2. Is this a low-risk change that can be auto-merged?
            3. What's the overall recommendation (approve, request changes, comment)?
            
            Provide a clear decision on auto-merge eligibility and overall status.
            """,
            agent=self.automation_manager,
            expected_output="Automation decision with clear reasoning and recommended status",
            context=[code_review_task, security_review_task]
        )
        
        # Execute the crew
        crew = Crew(
            agents=[self.code_reviewer, self.security_analyst, self.automation_manager],
            tasks=[code_review_task, security_review_task, automation_task],
            verbose=True
        )
        
        result = crew.kickoff()
        
        # Parse results and create ReviewResult
        return self._parse_crew_result(result, pr)
    
    def _format_files_for_review(self, files: List) -> str:
        """Format file changes for agent review"""
        formatted = []
        for file in files[:10]:  # Limit to first 10 files to avoid token limits
            formatted.append(f"""
File: {file.filename}
Status: {file.status}
Changes: +{file.additions} -{file.deletions}
Patch preview:
{file.patch[:500]}...
""")
        return "\n".join(formatted)
    
    def _parse_crew_result(self, crew_result: str, pr: PullRequest) -> ReviewResult:
        """Parse crew execution result into ReviewResult"""
        # Simple parsing - in production, you'd want more sophisticated parsing
        result_lower = crew_result.lower()
        
        # Determine status based on keywords
        if "critical" in result_lower or "security risk" in result_lower:
            status = ReviewStatus.CHANGES_REQUESTED
            auto_merge = False
        elif "approve" in result_lower and "low risk" in result_lower:
            status = ReviewStatus.APPROVED
            auto_merge = True
        elif "approve" in result_lower:
            status = ReviewStatus.APPROVED
            auto_merge = False
        else:
            status = ReviewStatus.COMMENTED
            auto_merge = False
        
        # Create summary and comments
        summary = f"Multi-agent review completed for PR #{pr.number}"
        comments = [
            ReviewComment(body=crew_result)
        ]
        
        return ReviewResult(
            status=status,
            summary=summary,
            comments=comments,
            auto_merge=auto_merge
        )