import pytest
from models import ReviewResult, Issue, ReviewType, CodeReviewRequest

def test_issue_creation():
    issue = Issue(
        type=ReviewType.SECURITY,
        severity="high",
        line_number=10,
        description="SQL injection vulnerability",
        suggestion="Use parameterized queries"
    )
    assert issue.type == ReviewType.SECURITY
    assert issue.severity == "high"
    assert issue.line_number == 10

def test_review_result_creation():
    issues = [
        Issue(
            type=ReviewType.SECURITY,
            severity="high",
            description="Test issue",
            suggestion="Fix it"
        )
    ]
    result = ReviewResult(
        file_path="test.py",
        issues=issues,
        overall_score=7,
        summary="Test summary"
    )
    assert result.file_path == "test.py"
    assert len(result.issues) == 1
    assert result.overall_score == 7

def test_code_review_request_defaults():
    request = CodeReviewRequest(
        file_path="test.py",
        code_content="print('hello')"
    )
    assert len(request.review_types) == 3
    assert ReviewType.SECURITY in request.review_types