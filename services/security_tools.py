import json
import re
from typing import List, Dict
from datetime import datetime
from models.security_report import Finding, ScanResult, SeverityLevel
from services.docker_manager import DockerManager
import logging

logger = logging.getLogger(__name__)

class SecurityToolBase:
    def __init__(self, docker_manager: DockerManager):
        self.docker_manager = docker_manager
        self.tool_name = ""
        self.image = ""
    
    def scan(self, target: str) -> ScanResult:
        raise NotImplementedError

class TrivyScanner(SecurityToolBase):
    def __init__(self, docker_manager: DockerManager):
        super().__init__(docker_manager)
        self.tool_name = "trivy"
        self.image = "aquasec/trivy:latest"
    
    def scan(self, target: str) -> ScanResult:
        """Scan for vulnerabilities using Trivy"""
        self.docker_manager.pull_image(self.image)
        
        command = ["trivy", "image", "--format", "json", target]
        stdout, stderr = self.docker_manager.run_security_tool(
            self.image, command
        )
        
        if stderr:
            logger.warning(f"Trivy stderr: {stderr}")
        
        findings = self._parse_trivy_output(stdout)
        summary = self._generate_summary(findings)
        
        return ScanResult(
            tool_name=self.tool_name,
            scan_type="vulnerability",
            target=target,
            timestamp=datetime.now(),
            findings=findings,
            summary=summary
        )
    
    def _parse_trivy_output(self, output: str) -> List[Finding]:
        findings = []
        try:
            data = json.loads(output) if output else {}
            results = data.get("Results", [])
            
            for result in results:
                vulnerabilities = result.get("Vulnerabilities", [])
                for vuln in vulnerabilities:
                    finding = Finding(
                        id=vuln.get("VulnerabilityID", ""),
                        title=vuln.get("Title", ""),
                        description=vuln.get("Description", ""),
                        severity=SeverityLevel(vuln.get("Severity", "info").lower()),
                        category="vulnerability",
                        file_path=result.get("Target", ""),
                        remediation=vuln.get("FixedVersion", "")
                    )
                    findings.append(finding)
        except Exception as e:
            logger.error(f"Failed to parse Trivy output: {e}")
        
        return findings
    
    def _generate_summary(self, findings: List[Finding]) -> Dict[str, int]:
        summary = {severity.value: 0 for severity in SeverityLevel}
        for finding in findings:
            summary[finding.severity.value] += 1
        return summary

class GitLeaksScanner(SecurityToolBase):
    def __init__(self, docker_manager: DockerManager):
        super().__init__(docker_manager)
        self.tool_name = "gitleaks"
        self.image = "zricethezav/gitleaks:latest"
    
    def scan(self, target: str) -> ScanResult:
        """Scan for secrets using GitLeaks"""
        self.docker_manager.pull_image(self.image)
        
        volumes = {target: {"bind": "/scan", "mode": "ro"}}
        command = ["detect", "--source", "/scan", "--report-format", "json", "--report-path", "/tmp/report.json", "--no-git"]
        
        stdout, stderr = self.docker_manager.run_security_tool(
            self.image, command, volumes=volumes
        )
        
        findings = self._parse_gitleaks_output(stdout)
        summary = self._generate_summary(findings)
        
        return ScanResult(
            tool_name=self.tool_name,
            scan_type="secrets",
            target=target,
            timestamp=datetime.now(),
            findings=findings,
            summary=summary
        )
    
    def _parse_gitleaks_output(self, output: str) -> List[Finding]:
        findings = []
        try:
            # GitLeaks outputs findings line by line in JSON format
            for line in output.strip().split('\n'):
                if line.strip():
                    data = json.loads(line)
                    finding = Finding(
                        id=data.get("Fingerprint", ""),
                        title=f"Secret detected: {data.get('RuleID', '')}",
                        description=data.get("Description", ""),
                        severity=SeverityLevel.HIGH,  # Secrets are typically high severity
                        category="secrets",
                        file_path=data.get("File", ""),
                        line_number=data.get("StartLine", 0),
                        remediation="Remove or encrypt the secret"
                    )
                    findings.append(finding)
        except Exception as e:
            logger.error(f"Failed to parse GitLeaks output: {e}")
        
        return findings
    
    def _generate_summary(self, findings: List[Finding]) -> Dict[str, int]:
        summary = {severity.value: 0 for severity in SeverityLevel}
        for finding in findings:
            summary[finding.severity.value] += 1
        return summary

class DockerBenchScanner(SecurityToolBase):
    def __init__(self, docker_manager: DockerManager):
        super().__init__(docker_manager)
        self.tool_name = "docker-bench"
        self.image = "docker/docker-bench-security:latest"
    
    def scan(self, target: str = "host") -> ScanResult:
        """Run Docker Bench Security checks"""
        self.docker_manager.pull_image(self.image)
        
        volumes = {
            "/var/run/docker.sock": {"bind": "/var/run/docker.sock", "mode": "ro"},
            "/usr/bin/docker": {"bind": "/usr/bin/docker", "mode": "ro"},
            "/etc": {"bind": "/host/etc", "mode": "ro"},
            "/var": {"bind": "/host/var", "mode": "ro"}
        }
        
        stdout, stderr = self.docker_manager.run_security_tool(
            self.image, [], volumes=volumes
        )
        
        findings = self._parse_docker_bench_output(stdout)
        summary = self._generate_summary(findings)
        
        return ScanResult(
            tool_name=self.tool_name,
            scan_type="compliance",
            target=target,
            timestamp=datetime.now(),
            findings=findings,
            summary=summary
        )
    
    def _parse_docker_bench_output(self, output: str) -> List[Finding]:
        findings = []
        try:
            lines = output.split('\n')
            for line in lines:
                if '[WARN]' in line or '[FAIL]' in line:
                    severity = SeverityLevel.HIGH if '[FAIL]' in line else SeverityLevel.MEDIUM
                    # Extract check ID and description
                    match = re.search(r'\[(WARN|FAIL)\]\s*(\d+\.\d+\.\d+)?\s*(.+)', line)
                    if match:
                        check_id = match.group(2) or "unknown"
                        description = match.group(3).strip()
                        
                        finding = Finding(
                            id=f"docker-bench-{check_id}",
                            title=f"Docker Bench Check {check_id}",
                            description=description,
                            severity=severity,
                            category="compliance",
                            remediation="Follow Docker security best practices"
                        )
                        findings.append(finding)
        except Exception as e:
            logger.error(f"Failed to parse Docker Bench output: {e}")
        
        return findings
    
    def _generate_summary(self, findings: List[Finding]) -> Dict[str, int]:
        summary = {severity.value: 0 for severity in SeverityLevel}
        for finding in findings:
            summary[finding.severity.value] += 1
        return summary