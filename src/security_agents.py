from crewai import Agent, Task, Crew
from typing import List, Dict, Any
from .security_scanner import SecurityScanner, SecurityFinding
from .docker_manager import DockerManager

class SecurityAgents:
    def __init__(self):
        self.scanner = SecurityScanner()
        self.docker_manager = DockerManager()
        
    def create_vulnerability_agent(self) -> Agent:
        """Agent specialized in vulnerability scanning"""
        return Agent(
            role='Vulnerability Scanner',
            goal='Identify security vulnerabilities in Docker containers and images',
            backstory='Expert in container security with deep knowledge of CVEs and security best practices',
            verbose=True,
            allow_delegation=False
        )
    
    def create_compliance_agent(self) -> Agent:
        """Agent specialized in compliance checking"""
        return Agent(
            role='Compliance Auditor',
            goal='Ensure Docker containers comply with security standards and best practices',
            backstory='Security compliance expert familiar with CIS benchmarks and industry standards',
            verbose=True,
            allow_delegation=False
        )
    
    def create_secrets_agent(self) -> Agent:
        """Agent specialized in secrets detection"""
        return Agent(
            role='Secrets Detective',
            goal='Detect exposed secrets, credentials, and sensitive information',
            backstory='Cybersecurity specialist focused on preventing credential exposure and data leaks',
            verbose=True,
            allow_delegation=False
        )
    
    def create_vulnerability_task(self, container_ids: List[str], image_names: List[str]) -> Task:
        """Task for vulnerability scanning"""
        return Task(
            description=f"""
            Scan the following containers and images for vulnerabilities:
            Containers: {container_ids}
            Images: {image_names}
            
            Focus on:
            - Container configuration issues
            - Image layer analysis
            - Runtime security problems
            """,
            agent=self.create_vulnerability_agent(),
            expected_output="List of vulnerability findings with severity levels"
        )
    
    def create_compliance_task(self, container_ids: List[str]) -> Task:
        """Task for compliance checking"""
        return Task(
            description=f"""
            Check compliance for containers: {container_ids}
            
            Verify:
            - User permissions and privileges
            - Network security settings
            - Resource limitations
            - Security policies adherence
            """,
            agent=self.create_compliance_agent(),
            expected_output="Compliance assessment report with recommendations"
        )
    
    def create_secrets_task(self, container_ids: List[str]) -> Task:
        """Task for secrets detection"""
        return Task(
            description=f"""
            Scan containers for exposed secrets: {container_ids}
            
            Look for:
            - API keys and tokens
            - Database credentials
            - Private keys and certificates
            - Hardcoded passwords
            """,
            agent=self.create_secrets_agent(),
            expected_output="Report of detected secrets and exposure risks"
        )