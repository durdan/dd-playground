import requests
from typing import List, Dict, Any, Optional
from models import PullRequest, PRFile, ReviewComment, ReviewStatus
import json

class GitHubClient:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def get_pr_details(self, owner: str, repo: str, pr_number: int) -> PullRequest:
        """Fetch PR details and files"""
        pr_url = f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}"
        files_url = f"{pr_url}/files"
        
        pr_response = self._make_request(pr_url)
        files_response = self._make_request(files_url)
        
        if not pr_response or not files_response:
            raise ValueError(f"Failed to fetch PR {pr_number} details")
        
        files = [
            PRFile(
                filename=f["filename"],
                additions=f["additions"],
                deletions=f["deletions"],
                changes=f["changes"],
                patch=f.get("patch", ""),
                status=f["status"]
            )
            for f in files_response
        ]
        
        return PullRequest(
            number=pr_number,
            title=pr_response["title"],
            body=pr_response["body"] or "",
            author=pr_response["user"]["login"],
            base_branch=pr_response["base"]["ref"],
            head_branch=pr_response["head"]["ref"],
            files=files,
            repository=repo,
            owner=owner
        )
    
    def submit_review(self, owner: str, repo: str, pr_number: int, 
                     comments: List[ReviewComment], status: ReviewStatus, summary: str) -> bool:
        """Submit PR review with comments"""
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}/reviews"
        
        review_comments = []
        general_comment = summary
        
        for comment in comments:
            if comment.path and comment.line:
                review_comments.append({
                    "path": comment.path,
                    "line": comment.line,
                    "body": comment.body
                })
            else:
                general_comment += f"\n\n{comment.body}"
        
        data = {
            "body": general_comment,
            "event": self._status_to_event(status),
            "comments": review_comments
        }
        
        response = self._make_request(url, method="POST", data=data)
        return response is not None
    
    def merge_pr(self, owner: str, repo: str, pr_number: int) -> bool:
        """Auto-merge PR if conditions are met"""
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}/merge"
        data = {
            "commit_title": f"Auto-merge PR #{pr_number}",
            "merge_method": "squash"
        }
        
        response = self._make_request(url, method="PUT", data=data)
        return response is not None
    
    def _make_request(self, url: str, method: str = "GET", data: Dict = None) -> Optional[Dict]:
        """Make HTTP request to GitHub API"""
        try:
            if method == "GET":
                response = requests.get(url, headers=self.headers)
            elif method == "POST":
                response = requests.post(url, headers=self.headers, json=data)
            elif method == "PUT":
                response = requests.put(url, headers=self.headers, json=data)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"GitHub API request failed: {e}")
            return None
    
    def _status_to_event(self, status: ReviewStatus) -> str:
        """Convert review status to GitHub event"""
        mapping = {
            ReviewStatus.APPROVED: "APPROVE",
            ReviewStatus.CHANGES_REQUESTED: "REQUEST_CHANGES",
            ReviewStatus.COMMENTED: "COMMENT"
        }
        return mapping.get(status, "COMMENT")