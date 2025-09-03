from typing import List, Dict, Any
from .models import Endpoint
from .renderers import MarkdownRenderer, JSONRenderer
from .generators import ValidationHelper

class DocumentationGenerator:
    def __init__(self):
        self.markdown_renderer = MarkdownRenderer()
        self.json_renderer = JSONRenderer()
        self.validator = ValidationHelper()
    
    def generate_markdown(self, endpoints: List[Endpoint], title: str = "API Documentation") -> str:
        """Generate Markdown documentation from endpoints."""
        self._validate_endpoints(endpoints)
        return self.markdown_renderer.render(endpoints, title)
    
    def generate_json(self, endpoints: List[Endpoint], title: str = "API Documentation") -> str:
        """Generate JSON documentation from endpoints."""
        self._validate_endpoints(endpoints)
        return self.json_renderer.render(endpoints, title)
    
    def _validate_endpoints(self, endpoints: List[Endpoint]) -> None:
        """Validate all endpoints and raise error if any are invalid."""
        all_errors = []
        
        for i, endpoint in enumerate(endpoints):
            errors = self.validator.validate_endpoint(endpoint)
            if errors:
                endpoint_errors = [f"Endpoint {i+1} ({endpoint.method.value} {endpoint.path}): {error}" 
                                 for error in errors]
                all_errors.extend(endpoint_errors)
        
        if all_errors:
            raise ValueError("Validation errors:\n" + "\n".join(all_errors))