from crewai import Crew, Process
from tasks import ReviewTasks
from agents import CodeReviewAgents
from models import CodeReviewRequest, ReviewType
from typing import List

class CodeReviewCrew:
    def __init__(self):
        self.agents = {
            ReviewType.SECURITY: CodeReviewAgents.security_agent(),
            ReviewType.QUALITY: CodeReviewAgents.quality_agent(),
            ReviewType.PERFORMANCE: CodeReviewAgents.performance_agent()
        }
    
    def create_crew(self, request: CodeReviewRequest) -> Crew:
        tasks = []
        agents = []
        
        for review_type in request.review_types:
            if review_type == ReviewType.SECURITY:
                task = ReviewTasks.create_security_task(request.code_content, request.file_path)
                tasks.append(task)
                agents.append(self.agents[ReviewType.SECURITY])
            elif review_type == ReviewType.QUALITY:
                task = ReviewTasks.create_quality_task(request.code_content, request.file_path)
                tasks.append(task)
                agents.append(self.agents[ReviewType.QUALITY])
            elif review_type == ReviewType.PERFORMANCE:
                task = ReviewTasks.create_performance_task(request.code_content, request.file_path)
                tasks.append(task)
                agents.append(self.agents[ReviewType.PERFORMANCE])
        
        if not tasks:
            raise ValueError("No valid review types specified")
        
        return Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )