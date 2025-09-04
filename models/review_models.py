from pydantic import BaseModel
from typing import List, Dict, Optional, Literal
from enum import Enum

class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ReviewType(str, Enum):
    SECURITY = "security"
    PERFORMANCE = "performance"
    ARCHITECTURE = "architecture"
    TESTING = "testing"

class Finding(BaseModel):
    line_number: Optional[int] = None
    severity: Severity
    category: str
    message: str
    suggestion: Optional[str] = None
    file_path: Optional[str] = None

class SpecialistReview(BaseModel):
    specialist_type: ReviewType
    findings: List[Finding]
    overall_score: int  # 1-10
    summary: str

class CodeReviewResult(BaseModel):
    file_paths: List[str]
    specialist_reviews: List[SpecialistReview]
    overall_score: int
    critical_issues: List[Finding]
    recommendations: List[str]