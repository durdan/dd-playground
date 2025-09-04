import re
from typing import List
from .detector_types import SafetyIssue, RiskLevel, OperationType

class SecretsOperationAnalyzer:
    def __init__(self):
        self.secret_patterns = [
            r'(?i)(password|passwd|pwd)\s*[=:]\s*["\']?[\w@#$%^&*]+',
            r'(?i)(api[_-]?key|apikey)\s*[=:]\s*["\']?[\w-]+',
            r'(?i)(secret|token)\s*[=:]\s*["\']?[\w-]+',
            r'(?i)(private[_-]?key)\s*[=:]\s*["\']?[\w-]+',
        ]
        self.sensitive_operations = [
            'store_secret', 'save_password', 'set_api_key', 'update_credentials'
        ]
    
    def analyze_operation(self, operation: str, content: str = "") -> List[SafetyIssue]:
        issues = []
        
        # Check for hardcoded secrets
        for pattern in self.secret_patterns:
            matches = re.findall(pattern, content)
            if matches:
                issues.append(SafetyIssue(
                    type=OperationType.SECRETS,
                    risk_level=RiskLevel.CRITICAL,
                    message="Hardcoded secret detected",
                    details={"pattern": pattern, "matches_count": len(matches)},
                    confidence=0.9
                ))
        
        # Check for sensitive operations
        for sensitive_op in self.sensitive_operations:
            if sensitive_op.lower() in operation.lower():
                issues.append(SafetyIssue(
                    type=OperationType.SECRETS,
                    risk_level=RiskLevel.HIGH,
                    message=f"Sensitive secrets operation: {sensitive_op}",
                    details={"operation": operation},
                    confidence=0.8
                ))
        
        # Check for plain text secret transmission
        if self._has_plain_text_secrets(content):
            issues.append(SafetyIssue(
                type=OperationType.SECRETS,
                risk_level=RiskLevel.HIGH,
                message="Potential plain text secret transmission",
                details={"content_length": len(content)},
                confidence=0.7
            ))
        
        return issues
    
    def _has_plain_text_secrets(self, content: str) -> bool:
        # Simple heuristic: look for patterns that suggest unencrypted secrets
        plain_text_indicators = [
            r'(?i)password\s*:\s*["\']?[a-zA-Z0-9@#$%^&*]{6,}["\']?',
            r'(?i)send.*password.*plain',
            r'(?i)unencrypted.*secret'
        ]
        return any(re.search(pattern, content) for pattern in plain_text_indicators)