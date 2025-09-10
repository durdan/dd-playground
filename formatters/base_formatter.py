from abc import ABC, abstractmethod
from models.specification import Specification
from templates.branding import BrandingConfig

class BaseFormatter(ABC):
    def __init__(self, branding: BrandingConfig):
        self.branding = branding
    
    @abstractmethod
    def format(self, spec: Specification, output_path: str) -> str:
        """Format specification and save to output_path"""
        pass
    
    def sanitize_filename(self, filename: str) -> str:
        """Remove invalid characters from filename"""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename.strip()