"""CrewAI tools for provider management"""
from crewai_tools import BaseTool
from typing import Dict, Any, Optional
from provider_manager import ProviderManager, OpenAIProvider, AnthropicProvider
import os

class ProviderManagerTool(BaseTool):
    name: str = "Provider Manager"
    description: str = "Manages AI providers and routes requests efficiently"
    
    def __init__(self):
        super().__init__()
        self.manager = ProviderManager()
        self._initialize_providers()
    
    def _initialize_providers(self):
        """Initialize available providers"""
        if os.getenv("OPENAI_API_KEY"):
            self.manager.add_provider(OpenAIProvider(os.getenv("OPENAI_API_KEY")))
        
        if os.getenv("ANTHROPIC_API_KEY"):
            self.manager.add_provider(AnthropicProvider(os.getenv("ANTHROPIC_API_KEY")))
    
    def _run(self, action: str, **kwargs) -> str:
        """Execute provider management actions"""
        try:
            if action == "generate":
                return self._generate_response(kwargs.get("prompt", ""), 
                                             kwargs.get("provider"))
            elif action == "get_metrics":
                return self._get_metrics()
            elif action == "get_best_provider":
                return self._get_best_provider()
            else:
                return f"Unknown action: {action}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _generate_response(self, prompt: str, provider_name: Optional[str] = None) -> str:
        if not prompt:
            return "Error: No prompt provided"
        
        if provider_name:
            provider = self.manager.get_provider(provider_name)
            if not provider:
                return f"Error: Provider '{provider_name}' not found"
        else:
            provider = self.manager.get_best_provider()
            if not provider:
                return "Error: No providers available"
        
        try:
            response = provider.generate_response(prompt)
            return f"[{provider.name}] {response}"
        except Exception as e:
            return f"Error from {provider.name}: {str(e)}"
    
    def _get_metrics(self) -> str:
        metrics = self.manager.get_all_metrics()
        result = "Provider Metrics:\n"
        for name, metric in metrics.items():
            result += f"- {name}: {metric.requests_count} requests, "
            result += f"{metric.error_rate:.2%} error rate, "
            result += f"{metric.avg_response_time:.3f}s avg response\n"
        return result
    
    def _get_best_provider(self) -> str:
        provider = self.manager.get_best_provider()
        return f"Best provider: {provider.name}" if provider else "No providers available"

class LoadBalancerTool(BaseTool):
    name: str = "Load Balancer"
    description: str = "Distributes requests across providers based on current load"
    
    def _run(self, providers_load: Dict[str, float]) -> str:
        """Simple load balancing logic"""
        if not providers_load:
            return "No provider load data available"
        
        # Find provider with lowest load
        best_provider = min(providers_load.items(), key=lambda x: x[1])
        return f"Route to: {best_provider[0]} (load: {best_provider[1]:.2f})"