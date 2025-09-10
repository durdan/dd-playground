import re
from typing import Dict, Any
from spec_types import SpecType

class ResponseFormatter:
    """Formats AI responses with proper markdown and code highlighting."""
    
    def __init__(self):
        self.language_patterns = {
            r'\b(?:python|py)\b': 'python',
            r'\b(?:javascript|js)\b': 'javascript',
            r'\b(?:java)\b': 'java',
            r'\b(?:sql)\b': 'sql',
            r'\b(?:json)\b': 'json',
            r'\b(?:html)\b': 'html',
            r'\b(?:css)\b': 'css'
        }
    
    def format_response(self, spec_type: SpecType, requirements: list, metadata: Dict[str, Any]) -> str:
        """Format response based on spec type and requirements."""
        if not requirements:
            raise ValueError("Requirements cannot be empty")
        
        response_parts = []
        
        # Add header
        response_parts.append(f"# {spec_type.value.replace('_', ' ').title()} Specification\n")
        
        # Add requirements section
        response_parts.append("## Requirements")
        for i, req in enumerate(requirements, 1):
            response_parts.append(f"{i}. {req}")
        response_parts.append("")
        
        # Add spec-specific sections
        response_parts.extend(self._get_spec_sections(spec_type))
        
        # Add code example if applicable
        if self._should_include_code(spec_type):
            language = self._detect_language(' '.join(requirements))
            response_parts.append("## Implementation Example")
            response_parts.append(f"