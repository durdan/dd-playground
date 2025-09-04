from typing import Dict, Any, Optional
from .manager import ObservabilityManager

class CrewAIObserver:
    """Specialized observer for CrewAI operations."""
    
    def __init__(self, observability_manager: ObservabilityManager):
        self.obs_manager = observability_manager
        self.logger = observability_manager.logger
    
    def observe_agent_execution(self, agent_id: str, task_description: str, **metadata):
        """Observe agent task execution."""
        return self.obs_manager.observe_operation(
            operation_type="agent_execution",
            operation_id=f"agent_{agent_id}_{int(time.time())}",
            agent_id=agent_id,
            task_description=task_description,
            **metadata
        )
    
    def observe_crew_execution(self, crew_id: str, crew_config: Dict[str, Any]):
        """Observe crew execution."""
        return self.obs_manager.observe_operation(
            operation_type="crew_execution",
            operation_id=f"crew_{crew_id}_{int(time.time())}",
            crew_id=crew_id,
            agent_count=len(crew_config.get('agents', [])),
            task_count=len(crew_config.get('tasks', [])),
            **crew_config
        )
    
    def observe_task_execution(self, task_id: str, task_type: str, assigned_agent: str):
        """Observe individual task execution."""
        return self.obs_manager.observe_operation(
            operation_type="task_execution",
            operation_id=f"task_{task_id}_{int(time.time())}",
            task_id=task_id,
            task_type=task_type,
            assigned_agent=assigned_agent
        )
    
    def log_agent_decision(self, agent_id: str, decision: str, reasoning: str):
        """Log agent decision making process."""
        self.logger.info(
            "Agent decision",
            extra={
                "agent_id": agent_id,
                "decision": decision,
                "reasoning": reasoning,
                "event_type": "agent_decision"
            }
        )
    
    def log_crew_collaboration(self, crew_id: str, agents_involved: list, interaction_type: str):
        """Log crew collaboration events."""
        self.logger.info(
            "Crew collaboration",
            extra={
                "crew_id": crew_id,
                "agents_involved": agents_involved,
                "interaction_type": interaction_type,
                "event_type": "crew_collaboration"
            }
        )