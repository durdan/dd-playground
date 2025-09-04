from typing import Dict, Any, List
from models import SafetyRule, RiskLevel

class SafetyValidator:
    def __init__(self):
        self.rules: Dict[str, SafetyRule] = {}
        self._setup_default_rules()
    
    def _setup_default_rules(self):
        """Setup default safety rules"""
        self.add_rule(SafetyRule(
            name="max_cost",
            max_value=1000.0,
            metric_key="cost",
            description="Maximum operation cost in USD"
        ))
        self.add_rule(SafetyRule(
            name="max_users_affected",
            max_value=100.0,
            metric_key="users_affected",
            description="Maximum number of users that can be affected"
        ))
        self.add_rule(SafetyRule(
            name="max_data_volume",
            max_value=1000000.0,
            metric_key="data_volume_mb",
            description="Maximum data volume in MB"
        ))
    
    def add_rule(self, rule: SafetyRule):
        """Add a safety rule"""
        if not rule.name or not rule.metric_key:
            raise ValueError("Rule name and metric_key are required")
        self.rules[rule.name] = rule
    
    def validate_operation(self, operation_data: Dict[str, Any]) -> tuple[List[str], RiskLevel]:
        """Validate operation against safety rules"""
        violations = []
        max_risk = RiskLevel.LOW
        
        for rule in self.rules.values():
            if rule.metric_key in operation_data:
                value = operation_data[rule.metric_key]
                if not isinstance(value, (int, float)):
                    continue
                    
                if value > rule.max_value:
                    violations.append(f"{rule.name}: {value} exceeds limit of {rule.max_value}")
                    
                    # Determine risk level based on how much the limit is exceeded
                    excess_ratio = value / rule.max_value
                    if excess_ratio > 5:
                        max_risk = max(max_risk, RiskLevel.CRITICAL, key=lambda x: x.value)
                    elif excess_ratio > 2:
                        max_risk = max(max_risk, RiskLevel.HIGH, key=lambda x: x.value)
                    elif excess_ratio > 1.5:
                        max_risk = max(max_risk, RiskLevel.MEDIUM, key=lambda x: x.value)
        
        return violations, max_risk
    
    def requires_human_approval(self, risk_level: RiskLevel, violations: List[str]) -> bool:
        """Determine if human approval is required"""
        return len(violations) > 0 or risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]