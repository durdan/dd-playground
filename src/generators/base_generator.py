from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseFileGenerator(ABC):
    @abstractmethod
    def generate(self, specification: Dict[str, Any], output_path: str, options: Dict[str, Any]) -> None:
        """Generate file from specification."""
        pass
    
    @abstractmethod
    def get_file_extension(self) -> str:
        """Return file extension for this generator."""
        pass
    
    def validate_specification(self, specification: Dict[str, Any]) -> None:
        """Validate specification format."""
        if not isinstance(specification, dict):
            raise ValueError("Specification must be a dictionary")
        
        required_fields = ['title', 'content']
        for field in required_fields:
            if field not in specification:
                raise ValueError(f"Missing required field: {field}")