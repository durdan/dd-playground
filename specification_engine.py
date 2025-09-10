from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum
import json

class SpecSection(Enum):
    OVERVIEW = "overview"
    FUNCTIONAL_REQUIREMENTS = "functional_requirements"
    NON_FUNCTIONAL_REQUIREMENTS = "non_functional_requirements"
    CONSTRAINTS = "constraints"
    ASSUMPTIONS = "assumptions"
    DEPENDENCIES = "dependencies"

@dataclass
class Requirement:
    id: str
    description: str
    priority: str  # High, Medium, Low
    category: str
    acceptance_criteria: List[str]

@dataclass
class SpecificationModel:
    title: str
    overview: str
    functional_requirements: List[Requirement]
    non_functional_requirements: List[Requirement]
    constraints: List[str]
    assumptions: List[str]
    dependencies: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'title': self.title,
            'overview': self.overview,
            'functional_requirements': [
                {
                    'id': req.id,
                    'description': req.description,
                    'priority': req.priority,
                    'category': req.category,
                    'acceptance_criteria': req.acceptance_criteria
                } for req in self.functional_requirements
            ],
            'non_functional_requirements': [
                {
                    'id': req.id,
                    'description': req.description,
                    'priority': req.priority,
                    'category': req.category,
                    'acceptance_criteria': req.acceptance_criteria
                } for req in self.non_functional_requirements
            ],
            'constraints': self.constraints,
            'assumptions': self.assumptions,
            'dependencies': self.dependencies
        }

@dataclass
class ValidationIssue:
    section: str
    severity: str  # Critical, Warning, Info
    message: str
    suggestion: Optional[str] = None

@dataclass
class ValidationResult:
    is_valid: bool
    score: float  # 0-100
    issues: List[ValidationIssue]
    summary: str