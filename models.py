from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class ReviewType(str, Enum):
    SECURITY = "security"
    QUALITY = "quality"
    PERFORMANCE = "performance"

class Issue(BaseModel):
    type: ReviewType
    severity: str  # "low", "medium", "high", "critical"
    line_number: Optional[int]
    description: str
    suggestion: str

class ReviewResult(BaseModel):
    file_path: str
    issues: List[Issue]
    overall_score: int  # 1-10
    summary: str

class CodeReviewRequest(BaseModel):
    file_path: str
    code_content: str
    review_types: List[ReviewType] = [ReviewType.SECURITY, ReviewType.QUALITY, ReviewType.PERFORMANCE]