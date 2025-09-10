from abc import ABC, abstractmethod
from typing import Dict, Any
import openai
import os
from ..models.specification_models import SpecificationRequest

class LLMClient(ABC):
    @abstractmethod
    def generate_specification(self, request: SpecificationRequest) -> str:
        pass

class OpenAIClient(LLMClient):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        openai.api_key = self.api_key

    def generate_specification(self, request: SpecificationRequest) -> str:
        prompt = self._build_prompt(request)
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self._get_system_prompt(request.specification_type)},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=4000,
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"Failed to generate specification: {str(e)}")

    def _build_prompt(self, request: SpecificationRequest) -> str:
        prompt_parts = [
            f"Title: {request.title}",
            f"Description: {request.description}",
            f"Requirements:",
        ]
        
        for i, req in enumerate(request.requirements, 1):
            prompt_parts.append(f"{i}. {req}")
        
        if request.constraints:
            prompt_parts.append("Constraints:")
            for constraint in request.constraints:
                prompt_parts.append(f"- {constraint}")
        
        if request.context:
            prompt_parts.append("Additional Context:")
            for key, value in request.context.items():
                prompt_parts.append(f"- {key}: {value}")
        
        return "\n".join(prompt_parts)

    def _get_system_prompt(self, spec_type: SpecificationType) -> str:
        base_prompt = """You are an expert software architect and technical writer. 
        Generate a comprehensive, well-structured specification document."""
        
        type_specific = {
            SpecificationType.FUNCTIONAL: "Focus on functional requirements, user stories, and business logic.",
            SpecificationType.TECHNICAL: "Focus on technical architecture, system design, and implementation details.",
            SpecificationType.API: "Focus on API endpoints, request/response formats, and integration patterns.",
            SpecificationType.DATABASE: "Focus on data models, relationships, and database schema design.",
            SpecificationType.UI_UX: "Focus on user interface design, user experience, and interaction patterns."
        }
        
        return f"{base_prompt} {type_specific.get(spec_type, '')}"