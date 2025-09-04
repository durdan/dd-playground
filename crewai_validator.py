from typing import Dict, Any, List
from models import QualityGate, ValidationResult, PRContext
import json
from datetime import datetime

class CrewAIValidator:
    """Service for orchestrating CrewAI agents for quality validation"""
    
    def __init__(self):
        self.agents = self._initialize_agents()
    
    def _initialize_agents(self) -> Dict[str, Any]:
        """Initialize CrewAI agents - mock implementation"""
        return {
            "code_reviewer": {"role": "Senior Code Reviewer", "expertise": "code_quality"},
            "test_validator": {"role": "QA Engineer", "expertise": "testing"},
            "doc_reviewer": {"role": "Technical Writer", "expertise": "documentation"},
            "security_scanner": {"role": "Security Analyst", "expertise": "security"}
        }
    
    def validate_gate(self, gate: QualityGate, pr_context: PRContext) -> ValidationResult:
        """Validate a quality gate using appropriate CrewAI agent"""
        if not gate.crew_agent:
            raise ValueError(f"No CrewAI agent specified for gate: {gate.name}")
        
        if gate.crew_agent not in self.agents:
            raise ValueError(f"Unknown CrewAI agent: {gate.crew_agent}")
        
        # Mock CrewAI agent execution
        result = self._execute_agent_validation(gate, pr_context)
        
        return ValidationResult(
            gate_name=gate.name,
            passed=result["passed"],
            score=result["score"],
            feedback=result["feedback"],
            details=result.get("details", {}),
            timestamp=datetime.now()
        )
    
    def _execute_agent_validation(self, gate: QualityGate, pr_context: PRContext) -> Dict[str, Any]:
        """Execute CrewAI agent validation - mock implementation"""
        agent_name = gate.crew_agent
        
        # Mock different validation logic based on gate type
        if agent_name == "code_reviewer":
            return self._mock_code_review(gate, pr_context)
        elif agent_name == "test_validator":
            return self._mock_test_validation(gate, pr_context)
        elif agent_name == "doc_reviewer":
            return self._mock_doc_review(gate, pr_context)
        elif agent_name == "security_scanner":
            return self._mock_security_scan(gate, pr_context)
        else:
            return {"passed": False, "score": 0.0, "feedback": "Unknown agent"}
    
    def _mock_code_review(self, gate: QualityGate, pr_context: PRContext) -> Dict[str, Any]:
        """Mock code review validation"""
        # Simple heuristics for demo
        lines_changed = len(pr_context.diff.split('\n'))
        files_count = len(pr_context.files_changed)
        
        score = max(0.0, min(10.0, 10.0 - (lines_changed / 100) - (files_count / 10)))
        min_score = gate.criteria.get("min_score", 7.0)
        
        return {
            "passed": score >= min_score,
            "score": score,
            "feedback": f"Code review score: {score:.1f}/10. Files: {files_count}, Lines: {lines_changed}",
            "details": {"lines_changed": lines_changed, "files_count": files_count}
        }
    
    def _mock_test_validation(self, gate: QualityGate, pr_context: PRContext) -> Dict[str, Any]:
        """Mock test validation"""
        # Check if test files are present
        test_files = [f for f in pr_context.files_changed if 'test' in f.lower()]
        has_tests = len(test_files) > 0
        
        coverage = 85.0 if has_tests else 45.0
        min_coverage = gate.criteria.get("min_coverage", 80.0)
        
        return {
            "passed": coverage >= min_coverage,
            "score": coverage,
            "feedback": f"Test coverage: {coverage}%. Test files: {len(test_files)}",
            "details": {"coverage": coverage, "test_files": test_files}
        }
    
    def _mock_doc_review(self, gate: QualityGate, pr_context: PRContext) -> Dict[str, Any]:
        """Mock documentation review"""
        doc_files = [f for f in pr_context.files_changed if f.endswith(('.md', '.rst', '.txt'))]
        has_docs = len(doc_files) > 0 or 'readme' in pr_context.description.lower()
        
        score = 8.0 if has_docs else 4.0
        min_completeness = gate.criteria.get("min_completeness", 70.0)
        
        return {
            "passed": score >= (min_completeness / 10),
            "score": score,
            "feedback": f"Documentation completeness: {score * 10}%. Doc files: {len(doc_files)}",
            "details": {"doc_files": doc_files, "has_description_docs": has_docs}
        }
    
    def _mock_security_scan(self, gate: QualityGate, pr_context: PRContext) -> Dict[str, Any]:
        """Mock security scan"""
        # Simple check for common security patterns
        risky_patterns = ['password', 'secret', 'api_key', 'token']
        security_issues = []
        
        for pattern in risky_patterns:
            if pattern in pr_context.diff.lower():
                security_issues.append(f"Potential {pattern} exposure")
        
        passed = len(security_issues) == 0
        score = 10.0 if passed else max(0.0, 10.0 - len(security_issues) * 2)
        
        return {
            "passed": passed,
            "score": score,
            "feedback": f"Security scan: {len(security_issues)} issues found",
            "details": {"issues": security_issues}
        }