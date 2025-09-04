from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Any, Optional

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class OperationType(Enum):
    DATABASE = "database"
    SECRETS = "secrets"
    AUTH = "auth"

@dataclass
class SafetyIssue:
    type: OperationType
    risk_level: RiskLevel
    message: str
    details: Dict[str, Any]
    confidence: float  # 0.0 to 1.0

@dataclass
class SafetyReport:
    operation: str
    issues: List[SafetyIssue]
    is_safe: bool
    overall_risk: RiskLevel
    
    def add_issue(self, issue: SafetyIssue):
        self.issues.append(issue)
        # Update overall risk to highest found
        risk_levels = [RiskLevel.LOW, RiskLevel.MEDIUM, RiskLevel.HIGH, RiskLevel.CRITICAL]
        current_max = risk_levels.index(self.overall_risk)
        new_level = risk_levels.index(issue.risk_level)
        if new_level > current_max:
            self.overall_risk = issue.risk_level
        self.is_safe = self.overall_risk in [RiskLevel.LOW, RiskLevel.MEDIUM]