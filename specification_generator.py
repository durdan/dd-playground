from models import SpecificationRequest, SpecificationType
from ai_client import AIClient

class SpecificationGenerator:
    def __init__(self, ai_client: AIClient):
        self.ai_client = ai_client
    
    def generate(self, request: SpecificationRequest) -> str:
        request.validate()
        
        prompt = self._build_prompt(request)
        return self.ai_client.generate_specification(prompt, request.spec_type.value)
    
    def _build_prompt(self, request: SpecificationRequest) -> str:
        base_prompt = f"Generate a {request.spec_type.value.replace('_', ' ')} for the following requirements:\n\n{request.requirements}"
        
        if request.context:
            context_str = "\n".join([f"{k}: {v}" for k, v in request.context.items()])
            base_prompt += f"\n\nAdditional context:\n{context_str}"
        
        return base_prompt