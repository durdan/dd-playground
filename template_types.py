from enum import Enum
from dataclasses import dataclass
from typing import List, Optional

class TemplateType(Enum):
    BUSINESS_ANALYSIS = "business_analysis"
    TEST_SPECIFICATION = "test_specification"
    ARCHITECTURE_SPECIFICATION = "architecture_specification"
    REQUIREMENTS_DOCUMENT = "requirements_document"

@dataclass
class TemplateSection:
    title: str
    content: str = ""
    subsections: List['TemplateSection'] = None
    is_required: bool = True
    
    def __post_init__(self):
        if self.subsections is None:
            self.subsections = []