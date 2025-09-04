import requests
import json
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class JiraConfig:
    base_url: str
    email: str
    api_token: str
    project_key: str


class JiraClient:
    def __init__(self, config: JiraConfig):
        self.config = config
        self.session = requests.Session()
        self.session.auth = (config.email, config.api_token)
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
    
    def test_connection(self) -> bool:
        """Test if we can connect to Jira with current credentials."""
        try:
            response = self.session.get(f"{self.config.base_url}/rest/api/3/myself")
            return response.status_code == 200
        except requests.RequestException:
            return False
    
    def get_project_info(self) -> Optional[Dict]:
        """Get project information to validate project key."""
        try:
            response = self.session.get(
                f"{self.config.base_url}/rest/api/3/project/{self.config.project_key}"
            )
            if response.status_code == 200:
                return response.json()
            return None
        except requests.RequestException:
            return None
    
    def create_issue(self, summary: str, description: str = "", issue_type: str = "Task") -> Optional[str]:
        """Create a Jira issue and return the issue key."""
        payload = {
            "fields": {
                "project": {"key": self.config.project_key},
                "summary": summary,
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": description
                                }
                            ]
                        }
                    ]
                },
                "issuetype": {"name": issue_type}
            }
        }
        
        try:
            response = self.session.post(
                f"{self.config.base_url}/rest/api/3/issue",
                data=json.dumps(payload)
            )
            
            if response.status_code == 201:
                return response.json()["key"]
            else:
                print(f"Failed to create issue: {response.status_code} - {response.text}")
                return None
        except requests.RequestException as e:
            print(f"Error creating issue: {e}")
            return None
    
    def sync_plan_tasks(self, tasks: List[str], plan_name: str = "Development Plan") -> List[str]:
        """Sync a list of tasks to Jira issues. Returns list of created issue keys."""
        created_issues = []
        
        for i, task in enumerate(tasks, 1):
            summary = f"{plan_name} - Task {i}: {task[:60]}..."  # Truncate long summaries
            description = f"Task from {plan_name}:\n\n{task}"
            
            issue_key = self.create_issue(summary, description)
            if issue_key:
                created_issues.append(issue_key)
                print(f"Created Jira issue: {issue_key}")
            else:
                print(f"Failed to create issue for task: {task[:50]}...")
        
        return created_issues