from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from enum import Enum

class OutputFormat(Enum):
    JSON = "json"
    MARKDOWN = "markdown"
    YAML = "yaml"

class SpecificationType(Enum):
    FUNCTIONAL = "functional"
    TECHNICAL = "technical"
    API = "api"
    DATABASE = "database"
    UI_UX = "ui_ux"

@dataclass
class SpecificationRequest:
    title: str
    description: str
    requirements: List[str]
    specification_type: SpecificationType
    context: Optional[Dict[str, Any]] = None
    constraints: Optional[List[str]] = None
    output_format: OutputFormat = OutputFormat.JSON

@dataclass
class SpecificationSection:
    title: str
    content: str
    subsections: Optional[List['SpecificationSection']] = None

@dataclass
class SpecificationOutput:
    title: str
    specification_type: SpecificationType
    sections: List[SpecificationSection]
    metadata: Dict[str, Any]
    raw_content: str
    format: OutputFormat