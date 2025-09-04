from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from .policies import PolicyValidator
from .exceptions import AgentError, PolicyViolationError

@dataclass
class StandardOperatingProcedure:
    """Defines step-by-step procedures for an agent"""
    name: str
    steps: List[str]
    prerequisites: List[str] = None
    
    def __post_init__(self):
        if not self.name.strip():
            raise AgentError("SOP name cannot be empty")
        if not self.steps:
            raise AgentError("SOP must have at least one step")
        self.prerequisites = self.prerequisites or []

class Agent:
    """Core CrewAI agent with role, policies, and SOPs"""
    
    def __init__(self, 
                 name: str, 
                 role: str, 
                 policies: List[str], 
                 sops: List[StandardOperatingProcedure]):
        self._validate_inputs(name, role, policies, sops)
        
        self.name = name
        self.role = role
        self.policies = policies
        self.sops = {sop.name: sop for sop in sops}
        self.policy_validator = PolicyValidator(policies)
        self.task_history: List[Dict[str, Any]] = []
    
    def _validate_inputs(self, name: str, role: str, policies: List[str], sops: List[StandardOperatingProcedure]):
        """Validate agent creation inputs"""
        if not name or not name.strip():
            raise AgentError("Agent name cannot be empty")
        if not role or not role.strip():
            raise AgentError("Agent role cannot be empty")
        if not isinstance(policies, list):
            raise AgentError("Policies must be a list")
        if not isinstance(sops, list):
            raise AgentError("SOPs must be a list")
    
    def execute_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task following policies and SOPs"""
        # Validate against policies
        if not self.policy_validator.validate_task(task_data):
            raise PolicyViolationError(f"Task violates agent policies: {self.policies}")
        
        # Find appropriate SOP
        sop_name = task_data.get('sop', 'default')
        if sop_name not in self.sops:
            raise AgentError(f"SOP '{sop_name}' not found for agent {self.name}")
        
        sop = self.sops[sop_name]
        
        # Execute SOP steps
        result = self._execute_sop(sop, task_data)
        
        # Record task execution
        self.task_history.append({
            'task': task_data,
            'sop_used': sop_name,
            'result': result,
            'timestamp': self._get_timestamp()
        })
        
        return result
    
    def _execute_sop(self, sop: StandardOperatingProcedure, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute SOP steps"""
        executed_steps = []
        
        for step in sop.steps:
            step_result = self._execute_step(step, task_data)
            executed_steps.append({
                'step': step,
                'result': step_result
            })
        
        return {
            'agent': self.name,
            'role': self.role,
            'sop': sop.name,
            'steps_executed': executed_steps,
            'status': 'completed'
        }
    
    def _execute_step(self, step: str, task_data: Dict[str, Any]) -> str:
        """Execute individual SOP step - simplified simulation"""
        return f"Executed: {step} with data: {task_data.get('input', 'N/A')}"
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Return agent capabilities"""
        return {
            'name': self.name,
            'role': self.role,
            'policies': self.policies,
            'available_sops': list(self.sops.keys()),
            'tasks_completed': len(self.task_history)
        }