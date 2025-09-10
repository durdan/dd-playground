import re
from typing import List
from spec_types import ProcessingResult

class MessageParser:
    """Extracts and categorizes user requirements from input text."""
    
    def __init__(self):
        self.requirement_patterns = [
            r'(?:need|want|require|should|must|create|build|implement)\s+(.+?)(?:\.|$)',
            r'(?:how to|help me|can you)\s+(.+?)(?:\?|$)',
            r'(?:design|develop|make)\s+(.+?)(?:\.|$)'
        ]
    
    def extract_requirements(self, message: str) -> List[str]:
        """Extract requirements from user message."""
        if not message or not message.strip():
            raise ValueError("Message cannot be empty")
        
        requirements = []
        message_lower = message.lower()
        
        for pattern in self.requirement_patterns:
            matches = re.findall(pattern, message_lower, re.IGNORECASE)
            requirements.extend([match.strip() for match in matches if match.strip()])
        
        # Fallback: if no patterns match, treat entire message as requirement
        if not requirements:
            requirements = [message.strip()]
        
        return list(set(requirements))  # Remove duplicates