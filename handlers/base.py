from abc import ABC, abstractmethod
from typing import Dict, Any
from ..config import SpecificationConfig

class SpecificationHandler(ABC):
    """Abstract base class for specification handlers"""
    
    def __init__(self, config: SpecificationConfig):
        self.config = config
    
    @abstractmethod
    def generate(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate specification content from input data"""
        pass
    
    @abstractmethod
    def validate_input(self, input_data: Dict[str, Any]) -> None:
        """Validate input data for this specification type"""
        pass
    
    def _add_metadata(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Add metadata to generated content"""
        content["metadata"] = {
            "generated_by": self.__class__.__name__,
            "config": self.config.__dict__,
            **self.config.metadata
        }
        return content