from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Dict, Any

class SpecType(Enum):
    API = "api"
    UI = "ui"
    ALGORITHM = "algorithm"
    DATA_STRUCTURE = "data_structure"
    SYSTEM_DESIGN = "system_design"
    DATABASE = "database"
    GENERAL = "general"

@dataclass
class ProcessingResult:
    original_message: str
    extracted_requirements: List[str]
    spec_type: SpecType
    formatted_response: str
    metadata: Dict[str, Any]