from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum

class ReviewStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    CHANGES_REQUESTED = "changes_requested"
    FAILED = "failed"

@dataclass
class PRFile:
    filename: str
    additions: int
    deletions: int
    changes: int
    patch: str
    status: str

@dataclass
class PullRequest:
    number: int
    title: str
    description: str
    author: str
    base_branch: str
    head_branch: str
    files: List[PRFile]
    url: str

@dataclass
class ReviewResult:
    agent_name: str
    score: float
    comments: List[str]
    suggestions: List[str]
    issues: List[str]
    
    def is_passing(self, threshold: float) -> bool:
        return self.score >= threshold

@dataclass
class QualityGateResult:
    overall_score: float
    status: ReviewStatus
    agent_results: Dict[str, ReviewResult]
    summary: str
    action_items: List[str]
    
    def is_passing(self, config: 'QualityGateConfig') -> bool:
        return (
            self.overall_score >= config.min_overall_score and
            self.status != ReviewStatus.FAILED
        )