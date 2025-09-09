from abc import ABC, abstractmethod
from typing import List
from template_types import TemplateSection

class SpecificationTemplate(ABC):
    def __init__(self, title: str, version: str = "1.0"):
        self.title = title
        self.version = version
        self.sections = self._create_sections()
    
    @abstractmethod
    def _create_sections(self) -> List[TemplateSection]:
        """Create the sections specific to this template type."""
        pass
    
    def get_sections(self) -> List[TemplateSection]:
        return self.sections
    
    def add_custom_section(self, section: TemplateSection):
        """Add a custom section to the template."""
        self.sections.append(section)