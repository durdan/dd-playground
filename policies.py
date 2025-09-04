from typing import List, Dict, Any
from .exceptions import PolicyViolationError

class PolicyValidator:
    """Validates tasks against agent policies"""
    
    def __init__(self, policies: List[str]):
        self.policies = policies
        self.policy_rules = self._parse_policies(policies)
    
    def _parse_policies(self, policies: List[str]) -> Dict[str, Any]:
        """Parse policy strings into validation rules"""
        rules = {}
        
        for policy in policies:
            if "no_external_data" in policy.lower():
                rules['no_external_data'] = True
            elif "require_approval" in policy.lower():
                rules['require_approval'] = True
            elif "max_execution_time" in policy.lower():
                # Extract time limit if specified
                rules['max_execution_time'] = 300  # default 5 minutes
        
        return rules
    
    def validate_task(self, task_data: Dict[str, Any]) -> bool:
        """Validate task against policies"""
        if not isinstance(task_data, dict):
            raise PolicyViolationError("Task data must be a dictionary")
        
        # Check external data policy
        if self.policy_rules.get('no_external_data') and task_data.get('external_data'):
            return False
        
        # Check approval requirement
        if self.policy_rules.get('require_approval') and not task_data.get('approved'):
            return False
        
        return True