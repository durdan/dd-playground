import json
import os
import tempfile
from typing import Dict, Any, Optional
from pathlib import Path
import docker
from docker.errors import DockerException


class DockerCrewAIExecutor:
    """Docker-based executor for CrewAI workflows."""
    
    def __init__(self, image_name: str = "crewai-executor:latest"):
        self.image_name = image_name
        self.client = self._get_docker_client()
    
    def _get_docker_client(self) -> docker.DockerClient:
        """Get Docker client with error handling."""
        try:
            client = docker.from_env()
            client.ping()  # Test connection
            return client
        except DockerException as e:
            raise RuntimeError(f"Failed to connect to Docker: {str(e)}")
    
    def execute_crew_workflow(
        self, 
        workflow_config: Dict[str, Any],
        environment_vars: Optional[Dict[str, str]] = None,
        timeout: int = 300
    ) -> Dict[str, Any]:
        """Execute a CrewAI workflow in Docker container."""
        
        if not workflow_config:
            raise ValueError("Workflow configuration cannot be empty")
        
        # Validate required fields
        required_fields = ["agents", "crew", "execution"]
        for field in required_fields:
            if field not in workflow_config:
                raise ValueError(f"Missing required field: {field}")
        
        try:
            # Create temporary directory for workflow files
            with tempfile.TemporaryDirectory() as temp_dir:
                config_path = Path(temp_dir) / "workflow_config.json"
                
                # Write configuration to file
                with open(config_path, 'w') as f:
                    json.dump(workflow_config, f, indent=2)
                
                # Prepare environment variables
                env_vars = environment_vars or {}
                env_vars.update({
                    "WORKFLOW_CONFIG_PATH": "/tmp/workflow_config.json"
                })
                
                # Run container
                result = self.client.containers.run(
                    image=self.image_name,
                    command=["python", "-c", self._get_execution_script()],
                    environment=env_vars,
                    volumes={
                        str(config_path): {
                            "bind": "/tmp/workflow_config.json",
                            "mode": "ro"
                        }
                    },
                    remove=True,
                    stdout=True,
                    stderr=True,
                    timeout=timeout
                )
                
                # Parse result
                try:
                    return json.loads(result.decode('utf-8'))
                except json.JSONDecodeError:
                    return {
                        "status": "completed",
                        "raw_output": result.decode('utf-8'),
                        "parsed": False
                    }
                    
        except DockerException as e:
            return {
                "status": "failed",
                "error": f"Docker execution failed: {str(e)}",
                "error_type": "docker_error"
            }
        except Exception as e:
            return {
                "status": "failed", 
                "error": str(e),
                "error_type": "execution_error"
            }
    
    def _get_execution_script(self) -> str:
        """Get the Python script to execute inside container."""
        return '''
import json
import os
import sys
from crewai_agent import CrewAIAgentManager, AgentConfig
from crewai_crew import CrewAICrewManager, CrewConfig, TaskConfig

def main():
    try:
        # Load workflow configuration
        config_path = os.environ.get("WORKFLOW_CONFIG_PATH", "/tmp/workflow_config.json")
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Initialize managers
        agent_manager = CrewAIAgentManager()
        crew_manager = CrewAICrewManager(agent_manager)
        
        # Create agents
        for agent_id, agent_config in config["agents"].items():
            agent_cfg = AgentConfig(**agent_config)
            agent_manager.create_agent(agent_id, agent_cfg)
        
        # Create and execute crew
        crew_config = config["crew"]
        tasks = [TaskConfig(**task) for task in crew_config["tasks"]]
        crew_cfg = CrewConfig(
            agents=crew_config["agents"],
            tasks=tasks,
            verbose=crew_config.get("verbose", True),
            process_type=crew_config.get("process_type", "sequential")
        )
        
        crew_id = config["execution"]["crew_id"]
        crew_manager.create_crew(crew_id, crew_cfg)
        
        # Execute
        inputs = config["execution"].get("inputs", {})
        result = crew_manager.execute_crew(crew_id, inputs)
        
        print(json.dumps(result))
        
    except Exception as e:
        error_result = {
            "status": "failed",
            "error": str(e),
            "error_type": "script_error"
        }
        print(json.dumps(error_result))
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
    
    def build_image(self, dockerfile_path: str = "Dockerfile.crewai") -> None:
        """Build the CrewAI Docker image."""
        if not os.path.exists(dockerfile_path):
            raise FileNotFoundError(f"Dockerfile not found: {dockerfile_path}")
        
        try:
            self.client.images.build(
                path=".",
                dockerfile=dockerfile_path,
                tag=self.image_name,
                rm=True
            )
        except DockerException as e:
            raise RuntimeError(f"Failed to build Docker image: {str(e)}")