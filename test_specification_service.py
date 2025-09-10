import pytest
from unittest.mock import Mock, patch
from models import SpecificationRequest, SpecificationType
from specification_service import SpecificationService

@patch.dict('os.environ', {'OPENAI_API_KEY': 'sk-test-key-1234567890abcdef'})
def test_specification_service_integration():
    service = SpecificationService()
    
    # Mock the AI client to avoid actual API calls
    service.ai_client.generate_specification = Mock(return_value="Generated specification content")
    
    request = SpecificationRequest("Build a user management system", SpecificationType.BUSINESS_ANALYSIS)
    response = service.generate_specification(request)
    
    assert response.content == "Generated specification content"
    assert response.spec_type == SpecificationType.BUSINESS_ANALYSIS
    assert isinstance(response.security_review_passed, bool)

def test_specification_service_handles_invalid_request():
    service = SpecificationService()
    
    request = SpecificationRequest("", SpecificationType.BUSINESS_ANALYSIS)
    
    with pytest.raises(ValueError):
        service.generate_specification(request)