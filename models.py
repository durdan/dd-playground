from enum import Enum
from dataclasses import dataclass
from typing import Optional, Dict, Any

class SpecificationType(Enum):
    BUSINESS_ANALYSIS = "business_analysis"
    TEST_SPECS = "test_specs"
    ARCHITECTURE_SPECS = "architecture_specs"

@dataclass
class SpecificationRequest:
    requirements: str
    spec_type: SpecificationType
    context: Optional[Dict[str, Any]] = None
    
    def validate(self) -> None:
        if not self.requirements or not self.requirements.strip():
            raise ValueError("Requirements cannot be empty")
        if len(self.requirements) > 10000:
            raise ValueError("Requirements too long (max 10000 characters)")

@dataclass
class SpecificationResponse:
    content: str
    spec_type: SpecificationType
    security_review_passed: bool
    review_notes: Optional[str] = None