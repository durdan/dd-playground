from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class SpecificationConfig:
    """Configuration for specification generation"""
    template_style: str = "standard"
    detail_level: str = "medium"  # low, medium, high
    include_examples: bool = True
    include_diagrams: bool = False
    custom_sections: Optional[list] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.detail_level not in ["low", "medium", "high"]:
            raise ValueError("detail_level must be 'low', 'medium', or 'high'")
        if self.custom_sections is None:
            self.custom_sections = []
        if self.metadata is None:
            self.metadata = {}