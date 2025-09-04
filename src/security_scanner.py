import docker
import json
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class SeverityLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class SecurityFinding:
    category: str
    severity: SeverityLevel
    title: str
    description: str
    container_id: Optional[str] = None
    image_name: Optional[str] = None
    remediation: Optional[str] = None

class SecurityScanner:
    def __init__(self):
        self.client = docker.from_env()
        self.secret_patterns = {
            'aws_access_key': r'AKIA[0-9A-Z]{16}',
            'private_key': r'-----BEGIN PRIVATE KEY-----',
            'password': r'password\s*[:=]\s*["\']?([^"\'\s]+)',
            'api_key': r'api[_-]?key\s*[:=]\s*["\']?([^"\'\s]+)',
        }
    
    def scan_container_vulnerabilities(self, container_id: str) -> List[SecurityFinding]:
        """Scan running container for vulnerabilities"""
        findings = []
        try:
            container = self.client.containers.get(container_id)
            
            # Check for privileged mode
            if container.attrs.get('HostConfig', {}).get('Privileged', False):
                findings.append(SecurityFinding(
                    category="container_config",
                    severity=SeverityLevel.HIGH,
                    title="Privileged Container",
                    description="Container running in privileged mode",
                    container_id=container_id,
                    remediation="Remove --privileged flag and use specific capabilities"
                ))
            
            # Check for root user
            config = container.attrs.get('Config', {})
            if config.get('User') in [None, '', '0', 'root']:
                findings.append(SecurityFinding(
                    category="container_config",
                    severity=SeverityLevel.MEDIUM,
                    title="Root User",
                    description="Container running as root user",
                    container_id=container_id,
                    remediation="Use non-root user in Dockerfile"
                ))
                
        except docker.errors.NotFound:
            findings.append(SecurityFinding(
                category="container_config",
                severity=SeverityLevel.LOW,
                title="Container Not Found",
                description=f"Container {container_id} not found",
                container_id=container_id
            ))
            
        return findings
    
    def scan_image_vulnerabilities(self, image_name: str) -> List[SecurityFinding]:
        """Scan Docker image for vulnerabilities"""
        findings = []
        try:
            image = self.client.images.get(image_name)
            
            # Check image history for suspicious layers
            history = image.history()
            for layer in history:
                created_by = layer.get('CreatedBy', '')
                if 'curl' in created_by and 'bash' in created_by:
                    findings.append(SecurityFinding(
                        category="image_security",
                        severity=SeverityLevel.MEDIUM,
                        title="Suspicious Layer Command",
                        description=f"Layer contains potentially risky command: {created_by[:100]}",
                        image_name=image_name,
                        remediation="Review and minimize RUN commands in Dockerfile"
                    ))
                    
        except docker.errors.ImageNotFound:
            findings.append(SecurityFinding(
                category="image_security",
                severity=SeverityLevel.LOW,
                title="Image Not Found",
                description=f"Image {image_name} not found",
                image_name=image_name
            ))
            
        return findings
    
    def scan_secrets(self, container_id: str) -> List[SecurityFinding]:
        """Scan container for exposed secrets"""
        findings = []
        try:
            container = self.client.containers.get(container_id)
            
            # Check environment variables
            env_vars = container.attrs.get('Config', {}).get('Env', [])
            for env_var in env_vars:
                for secret_type, pattern in self.secret_patterns.items():
                    if re.search(pattern, env_var, re.IGNORECASE):
                        findings.append(SecurityFinding(
                            category="secrets",
                            severity=SeverityLevel.HIGH,
                            title=f"Exposed {secret_type.replace('_', ' ').title()}",
                            description=f"Potential {secret_type} found in environment variables",
                            container_id=container_id,
                            remediation="Use secrets management system instead of environment variables"
                        ))
                        
        except docker.errors.NotFound:
            pass
            
        return findings