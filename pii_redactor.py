import re
from typing import List, Tuple
from models import PIIType, RedactionResult

class PIIRedactor:
    def __init__(self):
        self.patterns = {
            PIIType.EMAIL: r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            PIIType.SSN: r'\b\d{3}-?\d{2}-?\d{4}\b',
            PIIType.PHONE: r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            PIIType.CREDIT_CARD: r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'
        }
        self.redaction_char = '*'
    
    def redact_text(self, text: str, pii_types: List[PIIType] = None) -> RedactionResult:
        if not text:
            raise ValueError("Text cannot be empty")
        
        if pii_types is None:
            pii_types = list(PIIType)
        
        redacted_text = text
        found_pii = []
        total_redactions = 0
        
        for pii_type in pii_types:
            if pii_type in self.patterns:
                pattern = self.patterns[pii_type]
                matches = re.findall(pattern, redacted_text)
                
                if matches:
                    found_pii.append(pii_type)
                    total_redactions += len(matches)
                    redacted_text = re.sub(pattern, self._get_redaction_mask(pii_type), redacted_text)
        
        return RedactionResult(
            original_text=text,
            redacted_text=redacted_text,
            pii_found=found_pii,
            redaction_count=total_redactions
        )
    
    def _get_redaction_mask(self, pii_type: PIIType) -> str:
        masks = {
            PIIType.EMAIL: "[EMAIL_REDACTED]",
            PIIType.SSN: "[SSN_REDACTED]",
            PIIType.PHONE: "[PHONE_REDACTED]",
            PIIType.CREDIT_CARD: "[CARD_REDACTED]"
        }
        return masks.get(pii_type, "[PII_REDACTED]")