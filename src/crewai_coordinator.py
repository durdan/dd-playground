from crewai import Crew
from typing import List, Dict, Any
from .security_agents import SecurityAgents
from .docker_manager import DockerManager
from .security_scanner import SecurityScanner, SecurityFinding

class CrewAICoordinator:
    def __init__(self):
        self.security_agents = SecurityAgents()
        self.docker_manager = DockerManager()
        self.scanner = SecurityScanner()
    
    def coordinate_security_scan(self) -> Dict[str, Any]:
        """Coordinate comprehensive security scan using CrewAI agents"""
        
        # Get current Docker environment state
        containers = self.docker_manager.get_running_containers()
        images = self.docker_manager.get_images()
        
        container_ids = [c['id'] for c in containers]
        image_names = [tag for img in images for tag in img['tags'] if tag != '<none>:<none>']
        
        if not container_ids and not image_names:
            return {
                'status': 'no_targets',
                'message': 'No containers or images found to scan',
                'findings': []
            }
        
        # Create tasks for different security aspects
        tasks = []
        
        if container_ids:
            tasks.extend([
                self.security_agents.create_vulnerability_task(container_ids, image_names[:5]),  # Limit images
                self.security_agents.create_compliance_task(container_ids),
                self.security_agents.create_secrets_task(container_ids)
            ])
        
        if not tasks:
            return {
                'status': 'no_tasks',
                'message': 'No security tasks created',
                'findings': []
            }
        
        # Create and execute crew
        crew = Crew(
            agents=[task.agent for task in tasks],
            tasks=tasks,
            verbose=True
        )
        
        try:
            # Execute the crew (this would normally run the AI agents)
            # For this implementation, we'll run our actual security scans
            all_findings = []
            
            for container_id in container_ids:
                all_findings.extend(self.scanner.scan_container_vulnerabilities(container_id))
                all_findings.extend(self.scanner.scan_secrets(container_id))
            
            for image_name in image_names[:5]:  # Limit to first 5 images
                all_findings.extend(self.scanner.scan_image_vulnerabilities(image_name))
            
            return {
                'status': 'completed',
                'containers_scanned': len(container_ids),
                'images_scanned': min(len(image_names), 5),
                'findings': [self._finding_to_dict(f) for f in all_findings],
                'summary': self._generate_summary(all_findings)
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Security scan failed: {str(e)}',
                'findings': []
            }
    
    def _finding_to_dict(self, finding: SecurityFinding) -> Dict[str, Any]:
        """Convert SecurityFinding to dictionary"""
        return {
            'category': finding.category,
            'severity': finding.severity.value,
            'title': finding.title,
            'description': finding.description,
            'container_id': finding.container_id,
            'image_name': finding.image_name,
            'remediation': finding.remediation
        }
    
    def _generate_summary(self, findings: List[SecurityFinding]) -> Dict[str, Any]:
        """Generate summary statistics"""
        severity_counts = {}
        category_counts = {}
        
        for finding in findings:
            severity = finding.severity.value
            category = finding.category
            
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
            category_counts[category] = category_counts.get(category, 0) + 1
        
        return {
            'total_findings': len(findings),
            'by_severity': severity_counts,
            'by_category': category_counts
        }