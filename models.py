from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any, Optional


class SpecificationType(Enum):
    BUSINESS_ANALYSIS = "business_analysis"
    TEST_SPECS = "test_specs"
    ARCHITECTURE_SPECS = "architecture_specs"


@dataclass
class SpecificationRequest:
    spec_type: SpecificationType
    requirements: str
    context: Optional[Dict[str, Any]] = None
    max_tokens: Optional[int] = None


@dataclass
class SpecificationResponse:
    content: str
    spec_type: SpecificationType
    tokens_used: int
    processing_time: float