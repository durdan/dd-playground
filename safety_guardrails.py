import re
from typing import List, Dict, Tuple
from dataclasses import dataclass
from config import SafetyConfig, SafetyLevel

@dataclass
class SafetyViolation:
    level: SafetyLevel
    message: str
    content: str
    rule: str

class SafetyGuardrails:
    def __init__(self, config: SafetyConfig):
        self.config = config
        self._compile_patterns()
    
    def _compile_patterns(self):
        """Compile regex patterns for efficient matching."""
        self.keyword_patterns = [
            re.compile(rf'\b{re.escape(keyword)}\b', re.IGNORECASE)
            for keyword in self.config.blocked_keywords
        ]
    
    def check_content_safety(self, content: str) -> List[SafetyViolation]:
        """Check content against all safety rules."""
        violations = []
        
        # Check blocked keywords
        violations.extend(self._check_blocked_keywords(content))
        
        # Check toxicity (simulated)
        violations.extend(self._check_toxicity(content))
        
        # Check content length
        violations.extend(self._check_content_length(content))
        
        return violations
    
    def _check_blocked_keywords(self, content: str) -> List[SafetyViolation]:
        """Check for blocked keywords."""
        violations = []
        
        for pattern, keyword in zip(self.keyword_patterns, self.config.blocked_keywords):
            if pattern.search(content):
                violations.append(SafetyViolation(
                    level=SafetyLevel.HIGH,
                    message=f"Blocked keyword detected: {keyword}",
                    content=content[:100] + "..." if len(content) > 100 else content,
                    rule="blocked_keywords"
                ))
        
        return violations
    
    def _check_toxicity(self, content: str) -> List[SafetyViolation]:
        """Simulate toxicity detection."""
        # Simple heuristic - count negative words
        negative_words = ['hate', 'kill', 'destroy', 'attack', 'harm']
        toxicity_score = sum(1 for word in negative_words if word in content.lower()) / len(content.split())
        
        if toxicity_score > self.config.max_toxicity_score:
            violations = [SafetyViolation(
                level=SafetyLevel.MEDIUM,
                message=f"High toxicity score: {toxicity_score:.3f}",
                content=content[:100] + "..." if len(content) > 100 else content,
                rule="toxicity_check"
            )]
            return violations
        
        return []
    
    def _check_content_length(self, content: str) -> List[SafetyViolation]:
        """Check if content is suspiciously long or short."""
        violations = []
        
        if len(content) > 10000:
            violations.append(SafetyViolation(
                level=SafetyLevel.LOW,
                message="Content exceeds maximum length",
                content=content[:100] + "...",
                rule="max_length"
            ))
        elif len(content.strip()) == 0:
            violations.append(SafetyViolation(
                level=SafetyLevel.MEDIUM,
                message="Empty content detected",
                content="",
                rule="min_length"
            ))
        
        return violations
    
    def calculate_safety_score(self, violations: List[SafetyViolation]) -> float:
        """Calculate safety score based on violations."""
        if not violations:
            return 1.0
        
        penalty = 0.0
        for violation in violations:
            penalty += self.config.severity_thresholds[violation.level]
        
        return max(0.0, 1.0 - penalty)