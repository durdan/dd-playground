import json
from typing import Dict, Any, List
from .models import Endpoint, Parameter, Response

class ExampleGenerator:
    @staticmethod
    def format_request_example(endpoint: Endpoint) -> Dict[str, Any]:
        example = {
            "method": endpoint.method.value,
            "url": endpoint.path,
            "headers": {"Content-Type": "application/json"}
        }
        
        # Add path parameters
        if endpoint.path_params:
            path_with_examples = endpoint.path
            for param in endpoint.path_params:
                if param.example:
                    path_with_examples = path_with_examples.replace(
                        f"{{{param.name}}}", str(param.example)
                    )
            example["url"] = path_with_examples
        
        # Add query parameters
        if endpoint.query_params:
            query_params = {}
            for param in endpoint.query_params:
                if param.example is not None:
                    query_params[param.name] = param.example
            if query_params:
                example["query_params"] = query_params
        
        # Add request body
        if endpoint.request_body:
            example["body"] = endpoint.request_body
            
        return example
    
    @staticmethod
    def format_response_examples(responses: List[Response]) -> Dict[int, Dict[str, Any]]:
        examples = {}
        for response in responses:
            examples[response.status_code] = {
                "description": response.description,
                "body": response.example,
                "headers": response.headers
            }
        return examples

class ValidationHelper:
    @staticmethod
    def validate_endpoint(endpoint: Endpoint) -> List[str]:
        errors = []
        
        if not endpoint.path:
            errors.append("Path is required")
        
        if not endpoint.path.startswith('/'):
            errors.append("Path must start with '/'")
            
        if not endpoint.summary:
            errors.append("Summary is required")
            
        if not endpoint.description:
            errors.append("Description is required")
            
        # Validate path parameters exist in path
        for param in endpoint.path_params:
            if f"{{{param.name}}}" not in endpoint.path:
                errors.append(f"Path parameter '{param.name}' not found in path")
        
        return errors