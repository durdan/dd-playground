import os
import openai
from abc import ABC, abstractmethod
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class AIClient(ABC):
    @abstractmethod
    def generate_specification(self, prompt: str, spec_type: str) -> str:
        pass

class OpenAIClient(AIClient):
    def __init__(self):
        self._api_key = self._get_api_key()
        openai.api_key = self._api_key
    
    def _get_api_key(self) -> str:
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        if len(api_key) < 20:  # Basic validation
            raise ValueError("Invalid API key format")
        return api_key
    
    def generate_specification(self, prompt: str, spec_type: str) -> str:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self._get_system_prompt(spec_type)},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"AI generation failed: {e}")
            raise RuntimeError(f"Failed to generate specification: {str(e)}")
    
    def _get_system_prompt(self, spec_type: str) -> str:
        prompts = {
            "business_analysis": "You are a business analyst. Generate detailed business analysis documentation.",
            "test_specs": "You are a QA engineer. Generate comprehensive test specifications.",
            "architecture_specs": "You are a software architect. Generate detailed architecture specifications."
        }
        return prompts.get(spec_type, "Generate professional technical documentation.")