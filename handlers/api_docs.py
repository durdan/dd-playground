from typing import Dict, Any
from .base import SpecificationHandler
from ..exceptions import ValidationError

class ApiDocHandler(SpecificationHandler):
    """Handler for API documentation specifications"""
    
    def validate_input(self, input_data: Dict[str, Any]) -> None:
        required_fields = ["api_name", "endpoints"]
        for field in required_fields:
            if field not in input_data:
                raise ValidationError(f"Missing required field: {field}")
    
    def generate(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_input(input_data)
        
        content = {
            "title": f"API Documentation: {input_data['api_name']}",
            "sections": {
                "overview": self._generate_api_overview(input_data),
                "authentication": input_data.get("authentication", {}),
                "base_url": input_data.get("base_url", ""),
                "endpoints": self._process_endpoints(input_data["endpoints"]),
                "error_codes": input_data.get("error_codes", {}),
                "rate_limiting": input_data.get("rate_limiting", {})
            }
        }
        
        if self.config.include_examples:
            content["sections"]["examples"] = self._generate_api_examples()
        
        return self._add_metadata(content)
    
    def _generate_api_overview(self, input_data: Dict[str, Any]) -> str:
        return f"API documentation for {input_data['api_name']} - {input_data.get('description', '')}"
    
    def _process_endpoints(self, endpoints: list) -> list:
        processed = []
        for endpoint in endpoints:
            processed_endpoint = {
                "path": endpoint.get("path", ""),
                "method": endpoint.get("method", "GET"),
                "description": endpoint.get("description", ""),
                "parameters": endpoint.get("parameters", []),
                "request_body": endpoint.get("request_body", {}),
                "responses": endpoint.get("responses", {})
            }
            
            if self.config.detail_level == "high":
                processed_endpoint["headers"] = endpoint.get("headers", [])
                processed_endpoint["security"] = endpoint.get("security", [])
            
            processed.append(processed_endpoint)
        return processed
    
    def _generate_api_examples(self) -> Dict[str, Any]:
        return {
            "request_examples": ["Sample GET request", "Sample POST request"],
            "response_examples": ["Success response", "Error response"]
        }