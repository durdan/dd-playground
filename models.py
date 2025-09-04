from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum

class ReviewStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    CHANGES_REQUESTED = "changes_requested"
    COMMENTED = "commented"

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
    body: str
    author: str
    base_branch: str
    head_branch: str
    files: List[PRFile]
    repository: str
    owner: str

@dataclass
class ReviewComment:
    body: str
    path: Optional[str] = None
    line: Optional[int] = None

@dataclass
class ReviewResult:
    status: ReviewStatus
    summary: str
    comments: List[ReviewComment]
    auto_merge: bool = False