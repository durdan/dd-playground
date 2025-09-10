from typing import Dict, Any, List
from .base_agent import AIAgent, AgentResponse, AgentStatus, AgentError
import re

class CodeReviewerAgent(AIAgent):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("CodeReviewerAgent", config)
        self.review_criteria = {
            "error_handling": self._check_error_handling,
            "validation": self._check_validation,
            "structure": self._check_structure,
            "completeness": self._check_completeness
        }
    
    def process(self, input_data: str, context: Dict[str, Any] = None) -> AgentResponse:
        try:
            self.validate_input(input_data)
            self.status = AgentStatus.PROCESSING
            
            context = context or {}
            content_type = context.get("content_type", "specification")
            
            # Perform review
            review_results = self._perform_review(input_data, content_type)
            
            # Generate review report
            review_report = self._generate_review_report(review_results)
            
            # Determine overall status
            has_critical_issues = any(
                result["severity"] == "critical" 
                for result in review_results
            )
            
            status = AgentStatus.ERROR if has_critical_issues else AgentStatus.COMPLETED
            errors = [
                result["message"] 
                for result in review_results 
                if result["severity"] == "critical"
            ] if has_critical_issues else None
            
            self.status = status
            return self._create_response(
                content=review_report,
                status=status,
                metadata={
                    "content_type": content_type,
                    "issues_found": len(review_results),
                    "critical_issues": len(errors) if errors else 0
                },
                errors=errors
            )
            
        except AgentError:
            raise
        except Exception as e:
            self.status = AgentStatus.ERROR
            raise AgentError(f"Failed to review content: {str(e)}", self.name)
    
    def _perform_review(self, content: str, content_type: str) -> List[Dict[str, Any]]:
        """Perform comprehensive review of content"""
        results = []
        
        for criterion, check_func in self.review_criteria.items():
            try:
                issues = check_func(content, content_type)
                results.extend(issues)
            except Exception as e:
                results.append({
                    "criterion": criterion,
                    "message": f"Review check failed: {str(e)}",
                    "severity": "warning",
                    "line": None
                })
        
        return results
    
    def _check_error_handling(self, content: str, content_type: str) -> List[Dict[str, Any]]:
        """Check for proper error handling"""
        issues = []
        
        if content_type == "specification":
            if "error" not in content.lower():
                issues.append({
                    "criterion": "error_handling",
                    "message": "No error handling mentioned in specification",
                    "severity": "warning",
                    "line": None
                })
        
        elif content_type == "code":
            # Check for try-catch blocks or error handling patterns
            if not re.search(r'(try|catch|except|raise|throw)', content, re.IGNORECASE):
                issues.append({
                    "criterion": "error_handling",
                    "message": "No error handling found in code",
                    "severity": "critical",
                    "line": None
                })
        
        return issues
    
    def _check_validation(self, content: str, content_type: str) -> List[Dict[str, Any]]:
        """Check for input validation"""
        issues = []
        
        validation_keywords = ["validate", "validation", "check", "verify"]
        
        if not any(keyword in content.lower() for keyword in validation_keywords):
            issues.append({
                "criterion": "validation",
                "message": "No input validation mentioned",
                "severity": "warning",
                "line": None
            })
        
        return issues
    
    def _check_structure(self, content: str, content_type: str) -> List[Dict[str, Any]]:
        """Check content structure"""
        issues = []
        
        if content_type == "specification":
            required_sections = ["overview", "requirements"]
            for section in required_sections:
                if section not in content.lower():
                    issues.append({
                        "criterion": "structure",
                        "message": f"Missing required section: {section}",
                        "severity": "critical",
                        "line": None
                    })
        
        return issues
    
    def _check_completeness(self, content: str, content_type: str) -> List[Dict[str, Any]]:
        """Check content completeness"""
        issues = []
        
        if len(content.strip()) < 50:
            issues.append({
                "criterion": "completeness",
                "message": "Content appears incomplete or too brief",
                "severity": "critical",
                "line": None
            })
        
        # Check for placeholder text
        placeholders = ["{", "TODO", "FIXME", "placeholder"]
        for placeholder in placeholders:
            if placeholder in content:
                issues.append({
                    "criterion": "completeness",
                    "message": f"Contains placeholder text: {placeholder}",
                    "severity": "warning",
                    "line": None
                })
        
        return issues
    
    def _generate_review_report(self, results: List[Dict[str, Any]]) -> str:
        """Generate formatted review report"""
        if not results:
            return "✅ Review completed successfully. No issues found."
        
        report = "# Code Review Report\n\n"
        
        # Group by severity
        critical = [r for r in results if r["severity"] == "critical"]
        warnings = [r for r in results if r["severity"] == "warning"]
        
        if critical:
            report += "## ❌ Critical Issues\n"
            for issue in critical:
                report += f"- **{issue['criterion']}**: {issue['message']}\n"
            report += "\n"
        
        if warnings:
            report += "## ⚠️ Warnings\n"
            for issue in warnings:
                report += f"- **{issue['criterion']}**: {issue['message']}\n"
            report += "\n"
        
        report += f"## Summary\n"
        report += f"- Total issues: {len(results)}\n"
        report += f"- Critical: {len(critical)}\n"
        report += f"- Warnings: {len(warnings)}\n"
        
        return report