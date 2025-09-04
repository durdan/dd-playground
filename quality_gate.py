from typing import List, Dict, Any
from stop_rules import StopRule, RuleViolation, Severity

class QualityGateResult:
    def __init__(self):
        self.violations: List[RuleViolation] = []
        self.passed = True
        self.should_block = False
    
    def add_violation(self, violation: RuleViolation, block_on_failure: bool = True):
        self.violations.append(violation)
        if violation.severity in [Severity.ERROR, Severity.CRITICAL]:
            self.passed = False
            if block_on_failure:
                self.should_block = True
    
    def get_summary(self) -> Dict[str, Any]:
        return {
            'passed': self.passed,
            'should_block': self.should_block,
            'total_violations': len(self.violations),
            'violations_by_severity': {
                'critical': len([v for v in self.violations if v.severity == Severity.CRITICAL]),
                'error': len([v for v in self.violations if v.severity == Severity.ERROR]),
                'warning': len([v for v in self.violations if v.severity == Severity.WARNING])
            }
        }

class QualityGate:
    def __init__(self, rules: List[StopRule], block_on_failure: bool = True):
        self.rules = rules
        self.block_on_failure = block_on_failure
    
    def evaluate(self, change_data: Dict[str, Any]) -> QualityGateResult:
        """Evaluate all rules against the change data."""
        result = QualityGateResult()
        
        for rule in self.rules:
            violations = rule.evaluate(change_data)
            for violation in violations:
                result.add_violation(violation, self.block_on_failure)
        
        return result
    
    def add_rule(self, rule: StopRule):
        """Add a new rule to the quality gate."""
        self.rules.append(rule)
    
    def remove_rule(self, rule_name: str):
        """Remove a rule by name."""
        self.rules = [rule for rule in self.rules if rule.name != rule_name]