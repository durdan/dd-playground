from typing import Dict, Any
import os
from datetime import datetime
from config import ReleaseDocConfig

class TemplateEngine:
    """Simple template engine for release documentation"""
    
    def __init__(self, config: ReleaseDocConfig):
        self.config = config
    
    def render_template(self, template_name: str, variables: Dict[str, Any]) -> str:
        """Render template with provided variables"""
        template_path = os.path.join(self.config.template_dir, template_name)
        
        if not os.path.exists(template_path):
            return self._get_default_template(variables)
        
        with open(template_path, 'r') as f:
            template_content = f.read()
        
        return self._substitute_variables(template_content, variables)
    
    def _substitute_variables(self, template: str, variables: Dict[str, Any]) -> str:
        """Simple variable substitution"""
        result = template
        for key, value in variables.items():
            placeholder = f"{{{{{key}}}}}"
            if isinstance(value, list):
                value = self._format_list(value)
            elif isinstance(value, datetime):
                value = value.strftime("%Y-%m-%d %H:%M:%S")
            result = result.replace(placeholder, str(value))
        return result
    
    def _format_list(self, items: list) -> str:
        """Format list items for documentation"""
        if not items:
            return "None"
        return "\n".join(f"- {item}" for item in items)
    
    def _get_default_template(self, variables: Dict[str, Any]) -> str:
        """Default template if none provided"""
        return f"""# Release Notes - Version {{version}}

**Release Date:** {{date}}

## Changes
{{changes}}

## Audit Trail
{{audit_summary}}

## Approvals
{{approvals_summary}}

## Deployment Information
{{deployment_summary}}

---
*Generated automatically on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""