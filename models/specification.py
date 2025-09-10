from dataclasses import dataclass
from typing import List, Dict, Any
from datetime import datetime

@dataclass
class SpecificationSection:
    title: str
    content: str
    level: int = 1  # heading level
    metadata: Dict[str, Any] = None

@dataclass
class Specification:
    id: str
    title: str
    version: str
    created_at: datetime
    sections: List[SpecificationSection]
    metadata: Dict[str, Any] = None
    
    def validate(self) -> None:
        if not self.title.strip():
            raise ValueError("Specification title cannot be empty")
        if not self.sections:
            raise ValueError("Specification must have at least one section")
        for section in self.sections:
            if not section.title.strip():
                raise ValueError("Section title cannot be empty")