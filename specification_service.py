import inspect
from typing import Dict, Any
from models import SpecificationRequest, SpecificationResponse
from specification_generator import SpecificationGenerator
from security_reviewer import SecurityReviewer
from ai_client import OpenAIClient

class SpecificationService:
    def __init__(self):
        self.ai_client = OpenAIClient()
        self.generator = SpecificationGenerator(self.ai_client)
        self.security_reviewer = SecurityReviewer()
    
    def generate_specification(self, request: SpecificationRequest) -> SpecificationResponse:
        # Generate specification
        content = self.generator.generate(request)
        
        # Perform security review
        review_passed, issues = self._perform_security_review()
        
        review_notes = None
        if issues:
            review_notes = "; ".join([f"{issue.severity}: {issue.description}" for issue in issues])
        
        return SpecificationResponse(
            content=content,
            spec_type=request.spec_type,
            security_review_passed=review_passed,
            review_notes=review_notes
        )
    
    def _perform_security_review(self) -> tuple:
        # Get AI client code for review
        ai_client_code = inspect.getsource(self.ai_client.__class__)
        
        # Simulate API usage metadata
        api_usage = {
            'uses_env_vars': True,
            'validates_key_format': True,
            'has_error_handling': True
        }
        
        return self.security_reviewer.review_ai_integration(ai_client_code, api_usage)