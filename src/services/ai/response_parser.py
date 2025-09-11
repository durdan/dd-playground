import json
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from .prompt_templates import SpecType

logger = logging.getLogger(__name__)

@dataclass
class ParsedSpec:
    spec_type: SpecType
    content: Dict[str, Any]
    metadata: Dict[str, Any]
    validation_errors: List[str]

class ResponseParser:
    """Parse and validate AI responses into structured specifications"""
    
    def __init__(self):
        self.validators = {
            SpecType.API: self._validate_api_spec,
            SpecType.DATABASE: self._validate_database_spec,
            SpecType.COMPONENT: self._validate_component_spec,
            SpecType.SYSTEM: self._validate_system_spec
        }
    
    def parse_response(self, response: str, spec_type: SpecType) -> ParsedSpec:
        """Parse AI response into structured specification"""
        try:
            # Extract JSON from response (handle markdown code blocks)
            json_content = self._extract_json(response)
            
            # Parse JSON
            parsed_content = json.loads(json_content)
            
            # Validate structure
            validation_errors = self._validate_spec(parsed_content, spec_type)
            
            # Extract metadata
            metadata = self._extract_metadata(response, parsed_content)
            
            return ParsedSpec(
                spec_type=spec_type,
                content=parsed_content,
                metadata=metadata,
                validation_errors=validation_errors
            )
        
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from AI response: {e}")
            return ParsedSpec(
                spec_type=spec_type,
                content={},
                metadata={},
                validation_errors=[f"Invalid JSON: {str(e)}"]
            )
        except Exception as e:
            logger.error(f"Unexpected error parsing response: {e}")
            return ParsedSpec(
                spec_type=spec_type,
                content={},
                metadata={},
                validation_errors=[f"Parse error: {str(e)}"]
            )
    
    def _extract_json(self, response: str) -> str:
        """Extract JSON content from response, handling markdown code blocks"""
        response = response.strip()
        
        # Handle markdown code blocks
        if "