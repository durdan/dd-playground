import os
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

@dataclass
class WorkflowConfig:
    docker_image: str
    github_token: str
    repo_owner: str
    repo_name: str
    base_branch: str = "main"
    working_directory: str = "/workspace"
    build_commands: List[str] = None
    test_commands: List[str] = None
    volumes: Dict[str, str] = None
    env_vars: Dict[str, str] = None
    
    def __post_init__(self):
        if self.build_commands is None:
            self.build_commands = ["make", "build"]
        if self.test_commands is None:
            self.test_commands = ["make", "test"]
        if self.volumes is None:
            self.volumes = {}
        if self.env_vars is None:
            self.env_vars = {}
    
    @classmethod
    def from_file(cls, config_path: str) -> 'WorkflowConfig':
        """Load configuration from JSON file"""
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        with open(config_path, 'r') as f:
            data = json.load(f)
        
        return cls(**data)
    
    @classmethod
    def from_env(cls) -> 'WorkflowConfig':
        """Load configuration from environment variables"""
        required_vars = ["DOCKER_IMAGE", "GITHUB_TOKEN", "REPO_OWNER", "REPO_NAME"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {missing_vars}")
        
        return cls(
            docker_image=os.getenv("DOCKER_IMAGE"),
            github_token=os.getenv("GITHUB_TOKEN"),
            repo_owner=os.getenv("REPO_OWNER"),
            repo_name=os.getenv("REPO_NAME"),
            base_branch=os.getenv("BASE_BRANCH", "main"),
            working_directory=os.getenv("WORKING_DIR", "/workspace")
        )