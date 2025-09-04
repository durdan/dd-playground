import re
from typing import List
from .detector_types import SafetyIssue, RiskLevel, OperationType

class DatabaseOperationAnalyzer:
    def __init__(self):
        self.dangerous_operations = {
            'DROP': RiskLevel.CRITICAL,
            'DELETE': RiskLevel.HIGH,
            'TRUNCATE': RiskLevel.CRITICAL,
            'ALTER': RiskLevel.MEDIUM,
            'UPDATE': RiskLevel.MEDIUM,
        }
        self.sensitive_tables = ['users', 'accounts', 'payments', 'credentials', 'auth']
    
    def analyze_sql(self, sql: str) -> List[SafetyIssue]:
        issues = []
        sql_upper = sql.upper().strip()
        
        # Check for dangerous operations
        for operation, risk in self.dangerous_operations.items():
            if sql_upper.startswith(operation):
                issues.append(SafetyIssue(
                    type=OperationType.DATABASE,
                    risk_level=risk,
                    message=f"Dangerous database operation: {operation}",
                    details={"operation": operation, "sql": sql[:100]},
                    confidence=0.9
                ))
        
        # Check for operations on sensitive tables
        for table in self.sensitive_tables:
            if re.search(rf'\b{table}\b', sql, re.IGNORECASE):
                issues.append(SafetyIssue(
                    type=OperationType.DATABASE,
                    risk_level=RiskLevel.HIGH,
                    message=f"Operation on sensitive table: {table}",
                    details={"table": table, "sql": sql[:100]},
                    confidence=0.8
                ))
        
        # Check for missing WHERE clause in DELETE/UPDATE
        if re.match(r'(DELETE|UPDATE)', sql_upper) and 'WHERE' not in sql_upper:
            issues.append(SafetyIssue(
                type=OperationType.DATABASE,
                risk_level=RiskLevel.CRITICAL,
                message="DELETE/UPDATE without WHERE clause",
                details={"sql": sql[:100]},
                confidence=0.95
            ))
        
        return issues