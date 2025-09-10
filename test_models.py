import pytest
from models import SpecificationRequest, SpecificationType

def test_specification_request_validation_success():
    request = SpecificationRequest("Valid requirements", SpecificationType.BUSINESS_ANALYSIS)
    request.validate()  # Should not raise

def test_specification_request_validation_empty_requirements():
    request = SpecificationRequest("", SpecificationType.BUSINESS_ANALYSIS)
    with pytest.raises(ValueError, match="Requirements cannot be empty"):
        request.validate()

def test_specification_request_validation_too_long():
    long_requirements = "x" * 10001
    request = SpecificationRequest(long_requirements, SpecificationType.BUSINESS_ANALYSIS)
    with pytest.raises(ValueError, match="Requirements too long"):
        request.validate()