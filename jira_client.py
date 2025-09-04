import requests
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class JiraConfig:
    url: str
    username: str
    token: str
    project_key: str
    
    @classmethod
    def from_env(cls) -> 'JiraConfig':
        import os
        return cls(
            url=os.getenv('JIRA_URL', ''),
            username=os.getenv('JIRA_USERNAME', ''),
            token=os.getenv('JIRA_TOKEN', ''),
            project_key=os.getenv('JIRA_PROJECT_KEY', '')
        )
    
    def validate(self) -> None:
        if not all([self.url, self.username, self.token, self.project_key]):
            raise ValueError("Missing required Jira configuration. Set JIRA_URL, JIRA_USERNAME, JIRA_TOKEN, JIRA_PROJECT_KEY")


class JiraClient:
    def __init__(self, config: JiraConfig):
        self.config = config
        self.config.validate()
        self.session = requests.Session()
        self.session.auth = (config.username, config.token)
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        url = f"{self.config.url.rstrip('/')}/rest/api/2/{endpoint}"
        
        try:
            response = self.session.request(method, url, json=data)
            response.raise_for_status()
            return response.json() if response.content else {}
        except requests.exceptions.RequestException as e:
            raise Exception(f"Jira API error: {e}")
    
    def create_ticket(self, summary: str, description: str, issue_type: str = "Task") -> str:
        """Create a Jira ticket and return the ticket key."""
        ticket_data = {
            "fields": {
                "project": {"key": self.config.project_key},
                "summary": summary,
                "description": description,
                "issuetype": {"name": issue_type}
            }
        }
        
        result = self._make_request("POST", "issue", ticket_data)
        return result["key"]
    
    def update_ticket(self, ticket_key: str, summary: Optional[str] = None, description: Optional[str] = None) -> None:
        """Update an existing Jira ticket."""
        fields = {}
        if summary:
            fields["summary"] = summary
        if description:
            fields["description"] = description
        
        if fields:
            update_data = {"fields": fields}
            self._make_request("PUT", f"issue/{ticket_key}", update_data)
    
    def get_ticket(self, ticket_key: str) -> Dict[str, Any]:
        """Get ticket details."""
        return self._make_request("GET", f"issue/{ticket_key}")


def plan_to_jira_format(plan_content: str, title: str = "") -> tuple[str, str]:
    """Convert plan content to Jira ticket format."""
    lines = plan_content.strip().split('\n')
    
    # Extract title from first line if not provided
    if not title and lines:
        first_line = lines[0].strip()
        if first_line.startswith('#'):
            title = first_line.lstrip('#').strip()
            lines = lines[1:]
        else:
            title = "Development Plan"
    
    # Format description for Jira
    description_lines = []
    for line in lines:
        line = line.rstrip()
        if line.startswith('##'):
            description_lines.append(f"h2. {line.lstrip('#').strip()}")
        elif line.startswith('#'):
            description_lines.append(f"h1. {line.lstrip('#').strip()}")
        elif line.startswith('- '):
            description_lines.append(f"* {line[2:]}")
        elif line.startswith('* '):
            description_lines.append(line)
        else:
            description_lines.append(line)
    
    description = '\n'.join(description_lines)
    return title, description