import time
from .models import SpecificationRequest, SpecificationResponse
from .prompt_optimizer import PromptOptimizer
from .llm_client import LLMClient


class SpecificationGenerator:
    """Core service for generating specifications using optimized prompts."""
    
    def __init__(self, llm_client: LLMClient):
        if not llm_client:
            raise ValueError("LLM client is required")
        
        self.llm_client = llm_client
        self.prompt_optimizer = PromptOptimizer()
    
    def generate(self, request: SpecificationRequest) -> SpecificationResponse:
        """Generate specification based on request."""
        self._validate_request(request)
        
        # Optimize prompt using subagent
        optimized_prompt = self.prompt_optimizer.optimize_prompt(
            request.spec_type,
            request.requirements,
            request.context
        )
        
        # Get optimized generation parameters
        generation_params = self.prompt_optimizer.get_generation_params(request.spec_type)
        
        # Override with user-specified max_tokens if provided
        if request.max_tokens:
            generation_params["max_tokens"] = request.max_tokens
        
        # Generate using LLM
        result = self.llm_client.generate(optimized_prompt, **generation_params)
        
        return SpecificationResponse(
            content=result["content"],
            spec_type=request.spec_type,
            tokens_used=result["tokens_used"],
            processing_time=result["processing_time"]
        )
    
    def _validate_request(self, request: SpecificationRequest) -> None:
        """Validate specification request."""
        if not request:
            raise ValueError("Request is required")
        
        if not request.requirements or not request.requirements.strip():
            raise ValueError("Requirements cannot be empty")
        
        if not isinstance(request.spec_type, type(request.spec_type.__class__)):
            raise ValueError("Invalid specification type")