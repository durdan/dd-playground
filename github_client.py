import requests
import json
from typing import Dict, Optional
from dataclasses import dataclass

@dataclass
class PullRequest:
    number: int
    title: str
    body: str
    head_branch: str
    base_branch: str
    url: str

class GitHubClient:
    def __init__(self, token: str, repo_owner: str, repo_name: str):
        if not token or not repo_owner or not repo_name:
            raise ValueError("Token, repo_owner, and repo_name are required")
        
        self.token = token
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def create_pull_request(self, title: str, body: str, head_branch: str, 
                          base_branch: str = "main") -> PullRequest:
        """Create a new pull request"""
        if not title or not head_branch:
            raise ValueError("Title and head_branch are required")
        
        url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/pulls"
        data = {
            "title": title,
            "body": body,
            "head": head_branch,
            "base": base_branch
        }
        
        response = requests.post(url, headers=self.headers, json=data)
        
        if response.status_code == 201:
            pr_data = response.json()
            return PullRequest(
                number=pr_data["number"],
                title=pr_data["title"],
                body=pr_data["body"],
                head_branch=pr_data["head"]["ref"],
                base_branch=pr_data["base"]["ref"],
                url=pr_data["html_url"]
            )
        else:
            raise RuntimeError(f"Failed to create PR: {response.status_code} - {response.text}")
    
    def update_pr_status(self, pr_number: int, status: str, description: str) -> bool:
        """Update PR status check"""
        # This would typically use the commit SHA, simplified for example
        return True  # Placeholder implementation