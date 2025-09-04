from crewai import Crew
from tasks.review_tasks import ReviewTaskFactory
from models.review_models import CodeReviewResult, SpecialistReview, Finding, ReviewType, Severity
from typing import List, Dict
import re

class ReviewOrchestrator:
    """Orchestrates multi-specialist code reviews using CrewAI"""
    
    def __init__(self):
        self.task_factory = ReviewTaskFactory()
    
    def conduct_review(self, file_paths: List[str], code_content: str) -> CodeReviewResult:
        """Conduct a comprehensive multi-specialist code review"""
        if not file_paths:
            raise ValueError("At least one file path must be provided")
        if not code_content.strip():
            raise ValueError("Code content cannot be empty")
        
        # Create tasks for each specialist
        tasks = [
            self.task_factory.create_security_task(code_content, file_paths),
            self.task_factory.create_performance_task(code_content, file_paths),
            self.task_factory.create_architecture_task(code_content, file_paths),
            self.task_factory.create_testing_task(code_content, file_paths)
        ]
        
        # Create and execute crew
        crew = Crew(
            agents=list(self.task_factory.agents.values()),
            tasks=tasks,
            verbose=True
        )
        
        result = crew.kickoff()
        
        # Parse results and create structured output
        return self._parse_crew_results(result, file_paths)
    
    def _parse_crew_results(self, crew_result, file_paths: List[str]) -> CodeReviewResult:
        """Parse CrewAI results into structured review format"""
        # This is a simplified parser - in practice, you'd need more sophisticated parsing
        specialist_reviews = []
        all_findings = []
        
        # Mock parsing logic - replace with actual result parsing
        review_types = [ReviewType.SECURITY, ReviewType.PERFORMANCE, ReviewType.ARCHITECTURE, ReviewType.TESTING]
        
        for i, review_type in enumerate(review_types):
            findings = self._extract_findings_from_result(str(crew_result), review_type)
            all_findings.extend(findings)
            
            specialist_review = SpecialistReview(
                specialist_type=review_type,
                findings=findings,
                overall_score=self._calculate_score(findings),
                summary=f"{review_type.value.title()} review completed with {len(findings)} findings"
            )
            specialist_reviews.append(specialist_review)
        
        critical_issues = [f for f in all_findings if f.severity == Severity.CRITICAL]
        overall_score = self._calculate_overall_score(specialist_reviews)
        recommendations = self._generate_recommendations(specialist_reviews)
        
        return CodeReviewResult(
            file_paths=file_paths,
            specialist_reviews=specialist_reviews,
            overall_score=overall_score,
            critical_issues=critical_issues,
            recommendations=recommendations
        )
    
    def _extract_findings_from_result(self, result_text: str, review_type: ReviewType) -> List[Finding]:
        """Extract findings from crew result text"""
        # Simplified extraction - implement proper parsing based on your output format
        findings = []
        
        # Mock findings for demonstration
        if "security" in result_text.lower():
            findings.append(Finding(
                severity=Severity.HIGH,
                category="Input Validation",
                message="Potential SQL injection vulnerability detected",
                suggestion="Use parameterized queries"
            ))
        
        return findings
    
    def _calculate_score(self, findings: List[Finding]) -> int:
        """Calculate score based on findings severity"""
        if not findings:
            return 10
        
        severity_weights = {
            Severity.LOW: 1,
            Severity.MEDIUM: 2,
            Severity.HIGH: 4,
            Severity.CRITICAL: 8
        }
        
        total_weight = sum(severity_weights[f.severity] for f in findings)
        # Simple scoring logic - adjust as needed
        score = max(1, 10 - min(9, total_weight))
        return score
    
    def _calculate_overall_score(self, reviews: List[SpecialistReview]) -> int:
        """Calculate overall score from specialist reviews"""
        if not reviews:
            return 0
        return sum(r.overall_score for r in reviews) // len(reviews)
    
    def _generate_recommendations(self, reviews: List[SpecialistReview]) -> List[str]:
        """Generate high-level recommendations"""
        recommendations = []
        
        for review in reviews:
            if review.overall_score < 7:
                recommendations.append(f"Address {review.specialist_type.value} concerns - score: {review.overall_score}/10")
        
        if not recommendations:
            recommendations.append("Code quality is good overall - continue following best practices")
        
        return recommendations