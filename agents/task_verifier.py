from agents.base_agent import BaseAgent
from models import TaskRequest, AgentResponse, AgentRole, TaskStatus

class TaskVerifier(BaseAgent):
    def __init__(self):
        super().__init__(AgentRole.TASK_VERIFIER)
    
    def process(self, request: TaskRequest) -> AgentResponse:
        """Verify task completeness and feasibility"""
        errors = []
        suggestions = []
        
        # Basic validation
        if not request.description.strip():
            errors.append("Task description cannot be empty")
        
        if len(request.description) < 10:
            errors.append("Task description too brief, needs more detail")
        
        # Check for common requirements
        if not request.requirements:
            suggestions.append("Consider adding specific requirements for better clarity")
        
        # Analyze complexity
        complexity_score = self._assess_complexity(request)
        
        if errors:
            return self._create_response(
                TaskStatus.FAILED,
                {"complexity_score": complexity_score},
                errors=errors
            )
        
        feedback = [f"Task verified successfully with complexity score: {complexity_score}"]
        
        return self._create_response(
            TaskStatus.COMPLETED,
            {
                "is_valid": True,
                "complexity_score": complexity_score,
                "estimated_effort": self._estimate_effort(complexity_score)
            },
            feedback=feedback,
            suggestions=suggestions
        )
    
    def _assess_complexity(self, request: TaskRequest) -> int:
        """Simple complexity assessment (1-10 scale)"""
        score = 1
        
        # Factor in description length and keywords
        if len(request.description) > 100:
            score += 1
        if len(request.requirements) > 3:
            score += 1
        if any(keyword in request.description.lower() 
               for keyword in ['complex', 'integration', 'database', 'api']):
            score += 2
        
        return min(score, 10)
    
    def _estimate_effort(self, complexity_score: int) -> str:
        """Estimate effort based on complexity"""
        if complexity_score <= 3:
            return "Low"
        elif complexity_score <= 6:
            return "Medium"
        else:
            return "High"