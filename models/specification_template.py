from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
import uuid
from datetime import datetime

class TemplateType(Enum):
    API_SPECIFICATION = "api_specification"
    DATABASE_SCHEMA = "database_schema"
    SYSTEM_ARCHITECTURE = "system_architecture"
    USER_INTERFACE = "user_interface"
    BUSINESS_PROCESS = "business_process"
    SECURITY_REQUIREMENTS = "security_requirements"

@dataclass
class TemplateSection:
    name: str
    description: str
    required: bool = True
    placeholder: str = ""
    validation_rules: List[str] = field(default_factory=list)

@dataclass
class SpecificationTemplate:
    id: str
    name: str
    template_type: TemplateType
    description: str
    sections: List[TemplateSection]
    mermaid_diagram: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    version: str = "1.0.0"
    
    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())