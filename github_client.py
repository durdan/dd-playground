import requests
from typing import List, Optional
from models import PullRequest, PRFile
from config import GitHubConfig

class GitHubClient:
    def __init__(self, config: GitHubConfig):
        self.config = config
        self.headers = {
            'Authorization': f'token {config.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
    
    def get_pull_request(self, owner: str, repo: str, pr_number: int) -> PullRequest:
        """Fetch PR details and files."""
        pr_url = f"{self.config.base_url}/repos/{owner}/{repo}/pulls/{pr_number}"
        files_url = f"{pr_url}/files"
        
        # Get PR details
        pr_response = self._make_request(pr_url)
        if not pr_response:
            raise ValueError(f"PR #{pr_number} not found")
        
        # Get PR files
        files_response = self._make_request(files_url)
        if files_response is None:
            raise ValueError(f"Could not fetch files for PR #{pr_number}")
        
        files = [
            PRFile(
                filename=f['filename'],
                additions=f['additions'],
                deletions=f['deletions'],
                changes=f['changes'],
                patch=f.get('patch', ''),
                status=f['status']
            )
            for f in files_response
        ]
        
        return PullRequest(
            number=pr_response['number'],
            title=pr_response['title'],
            description=pr_response.get('body', ''),
            author=pr_response['user']['login'],
            base_branch=pr_response['base']['ref'],
            head_branch=pr_response['head']['ref'],
            files=files,
            url=pr_response['html_url']
        )
    
    def post_review_comment(self, owner: str, repo: str, pr_number: int, 
                          body: str, event: str = "COMMENT") -> bool:
        """Post a review comment on the PR."""
        url = f"{self.config.base_url}/repos/{owner}/{repo}/pulls/{pr_number}/reviews"
        data = {
            'body': body,
            'event': event  # APPROVE, REQUEST_CHANGES, COMMENT
        }
        
        response = self._make_request(url, method='POST', data=data)
        return response is not None
    
    def update_status(self, owner: str, repo: str, sha: str, 
                     state: str, description: str, context: str = "crew-ai-review") -> bool:
        """Update commit status."""
        url = f"{self.config.base_url}/repos/{owner}/{repo}/statuses/{sha}"
        data = {
            'state': state,  # pending, success, error, failure
            'description': description,
            'context': context
        }
        
        response = self._make_request(url, method='POST', data=data)
        return response is not None
    
    def _make_request(self, url: str, method: str = 'GET', data: Optional[dict] = None):
        """Make HTTP request with error handling."""
        try:
            if method == 'GET':
                response = requests.get(url, headers=self.headers)
            else:
                response = requests.post(url, headers=self.headers, json=data)
            
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"GitHub API error: {e}")
            return None