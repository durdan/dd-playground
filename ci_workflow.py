import os
import logging
from typing import Optional
from .docker_executor import DockerExecutor, DockerResult
from .github_client import GitHubClient, PullRequest
from .workflow_config import WorkflowConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CIWorkflow:
    def __init__(self, config: WorkflowConfig):
        self.config = config
        self.docker_executor = DockerExecutor(
            image=config.docker_image,
            working_dir=config.working_directory
        )
        self.github_client = GitHubClient(
            token=config.github_token,
            repo_owner=config.repo_owner,
            repo_name=config.repo_name
        )
    
    def run_build(self) -> DockerResult:
        """Execute build commands in Docker"""
        logger.info("Starting build process...")
        result = self.docker_executor.run_command(
            command=self.config.build_commands,
            volumes=self.config.volumes,
            env_vars=self.config.env_vars
        )
        
        if result.success:
            logger.info("Build completed successfully")
        else:
            logger.error(f"Build failed: {result.stderr}")
        
        return result
    
    def run_tests(self) -> DockerResult:
        """Execute test commands in Docker"""
        logger.info("Starting test execution...")
        result = self.docker_executor.run_command(
            command=self.config.test_commands,
            volumes=self.config.volumes,
            env_vars=self.config.env_vars
        )
        
        if result.success:
            logger.info("Tests passed successfully")
        else:
            logger.error(f"Tests failed: {result.stderr}")
        
        return result
    
    def create_pr_from_results(self, build_result: DockerResult, test_result: DockerResult,
                              branch_name: str, pr_title: str) -> Optional[PullRequest]:
        """Create PR based on CI results"""
        if not build_result.success:
            logger.error("Cannot create PR: build failed")
            return None
        
        # Create PR body with CI results
        body_parts = [
            "## CI Results",
            "",
            f"**Build Status:** {'✅ Passed' if build_result.success else '❌ Failed'}",
            f"**Test Status:** {'✅ Passed' if test_result.success else '❌ Failed'}",
            ""
        ]
        
        if build_result.stdout:
            body_parts.extend([
                "### Build Output",
                "