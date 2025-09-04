from typing import Dict
from models import OperationType

class CostCalculator:
    """Calculate costs for different AI models and providers"""
    
    # Pricing per 1K tokens (input, output)
    MODEL_PRICING = {
        "gpt-4": (0.03, 0.06),
        "gpt-4-turbo": (0.01, 0.03),
        "gpt-3.5-turbo": (0.0015, 0.002),
        "claude-3-opus": (0.015, 0.075),
        "claude-3-sonnet": (0.003, 0.015),
        "claude-3-haiku": (0.00025, 0.00125),
    }
    
    def calculate_cost(self, model: str, input_tokens: int, output_tokens: int, 
                      operation_type: OperationType = OperationType.CHAT) -> float:
        """Calculate cost based on model and token usage"""
        if model not in self.MODEL_PRICING:
            raise ValueError(f"Unknown model: {model}")
        
        input_rate, output_rate = self.MODEL_PRICING[model]
        
        input_cost = (input_tokens / 1000) * input_rate
        output_cost = (output_tokens / 1000) * output_rate
        
        return round(input_cost + output_cost, 6)
    
    def get_supported_models(self) -> list:
        """Get list of supported models"""
        return list(self.MODEL_PRICING.keys())