import re
from typing import List, Dict, Set
from dataclasses import dataclass

@dataclass
class PIIMatch:
    pii_type: str
    value: str
    start: int
    end: int

class PIIDetector:
    def __init__(self):
        self.patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'phone': r'\b\d{3}-\d{3}-\d{4}\b',
            'credit_card': r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
            'ip_address': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
        }
    
    def detect_pii(self, text: str) -> List[PIIMatch]:
        """Detect PII in text using regex patterns"""
        if not text:
            return []
        
        matches = []
        for pii_type, pattern in self.patterns.items():
            for match in re.finditer(pattern, text):
                matches.append(PIIMatch(
                    pii_type=pii_type,
                    value=match.group(),
                    start=match.start(),
                    end=match.end()
                ))
        
        return matches
    
    def get_pii_types(self, text: str) -> Set[str]:
        """Get set of PII types found in text"""
        matches = self.detect_pii(text)
        return {match.pii_type for match in matches}
    
    def has_pii(self, text: str) -> bool:
        """Check if text contains any PII"""
        return len(self.detect_pii(text)) > 0