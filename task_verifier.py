from models import Task, ValidationResult, VerificationReport, ValidationStatus
from architect_agent import ArchitectAgent
from guardrail_agent import GuardrailAgent
from typing import List

class TaskVerifier:
    def __init__(self):
        self.architect_agent = ArchitectAgent()
        self.guardrail_agent = GuardrailAgent()
    
    def verify_task(self, task: Task) -> VerificationReport:
        """Main verification method combining all agents"""
        if not self._basic_validation(task):
            return VerificationReport(
                task_id=task.id,
                overall_status=ValidationStatus.FAILED,
                results=[ValidationResult(
                    agent_name="basic_validator",
                    status=ValidationStatus.FAILED,
                    message="Task failed basic validation",
                    details={"reason": "Missing required fields"}
                )],
                final_recommendations=["Provide complete task information"]
            )
        
        results = []
        
        # Architecture validation
        arch_result = self.architect_agent.validate_architecture(task)
        results.append(arch_result)
        
        # Guardrail enforcement
        guardrail_result = self.guardrail_agent.enforce_guardrails(task)
        results.append(guardrail_result)
        
        # Determine overall status
        overall_status = self._determine_overall_status(results)
        final_recommendations = self._compile_recommendations(results)
        
        return VerificationReport(
            task_id=task.id,
            overall_status=overall_status,
            results=results,
            final_recommendations=final_recommendations
        )
    
    def _basic_validation(self, task: Task) -> bool:
        """Basic task validation"""
        return (
            task.id and 
            task.title and 
            task.description and 
            task.task_type
        )
    
    def _determine_overall_status(self, results: List[ValidationResult]) -> ValidationStatus:
        """Determine overall status from individual results"""
        if any(r.status == ValidationStatus.FAILED for r in results):
            return ValidationStatus.FAILED
        elif any(r.status == ValidationStatus.WARNING for r in results):
            return ValidationStatus.WARNING
        else:
            return ValidationStatus.PASSED
    
    def _compile_recommendations(self, results: List[ValidationResult]) -> List[str]:
        """Compile all recommendations from agents"""
        recommendations = []
        for result in results:
            recommendations.extend(result.suggestions)
        return list(set(recommendations))  # Remove duplicates