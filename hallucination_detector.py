import re
from typing import List, Dict
from .detector_types import SafetyIssue, RiskLevel, OperationType

class HallucinationDetector:
    def __init__(self):
        self.suspicious_patterns = [
            r'(?i)i\s+think|i\s+believe|probably|might\s+be|could\s+be',
            r'(?i)as\s+far\s+as\s+i\s+know|to\s+my\s+knowledge',
            r'(?i)fictional|example\.com|placeholder|dummy',
            r'(?i)xxx|yyy|zzz|foo|bar|baz',
        ]
        self.confidence_keywords = [
            'uncertain', 'unsure', 'maybe', 'perhaps', 'possibly'
        ]
    
    def detect_hallucination(self, content: str, context: Dict = None) -> List[SafetyIssue]:
        issues = []
        content_lower = content.lower()
        
        # Check for suspicious patterns
        for pattern in self.suspicious_patterns:
            if re.search(pattern, content):
                issues.append(SafetyIssue(
                    type=OperationType.DATABASE,  # Context-dependent
                    risk_level=RiskLevel.MEDIUM,
                    message="Content contains uncertain language patterns",
                    details={"pattern": pattern, "content_snippet": content[:100]},
                    confidence=0.7
                ))
        
        # Check for low confidence indicators
        confidence_score = self._calculate_confidence(content_lower)
        if confidence_score < 0.5:
            issues.append(SafetyIssue(
                type=OperationType.DATABASE,
                risk_level=RiskLevel.HIGH,
                message="Content shows low confidence indicators",
                details={"confidence_score": confidence_score},
                confidence=0.8
            ))
        
        # Check for fabricated technical details
        if self._has_fabricated_details(content):
            issues.append(SafetyIssue(
                type=OperationType.DATABASE,
                risk_level=RiskLevel.CRITICAL,
                message="Content may contain fabricated technical details",
                details={"indicators": "suspicious technical patterns"},
                confidence=0.9
            ))
        
        return issues
    
    def _calculate_confidence(self, content: str) -> float:
        confidence_hits = sum(1 for keyword in self.confidence_keywords if keyword in content)
        word_count = len(content.split())
        return max(0.0, 1.0 - (confidence_hits / max(word_count, 1)) * 5)
    
    def _has_fabricated_details(self, content: str) -> bool:
        # Check for suspicious technical patterns
        fabrication_patterns = [
            r'version\s+\d+\.\d+\.\d+\.\d+',  # Overly specific versions
            r'error\s+code\s+\d{4,}',  # Specific error codes
            r'port\s+\d{5}',  # Unusual port numbers
        ]
        return any(re.search(pattern, content, re.IGNORECASE) for pattern in fabrication_patterns)