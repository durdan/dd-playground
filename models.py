from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum

class SpecificationType(Enum):
    FUNCTIONAL = "functional"
    TECHNICAL = "technical"
    UI_UX = "ui_ux"
    API = "api"
    DATABASE = "database"
    SECURITY = "security"
    PERFORMANCE = "performance"
    INTEGRATION = "integration"

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class Requirement:
    id: str
    text: str
    category: str
    priority: Priority
    entities: List[str]
    keywords: List[str]
    confidence: float

@dataclass
class SpecificationNeeds:
    types: List[SpecificationType]
    complexity: str  # simple, moderate, complex
    estimated_effort: str  # low, medium, high
    dependencies: List[str]

@dataclass
class StructuredInput:
    requirements: List[Requirement]
    specification_needs: SpecificationNeeds
    context: Dict[str, Any]
    metadata: Dict[str, Any]