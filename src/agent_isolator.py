from crewai import Agent, Task
from typing import Any, Dict, Optional
import json
import uuid
from .docker_executor import DockerExecutor, ContainerConfig
from .resource_manager import ResourceManager, ResourceLimits

class IsolatedAgent:
    def __init__(self, agent: Agent, docker_image: str = "crewai-agent:latest"):
        self.agent = agent
        self.docker_image = docker_image
        self.executor = DockerExecutor()
        self.resource_manager = ResourceManager(ResourceLimits())
        
    def execute_task(self, task: Task, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute task in isolated Docker container."""
        if not self.resource_manager.can_create_container():
            raise RuntimeError("Resource limit exceeded: too many active containers")
        
        container_name = f"agent-{uuid.uuid4().hex[:8]}"
        
        # Prepare task data
        task_data = {
            "agent_role": self.agent.role,
            "agent_goal": self.agent.goal,
            "agent_backstory": self.agent.backstory,
            "task_description": task.description,
            "task_expected_output": task.expected_output,
            "context": context or {}
        }
        
        # Configure container
        config = ContainerConfig(
            image=self.docker_image,
            command=["python", "agent_runtime.py"],
            environment={
                "AGENT_ROLE": self.agent.role,
                "PYTHONPATH": "/app"
            },
            volumes={},
            mem_limit="512m",
            cpu_limit=1.0,
            network_mode="none",  # No network access
            read_only=True
        )
        
        try:
            # Create and execute
            container = self.executor.create_container(config, container_name)
            self.resource_manager.register_container(container.id)
            
            result = self.executor.execute_task(container, task_data)
            
            return {
                "success": result["exit_code"] == 0,
                "output": result["output"],
                "logs": result["logs"],
                "container_id": container.id
            }
            
        finally:
            self.resource_manager.unregister_container(container.id)

class IsolatedCrew:
    def __init__(self, agents: list[Agent], tasks: list[Task]):
        self.isolated_agents = [IsolatedAgent(agent) for agent in agents]
        self.tasks = tasks
        
    def kickoff(self) -> Dict[str, Any]:
        """Execute all tasks with isolated agents."""
        results = []
        context = {}
        
        for i, task in enumerate(self.tasks):
            agent = self.isolated_agents[i % len(self.isolated_agents)]
            
            try:
                result = agent.execute_task(task, context)
                results.append({
                    "task_index": i,
                    "agent_role": agent.agent.role,
                    "result": result
                })
                
                # Pass successful results as context to next task
                if result["success"]:
                    context[f"task_{i}_output"] = result["output"]
                    
            except Exception as e:
                results.append({
                    "task_index": i,
                    "agent_role": agent.agent.role,
                    "result": {
                        "success": False,
                        "output": {},
                        "logs": f"Execution failed: {str(e)}",
                        "container_id": None
                    }
                })
        
        return {
            "success": all(r["result"]["success"] for r in results),
            "results": results
        }