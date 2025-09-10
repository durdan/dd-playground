import re
from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class SecurityIssue:
    severity: str  # "high", "medium", "low"
    description: str
    recommendation: str

class SecurityReviewer:
    def __init__(self):
        self.security_patterns = [
            (r'api[_-]?key\s*=\s*["\'][^"\']+["\']', "high", "Hardcoded API key detected"),
            (r'password\s*=\s*["\'][^"\']+["\']', "high", "Hardcoded password detected"),
            (r'token\s*=\s*["\'][^"\']+["\']', "medium", "Hardcoded token detected"),
            (r'secret\s*=\s*["\'][^"\']+["\']', "high", "Hardcoded secret detected"),
        ]
    
    def review_ai_integration(self, code_content: str, api_usage: dict) -> Tuple[bool, List[SecurityIssue]]:
        issues = []
        
        # Check for hardcoded secrets
        issues.extend(self._check_hardcoded_secrets(code_content))
        
        # Check API key management
        issues.extend(self._check_api_key_management(api_usage))
        
        # Check input validation
        issues.extend(self._check_input_validation(code_content))
        
        # Determine if review passes
        high_severity_issues = [issue for issue in issues if issue.severity == "high"]
        review_passed = len(high_severity_issues) == 0
        
        return review_passed, issues
    
    def _check_hardcoded_secrets(self, code_content: str) -> List[SecurityIssue]:
        issues = []
        for pattern, severity, description in self.security_patterns:
            if re.search(pattern, code_content, re.IGNORECASE):
                issues.append(SecurityIssue(
                    severity=severity,
                    description=description,
                    recommendation="Use environment variables or secure key management"
                ))
        return issues
    
    def _check_api_key_management(self, api_usage: dict) -> List[SecurityIssue]:
        issues = []
        
        if not api_usage.get('uses_env_vars', False):
            issues.append(SecurityIssue(
                severity="high",
                description="API key not loaded from environment variables",
                recommendation="Load API keys from environment variables"
            ))
        
        if not api_usage.get('validates_key_format', False):
            issues.append(SecurityIssue(
                severity="medium",
                description="API key format not validated",
                recommendation="Add basic API key format validation"
            ))
        
        return issues
    
    def _check_input_validation(self, code_content: str) -> List[SecurityIssue]:
        issues = []
        
        if 'validate(' not in code_content:
            issues.append(SecurityIssue(
                severity="medium",
                description="Input validation not detected",
                recommendation="Implement input validation for user requirements"
            ))
        
        return issues