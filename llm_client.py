from abc import ABC, abstractmethod
from typing import Dict, Any
import openai
import time


class LLMClient(ABC):
    """Abstract interface for LLM API integration."""
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate content using the LLM."""
        pass


class OpenAIClient(LLMClient):
    """OpenAI API client implementation."""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        if not api_key:
            raise ValueError("API key is required")
        
        openai.api_key = api_key
        self.model = model
    
    def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate content using OpenAI API."""
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty")
        
        start_time = time.time()
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=kwargs.get("max_tokens", 2000),
                temperature=kwargs.get("temperature", 0.3),
            )
            
            processing_time = time.time() - start_time
            
            return {
                "content": response.choices[0].message.content,
                "tokens_used": response.usage.total_tokens,
                "processing_time": processing_time
            }
            
        except openai.error.OpenAIError as e:
            raise RuntimeError(f"OpenAI API error: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error during generation: {str(e)}")