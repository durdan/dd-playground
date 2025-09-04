import re
from agents.base_agent import BaseAgent
from models import TaskRequest, AgentResponse, AgentRole, TaskStatus

class CodeReviewer(BaseAgent):
    def __init__(self):
        super().__init__(AgentRole.CODE_REVIEWER)
    
    def process(self, request: TaskRequest) -> AgentResponse:
        """Review code quality and standards"""
        if not request.code:
            return self._create_response(
                TaskStatus.FAILED,
                {},
                errors=["No code provided for review"]
            )
        
        issues = []
        suggestions = []
        quality_score = 10  # Start with perfect score
        
        # Check basic code quality metrics
        issues.extend(self._check_naming_conventions(request.code))
        issues.extend(self._check_code_structure(request.code))
        issues.extend(self._check_documentation(request.code))
        
        # Generate suggestions
        suggestions.extend(self._generate_suggestions(request.code))
        
        # Calculate quality score
        quality_score -= len(issues)
        quality_score = max(0, quality_score)
        
        feedback = [f"Code review completed. Quality score: {quality_score}/10"]
        if issues:
            feedback.append(f"Found {len(issues)} issues to address")
        
        return self._create_response(
            TaskStatus.COMPLETED,
            {
                "quality_score": quality_score,
                "issues_count": len(issues),
                "has_documentation": self._has_documentation(request.code)
            },
            feedback=feedback,
            suggestions=suggestions,
            errors=issues
        )
    
    def _check_naming_conventions(self, code: str) -> list:
        """Check for proper naming conventions"""
        issues = []
        
        # Check for camelCase variables (should be snake_case in Python)
        camel_case_pattern = r'\b[a-z]+[A-Z][a-zA-Z]*\b'
        if re.search(camel_case_pattern, code):
            issues.append("Consider using snake_case for variable names")
        
        return issues
    
    def _check_code_structure(self, code: str) -> list:
        """Check code structure and organization"""
        issues = []
        lines = code.split('\n')
        
        # Check line length
        long_lines = [i+1 for i, line in enumerate(lines) if len(line) > 100]
        if long_lines:
            issues.append(f"Lines too long (>100 chars): {long_lines[:3]}")
        
        # Check for proper imports
        if 'import' in code and not code.strip().startswith(('import', 'from')):
            issues.append("Imports should be at the top of the file")
        
        return issues
    
    def _check_documentation(self, code: str) -> list:
        """Check for documentation"""
        issues = []
        
        if 'def ' in code and '"""' not in code and "'''" not in code:
            issues.append("Functions should have docstrings")
        
        return issues
    
    def _generate_suggestions(self, code: str) -> list:
        """Generate improvement suggestions"""
        suggestions = []
        
        if 'print(' in code:
            suggestions.append("Consider using logging instead of print statements")
        
        if 'except:' in code:
            suggestions.append("Avoid bare except clauses, specify exception types")
        
        return suggestions
    
    def _has_documentation(self, code: str) -> bool:
        """Check if code has documentation"""
        return '"""' in code or "'''" in code