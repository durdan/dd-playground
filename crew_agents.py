from crewai import Agent, Task, Crew
from typing import List
from models import PullRequest, ReviewResult
from config import CrewConfig

class PRReviewAgents:
    def __init__(self, config: CrewConfig):
        self.config = config
        self._setup_agents()
    
    def _setup_agents(self):
        """Initialize specialized review agents."""
        self.code_quality_agent = Agent(
            role='Code Quality Reviewer',
            goal='Analyze code quality, maintainability, and best practices',
            backstory='Expert in clean code principles, design patterns, and maintainability',
            verbose=True,
            allow_delegation=False
        )
        
        self.security_agent = Agent(
            role='Security Reviewer',
            goal='Identify security vulnerabilities and potential risks',
            backstory='Cybersecurity expert specializing in secure coding practices',
            verbose=True,
            allow_delegation=False
        )
        
        self.performance_agent = Agent(
            role='Performance Reviewer',
            goal='Analyze performance implications and optimization opportunities',
            backstory='Performance optimization expert with deep system knowledge',
            verbose=True,
            allow_delegation=False
        )
        
        self.documentation_agent = Agent(
            role='Documentation Reviewer',
            goal='Ensure proper documentation and code clarity',
            backstory='Technical writer focused on code documentation and clarity',
            verbose=True,
            allow_delegation=False
        )
    
    def review_pull_request(self, pr: PullRequest) -> List[ReviewResult]:
        """Coordinate multi-agent PR review."""
        results = []
        
        # Prepare context for agents
        context = self._prepare_context(pr)
        
        # Create tasks for each agent
        tasks = [
            self._create_code_quality_task(context),
            self._create_security_task(context),
            self._create_performance_task(context),
            self._create_documentation_task(context)
        ]
        
        # Create and run crew
        crew = Crew(
            agents=[
                self.code_quality_agent,
                self.security_agent,
                self.performance_agent,
                self.documentation_agent
            ],
            tasks=tasks,
            verbose=True
        )
        
        crew_results = crew.kickoff()
        
        # Parse results from each agent
        results.extend(self._parse_crew_results(crew_results))
        
        return results
    
    def _prepare_context(self, pr: PullRequest) -> str:
        """Prepare context string for agents."""
        files_summary = "\n".join([
            f"- {f.filename}: +{f.additions}/-{f.deletions} ({f.status})"
            for f in pr.files
        ])
        
        patches = "\n\n".join([
            f"=== {f.filename} ===\n{f.patch}"
            for f in pr.files if f.patch
        ])
        
        return f"""
Pull Request: {pr.title}
Author: {pr.author}
Branch: {pr.head_branch} -> {pr.base_branch}
Description: {pr.description}

Files Changed:
{files_summary}

Code Changes:
{patches}
        """.strip()
    
    def _create_code_quality_task(self, context: str) -> Task:
        return Task(
            description=f"""
            Review the following pull request for code quality:
            
            {context}
            
            Analyze:
            1. Code structure and organization
            2. Naming conventions
            3. Code duplication
            4. Design patterns usage
            5. Maintainability
            
            Provide a score (1-10) and specific feedback.
            """,
            agent=self.code_quality_agent
        )
    
    def _create_security_task(self, context: str) -> Task:
        return Task(
            description=f"""
            Review the following pull request for security issues:
            
            {context}
            
            Check for:
            1. Input validation
            2. Authentication/authorization
            3. Data exposure risks
            4. Injection vulnerabilities
            5. Cryptographic issues
            
            Provide a score (1-10) and security recommendations.
            """,
            agent=self.security_agent
        )
    
    def _create_performance_task(self, context: str) -> Task:
        return Task(
            description=f"""
            Review the following pull request for performance:
            
            {context}
            
            Evaluate:
            1. Algorithm efficiency
            2. Resource usage
            3. Database queries
            4. Memory management
            5. Scalability concerns
            
            Provide a score (1-10) and optimization suggestions.
            """,
            agent=self.performance_agent
        )
    
    def _create_documentation_task(self, context: str) -> Task:
        return Task(
            description=f"""
            Review the following pull request for documentation:
            
            {context}
            
            Check:
            1. Code comments
            2. Function/class documentation
            3. README updates
            4. API documentation
            5. Code clarity
            
            Provide a score (1-10) and documentation improvements.
            """,
            agent=self.documentation_agent
        )
    
    def _parse_crew_results(self, crew_results) -> List[ReviewResult]:
        """Parse crew results into ReviewResult objects."""
        # This is a simplified parser - in practice, you'd need more sophisticated parsing
        results = []
        agent_names = ['Code Quality', 'Security', 'Performance', 'Documentation']
        
        for i, result in enumerate(crew_results):
            # Extract score, comments, etc. from result text
            # This would need more sophisticated parsing in practice
            score = self._extract_score(str(result))
            comments = self._extract_comments(str(result))
            
            results.append(ReviewResult(
                agent_name=agent_names[i] if i < len(agent_names) else f"Agent {i}",
                score=score,
                comments=comments,
                suggestions=[],
                issues=[]
            ))
        
        return results
    
    def _extract_score(self, text: str) -> float:
        """Extract numerical score from agent response."""
        import re
        score_match = re.search(r'score[:\s]*(\d+(?:\.\d+)?)', text.lower())
        return float(score_match.group(1)) if score_match else 5.0
    
    def _extract_comments(self, text: str) -> List[str]:
        """Extract comments from agent response."""
        # Simple extraction - split by lines and filter
        lines = text.split('\n')
        comments = [line.strip() for line in lines if line.strip() and not line.startswith('=')]
        return comments[:5]  # Limit to top 5 comments