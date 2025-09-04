from typing import Dict, Any, Optional
from datetime import datetime
import os
from dataclasses import asdict

from config import ReleaseDocConfig, DEFAULT_CONFIG
from audit_integration import AuditSystemInterface, ReleaseData
from template_engine import TemplateEngine

class ReleaseDocumentationError(Exception):
    """Custom exception for release documentation errors"""
    pass

class ReleaseDocGenerator:
    """Main class for generating automated release documentation"""
    
    def __init__(self, config: ReleaseDocConfig = DEFAULT_CONFIG):
        self.config = config
        self.audit_system = AuditSystemInterface()
        self.template_engine = TemplateEngine(config)
    
    def generate_release_doc(self, version: str, changes: list[str], 
                           start_date: Optional[datetime] = None,
                           end_date: Optional[datetime] = None) -> str:
        """Generate complete release documentation"""
        
        if not version or not version.strip():
            raise ReleaseDocumentationError("Version is required")
        
        if not changes:
            raise ReleaseDocumentationError("Changes list cannot be empty")
        
        # Set default dates if not provided
        end_date = end_date or datetime.now()
        start_date = start_date or datetime.now().replace(day=1)  # Start of month
        
        # Validate release readiness
        is_ready, errors = self.audit_system.validate_release_readiness(version)
        if not is_ready:
            raise ReleaseDocumentationError(f"Release not ready: {'; '.join(errors)}")
        
        # Gather all release data
        release_data = self._collect_release_data(version, changes, start_date, end_date)
        
        # Generate documentation
        doc_content = self._generate_documentation(release_data)
        
        # Save to file
        output_path = self._save_documentation(version, doc_content)
        
        return output_path
    
    def _collect_release_data(self, version: str, changes: list[str], 
                            start_date: datetime, end_date: datetime) -> ReleaseData:
        """Collect all data needed for release documentation"""
        
        audit_records = self.audit_system.get_audit_records_for_release(version, start_date, end_date)
        approvals = self.audit_system.get_approvals_for_release(version)
        deployment_info = self.audit_system.get_deployment_info(version)
        
        return ReleaseData(
            version=version,
            date=end_date,
            changes=changes,
            audit_records=audit_records,
            approvals=approvals,
            deployment=deployment_info
        )
    
    def _generate_documentation(self, release_data: ReleaseData) -> str:
        """Generate documentation content from release data"""
        
        # Prepare template variables
        template_vars = {
            'version': release_data.version,
            'date': release_data.date,
            'changes': release_data.changes,
            'audit_summary': self._format_audit_summary(release_data.audit_records),
            'approvals_summary': self._format_approvals_summary(release_data.approvals),
            'deployment_summary': self._format_deployment_summary(release_data.deployment)
        }
        
        return self.template_engine.render_template(self.config.default_template, template_vars)
    
    def _format_audit_summary(self, audit_records: list) -> str:
        """Format audit records for documentation"""
        if not audit_records:
            return "No audit records found"
        
        summary = []
        for record in audit_records:
            summary.append(f"- {record.action} by {record.user} on {record.timestamp.strftime('%Y-%m-%d')}")
        
        return "\n".join(summary)
    
    def _format_approvals_summary(self, approvals: list) -> str:
        """Format approval records for documentation"""
        if not approvals:
            return "No approvals recorded"
        
        summary = []
        for approval in approvals:
            status_emoji = "✅" if approval.status == "approved" else "❌" if approval.status == "rejected" else "⏳"
            summary.append(f"- {status_emoji} {approval.approver} ({approval.status})")
            if approval.comments:
                summary.append(f"  Comment: {approval.comments}")
        
        return "\n".join(summary)
    
    def _format_deployment_summary(self, deployment: dict) -> str:
        """Format deployment information"""
        if not deployment:
            return "No deployment information available"
        
        summary = []
        for key, value in deployment.items():
            summary.append(f"- {key.replace('_', ' ').title()}: {value}")
        
        return "\n".join(summary)
    
    def _save_documentation(self, version: str, content: str) -> str:
        """Save documentation to file"""
        filename = f"release_notes_{version.replace('.', '_')}.md"
        output_path = os.path.join(self.config.output_dir, filename)
        
        with open(output_path, 'w') as f:
            f.write(content)
        
        return output_path