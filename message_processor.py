from typing import Dict, Any
from message_parser import MessageParser
from spec_type_identifier import SpecTypeIdentifier
from response_formatter import ResponseFormatter
from spec_types import ProcessingResult

class MessageProcessor:
    """Main orchestrator for intelligent message processing."""
    
    def __init__(self):
        self.parser = MessageParser()
        self.identifier = SpecTypeIdentifier()
        self.formatter = ResponseFormatter()
    
    def process_message(self, message: str) -> ProcessingResult:
        """Process user message and return formatted result."""
        if not message or not message.strip():
            raise ValueError("Message cannot be empty")
        
        # Extract requirements
        requirements = self.parser.extract_requirements(message)
        
        # Identify spec type
        spec_type = self.identifier.identify_spec_type(requirements)
        
        # Create metadata
        metadata = {
            'word_count': len(message.split()),
            'requirement_count': len(requirements),
            'confidence': self._calculate_confidence(spec_type, requirements)
        }
        
        # Format response
        formatted_response = self.formatter.format_response(spec_type, requirements, metadata)
        
        return ProcessingResult(
            original_message=message,
            extracted_requirements=requirements,
            spec_type=spec_type,
            formatted_response=formatted_response,
            metadata=metadata
        )
    
    def _calculate_confidence(self, spec_type, requirements) -> float:
        """Calculate confidence score for spec type identification."""
        if not requirements:
            return 0.0
        
        # Simple confidence based on keyword matches
        combined_text = ' '.join(requirements).lower()
        keywords = self.identifier.type_keywords.get(spec_type, [])
        matches = sum(1 for keyword in keywords if keyword in combined_text)
        
        return min(matches / len(keywords), 1.0) if keywords else 0.5