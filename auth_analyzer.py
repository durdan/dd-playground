import re
from typing import List
from .detector_types import SafetyIssue, RiskLevel, OperationType

class AuthOperationAnalyzer:
    def __init__(self):
        self.critical_auth_operations = [
            'grant_admin', 'revoke_access', 'delete_user', 'change_permissions',
            'bypass_auth', 'disable_mfa', 'reset_password'
        ]
        self.privilege_escalation_patterns = [
            r'(?i)sudo|su\s+root|chmod\s+777',
            r'(?i)grant.*admin|add.*admin|promote.*admin',
            r'(?i)bypass.*auth|skip.*auth|disable.*auth'
        ]
    
    def analyze_auth_operation(self, operation: str, context: str = "") -> List[SafetyIssue]:
        issues = []
        
        # Check for critical auth operations
        for critical_op in self.critical_auth_operations:
            if critical_op.lower() in operation.lower():
                issues.append(SafetyIssue(
                    type=OperationType.AUTH,
                    risk_level=RiskLevel.CRITICAL,
                    message=f"Critical auth operation: {critical_op}",
                    details={"operation": operation},
                    confidence=0.9
                ))
        
        # Check for privilege escalation patterns
        combined_text = f"{operation} {context}"
        for pattern in self.privilege_escalation_patterns:
            if re.search(pattern, combined_text):
                issues.append(SafetyIssue(
                    type=OperationType.AUTH,
                    risk_level=RiskLevel.CRITICAL,
                    message="Potential privilege escalation detected",
                    details={"pattern": pattern, "context": context[:100]},
                    confidence=0.85
                ))
        
        # Check for bulk user operations
        if self._is_bulk_user_operation(operation, context):
            issues.append(SafetyIssue(
                type=OperationType.AUTH,
                risk_level=RiskLevel.HIGH,
                message="Bulk user operation detected",
                details={"operation": operation},
                confidence=0.7
            ))
        
        return issues
    
    def _is_bulk_user_operation(self, operation: str, context: str) -> bool:
        bulk_indicators = [
            r'(?i)all\s+users|every\s+user|\*\s+users',
            r'(?i)batch.*user|bulk.*user|mass.*user',
            r'(?i)delete.*users|remove.*users'
        ]
        combined = f"{operation} {context}"
        return any(re.search(pattern, combined) for pattern in bulk_indicators)