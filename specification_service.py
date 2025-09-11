from typing import Dict, Any
from .models import SpecificationRequest, SpecificationResponse, SpecificationType
from .specification_generator import SpecificationGenerator
from .llm_client import LLMClient, OpenAIClient


class SpecificationService:
    """High-level service layer for specification generation."""
    
    def __init__(self, llm_client: LLMClient = None):
        self.generator = SpecificationGenerator(
            llm_client or self._create_default_client()
        )
    
    def generate_business_analysis(self, requirements: str, 
                                 context: Dict[str, Any] = None,
                                 max_tokens: int = None) -> SpecificationResponse:
        """Generate business analysis specification."""
        request = SpecificationRequest(
            spec_type=SpecificationType.BUSINESS_ANALYSIS,
            requirements=requirements,
            context=context,
            max_tokens=max_tokens
        )
        return self.generator.generate(request)
    
    def generate_test_specs(self, requirements: str,
                           context: Dict[str, Any] = None,
                           max_tokens: int = None) -> SpecificationResponse:
        """Generate test specifications."""
        request = SpecificationRequest(
            spec_type=SpecificationType.TEST_SPECS,
            requirements=requirements,
            context=context,
            max_tokens=max_tokens
        )
        return self.generator.generate(request)
    
    def generate_architecture_specs(self, requirements: str,
                                   context: Dict[str, Any] = None,
                                   max_tokens: int = None) -> SpecificationResponse:
        """Generate architecture specifications."""
        request = SpecificationRequest(
            spec_type=SpecificationType.ARCHITECTURE_SPECS,
            requirements=requirements,
            context=context,
            max_tokens=max_tokens
        )
        return self.generator.generate(request)
    
    def generate_specification(self, spec_type: str, requirements: str,
                             context: Dict[str, Any] = None,
                             max_tokens: int = None) -> SpecificationResponse:
        """Generate specification by type string."""
        try:
            spec_type_enum = SpecificationType(spec_type)
        except ValueError:
            raise ValueError(f"Unsupported specification type: {spec_type}")
        
        request = SpecificationRequest(
            spec_type=spec_type_enum,
            requirements=requirements,
            context=context,
            max_tokens=max_tokens
        )
        return self.generator.generate(request)
    
    def _create_default_client(self) -> LLMClient:
        """Create default LLM client (requires API key from environment)."""
        import os
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        return OpenAIClient(api_key)