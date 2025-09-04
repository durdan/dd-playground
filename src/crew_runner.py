import asyncio
import json
import time
from typing import Dict, Any
from datetime import datetime
from crewai import Agent, Task, Crew
from crewai.tools import BaseTool

from .models import WorkflowRequest, WorkflowResult, WorkflowStatus, AgentConfig, TaskConfig
from .config import settings


class CrewAIRunner:
    """Service to execute CrewAI workflows."""
    
    def __init__(self):
        self.active_workflows: Dict[str, WorkflowResult] = {}
    
    async def execute_workflow(self, request: WorkflowRequest) -> WorkflowResult:
        """Execute a CrewAI workflow asynchronously."""
        workflow_result = WorkflowResult(
            workflow_id=request.workflow_id,
            status=WorkflowStatus.PENDING,
            started_at=datetime.utcnow()
        )
        
        self.active_workflows[request.workflow_id] = workflow_result
        
        try:
            workflow_result.status = WorkflowStatus.RUNNING
            start_time = time.time()
            
            # Create agents
            agents = self._create_agents(request.agents)
            
            # Create tasks
            tasks = self._create_tasks(request.tasks, agents)
            
            # Create and run crew
            crew = Crew(
                agents=list(agents.values()),
                tasks=tasks,
                verbose=True,
                max_iter=request.max_iterations or settings.crew_max_iterations
            )
            
            # Execute workflow with timeout
            result = await asyncio.wait_for(
                self._run_crew(crew),
                timeout=request.timeout or settings.crew_max_execution_time
            )
            
            execution_time = time.time() - start_time
            
            workflow_result.status = WorkflowStatus.COMPLETED
            workflow_result.completed_at = datetime.utcnow()
            workflow_result.execution_time = execution_time
            workflow_result.results = {"output": result}
            
        except asyncio.TimeoutError:
            workflow_result.status = WorkflowStatus.FAILED
            workflow_result.error_message = "Workflow execution timed out"
            workflow_result.completed_at = datetime.utcnow()
            
        except Exception as e:
            workflow_result.status = WorkflowStatus.FAILED
            workflow_result.error_message = str(e)
            workflow_result.completed_at = datetime.utcnow()
        
        return workflow_result
    
    def _create_agents(self, agent_configs: list[AgentConfig]) -> Dict[str, Agent]:
        """Create CrewAI agents from configuration."""
        agents = {}
        
        for config in agent_configs:
            agent = Agent(
                role=config.role,
                goal=config.goal,
                backstory=config.backstory,
                verbose=config.verbose,
                tools=self._get_tools(config.tools)
            )
            agents[config.role] = agent
        
        return agents
    
    def _create_tasks(self, task_configs: list[TaskConfig], agents: Dict[str, Agent]) -> list[Task]:
        """Create CrewAI tasks from configuration."""
        tasks = []
        
        for config in task_configs:
            if config.agent not in agents:
                raise ValueError(f"Agent '{config.agent}' not found for task")
            
            task = Task(
                description=config.description,
                agent=agents[config.agent],
                expected_output=config.expected_output,
                tools=self._get_tools(config.tools)
            )
            tasks.append(task)
        
        return tasks
    
    def _get_tools(self, tool_names: list[str]) -> list[BaseTool]:
        """Get tools by name (placeholder for actual tool implementation)."""
        # In a real implementation, you would have a tool registry
        return []
    
    async def _run_crew(self, crew: Crew) -> str:
        """Run crew in a separate thread to avoid blocking."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, crew.kickoff)
    
    def get_workflow_status(self, workflow_id: str) -> WorkflowResult:
        """Get the status of a workflow."""
        if workflow_id not in self.active_workflows:
            raise ValueError(f"Workflow '{workflow_id}' not found")
        
        return self.active_workflows[workflow_id]
    
    def cancel_workflow(self, workflow_id: str) -> bool:
        """Cancel a running workflow."""
        if workflow_id not in self.active_workflows:
            return False
        
        workflow = self.active_workflows[workflow_id]
        if workflow.status == WorkflowStatus.RUNNING:
            workflow.status = WorkflowStatus.CANCELLED
            workflow.completed_at = datetime.utcnow()
            return True
        
        return False