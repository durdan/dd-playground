import json
from typing import List, Dict, Any
from .models import Endpoint, Parameter, Response
from .generators import ExampleGenerator, ValidationHelper

class MarkdownRenderer:
    def __init__(self):
        self.example_gen = ExampleGenerator()
    
    def render(self, endpoints: List[Endpoint], title: str = "API Documentation") -> str:
        md = [f"# {title}\n"]
        
        # Group endpoints by tags
        grouped = self._group_by_tags(endpoints)
        
        for tag, tag_endpoints in grouped.items():
            md.append(f"## {tag}\n")
            
            for endpoint in tag_endpoints:
                md.extend(self._render_endpoint(endpoint))
                md.append("---\n")
        
        return "\n".join(md)
    
    def _group_by_tags(self, endpoints: List[Endpoint]) -> Dict[str, List[Endpoint]]:
        grouped = {}
        for endpoint in endpoints:
            tags = endpoint.tags if endpoint.tags else ["General"]
            for tag in tags:
                if tag not in grouped:
                    grouped[tag] = []
                grouped[tag].append(endpoint)
        return grouped
    
    def _render_endpoint(self, endpoint: Endpoint) -> List[str]:
        md = []
        
        # Title and basic info
        md.append(f"### {endpoint.method.value} {endpoint.path}")
        md.append(f"**{endpoint.summary}**\n")
        md.append(f"{endpoint.description}\n")
        
        # Parameters
        if endpoint.path_params:
            md.append("#### Path Parameters")
            md.extend(self._render_parameters(endpoint.path_params))
        
        if endpoint.query_params:
            md.append("#### Query Parameters")
            md.extend(self._render_parameters(endpoint.query_params))
        
        # Request body
        if endpoint.request_body:
            md.append("#### Request Body")
            md.append("