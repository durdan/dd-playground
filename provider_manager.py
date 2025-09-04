"""Existing provider manager - simplified version for demo"""
import os
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dataclasses import dataclass
import time

@dataclass
class ProviderMetrics:
    requests_count: int = 0
    avg_response_time: float = 0.0
    error_count: int = 0
    last_request_time: float = 0.0
    
    @property
    def error_rate(self) -> float:
        return self.error_count / max(self.requests_count, 1)

class AIProvider(ABC):
    def __init__(self, name: str):
        self.name = name
        self.metrics = ProviderMetrics()
    
    @abstractmethod
    def generate_response(self, prompt: str, **kwargs) -> str:
        pass
    
    def update_metrics(self, response_time: float, error: bool = False):
        self.metrics.requests_count += 1
        self.metrics.last_request_time = time.time()
        
        if error:
            self.metrics.error_count += 1
        else:
            # Simple moving average
            total_time = self.metrics.avg_response_time * (self.metrics.requests_count - 1)
            self.metrics.avg_response_time = (total_time + response_time) / self.metrics.requests_count

class OpenAIProvider(AIProvider):
    def __init__(self, api_key: str):
        super().__init__("openai")
        self.api_key = api_key
    
    def generate_response(self, prompt: str, **kwargs) -> str:
        start_time = time.time()
        try:
            # Simulate API call
            time.sleep(0.1)  # Mock response time
            response = f"OpenAI response to: {prompt[:50]}..."
            self.update_metrics(time.time() - start_time)
            return response
        except Exception as e:
            self.update_metrics(time.time() - start_time, error=True)
            raise

class AnthropicProvider(AIProvider):
    def __init__(self, api_key: str):
        super().__init__("anthropic")
        self.api_key = api_key
    
    def generate_response(self, prompt: str, **kwargs) -> str:
        start_time = time.time()
        try:
            # Simulate API call
            time.sleep(0.15)  # Mock response time
            response = f"Anthropic response to: {prompt[:50]}..."
            self.update_metrics(time.time() - start_time)
            return response
        except Exception as e:
            self.update_metrics(time.time() - start_time, error=True)
            raise

class ProviderManager:
    def __init__(self):
        self.providers: Dict[str, AIProvider] = {}
    
    def add_provider(self, provider: AIProvider):
        self.providers[provider.name] = provider
    
    def get_provider(self, name: str) -> Optional[AIProvider]:
        return self.providers.get(name)
    
    def get_best_provider(self) -> Optional[AIProvider]:
        """Select provider with lowest error rate and reasonable response time"""
        if not self.providers:
            return None
        
        available_providers = [p for p in self.providers.values() 
                             if p.metrics.error_rate < 0.5]  # Less than 50% error rate
        
        if not available_providers:
            return list(self.providers.values())[0]  # Fallback to first provider
        
        # Sort by error rate, then by response time
        return min(available_providers, 
                  key=lambda p: (p.metrics.error_rate, p.metrics.avg_response_time))
    
    def get_all_metrics(self) -> Dict[str, ProviderMetrics]:
        return {name: provider.metrics for name, provider in self.providers.items()}