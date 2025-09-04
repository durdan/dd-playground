from github_client import GitHubClient
from crew_agents import PRReviewCrew
from models import PullRequest, ReviewResult
import logging

class PRProcessor:
    def __init__(self, github_client: GitHubClient, review_crew: PRReviewCrew):
        self.github_client = github_client
        self.review_crew = review_crew
        self.logger = logging.getLogger(__name__)
    
    def process_pr(self, owner: str, repo: str, pr_number: int) -> bool:
        """Process a PR through the complete review pipeline"""
        try:
            # Fetch PR details
            self.logger.info(f"Processing PR #{pr_number} in {owner}/{repo}")
            pr = self.github_client.get_pr_details(owner, repo, pr_number)
            
            # Skip if no files changed
            if not pr.files:
                self.logger.info(f"No files changed in PR #{pr_number}, skipping review")
                return True
            
            # Run multi-agent review
            self.logger.info(f"Starting multi-agent review for PR #{pr_number}")
            review_result = self.review_crew.review_pr(pr)
            
            # Submit review to GitHub
            success = self.github_client.submit_review(
                owner, repo, pr_number,
                review_result.comments,
                review_result.status,
                review_result.summary
            )
            
            if not success:
                self.logger.error(f"Failed to submit review for PR #{pr_number}")
                return False
            
            # Auto-merge if approved
            if review_result.auto_merge:
                self.logger.info(f"Auto-merging PR #{pr_number}")
                merge_success = self.github_client.merge_pr(owner, repo, pr_number)
                if not merge_success:
                    self.logger.warning(f"Auto-merge failed for PR #{pr_number}")
            
            self.logger.info(f"Successfully processed PR #{pr_number}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error processing PR #{pr_number}: {e}")
            return False