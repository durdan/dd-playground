import pytest
from security_reviewer import SecurityReviewer, SecurityIssue

def test_security_reviewer_detects_hardcoded_api_key():
    reviewer = SecurityReviewer()
    code_with_hardcoded_key = 'api_key = "sk-1234567890abcdef"'
    
    passed, issues = reviewer.review_ai_integration(code_with_hardcoded_key, {'uses_env_vars': True, 'validates_key_format': True})
    
    assert not passed
    assert len(issues) > 0
    assert any(issue.severity == "high" for issue in issues)

def test_security_reviewer_passes_secure_code():
    reviewer = SecurityReviewer()
    secure_code = 'api_key = os.getenv("OPENAI_API_KEY")\nvalidate()'
    
    passed, issues = reviewer.review_ai_integration(secure_code, {'uses_env_vars': True, 'validates_key_format': True})
    
    assert passed
    assert len([issue for issue in issues if issue.severity == "high"]) == 0

def test_security_reviewer_flags_missing_env_vars():
    reviewer = SecurityReviewer()
    
    passed, issues = reviewer.review_ai_integration("", {'uses_env_vars': False, 'validates_key_format': True})
    
    assert not passed
    assert any("environment variables" in issue.description for issue in issues)