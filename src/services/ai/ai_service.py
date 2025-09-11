import asyncio
import json
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum
import aiohttp
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

class AIProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    AZURE = "azure"

@dataclass
class AIConfig:
    provider: AIProvider
    api_key: str
    model: str
    base_url: Optional[str] = None
    max_tokens: int = 2000
    temperature: float = 0.7
    timeout: int = 30

class AIServiceError(Exception):
    """Base exception for AI service errors"""
    pass

class RateLimitError(AIServiceError):
    """Raised when API rate limit is exceeded"""
    pass

class InvalidResponseError(AIServiceError):
    """Raised when AI response cannot be parsed"""
    pass

class AIService:
    def __init__(self, config: AIConfig):
        self.config = config
        self._session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        self._session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.config.timeout)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._session:
            await self._session.close()
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def generate_completion(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> str:
        """Generate completion from AI service with retry logic"""
        if not self._session:
            raise AIServiceError("AI service not initialized. Use async context manager.")
        
        try:
            if self.config.provider == AIProvider.OPENAI:
                return await self._openai_completion(prompt, system_prompt, **kwargs)
            elif self.config.provider == AIProvider.ANTHROPIC:
                return await self._anthropic_completion(prompt, system_prompt, **kwargs)
            else:
                raise AIServiceError(f"Unsupported provider: {self.config.provider}")
        
        except aiohttp.ClientResponseError as e:
            if e.status == 429:
                raise RateLimitError(f"Rate limit exceeded: {e}")
            raise AIServiceError(f"API error: {e}")
        except asyncio.TimeoutError:
            raise AIServiceError("Request timeout")
        except Exception as e:
            logger.error(f"Unexpected error in AI service: {e}")
            raise AIServiceError(f"Unexpected error: {e}")
    
    async def _openai_completion(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> str:
        """OpenAI API completion"""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": self.config.model,
            "messages": messages,
            "max_tokens": kwargs.get("max_tokens", self.config.max_tokens),
            "temperature": kwargs.get("temperature", self.config.temperature)
        }
        
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json"
        }
        
        url = f"{self.config.base_url or 'https://api.openai.com'}/v1/chat/completions"
        
        async with self._session.post(url, json=payload, headers=headers) as response:
            response.raise_for_status()
            data = await response.json()
            return data["choices"][0]["message"]["content"]
    
    async def _anthropic_completion(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> str:
        """Anthropic API completion"""
        payload = {
            "model": self.config.model,
            "max_tokens": kwargs.get("max_tokens", self.config.max_tokens),
            "temperature": kwargs.get("temperature", self.config.temperature),
            "messages": [{"role": "user", "content": prompt}]
        }
        
        if system_prompt:
            payload["system"] = system_prompt
        
        headers = {
            "x-api-key": self.config.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        url = f"{self.config.base_url or 'https://api.anthropic.com'}/v1/messages"
        
        async with self._session.post(url, json=payload, headers=headers) as response:
            response.raise_for_status()
            data = await response.json()
            return data["content"][0]["text"]