from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class BrandingConfig:
    company_name: str = "TechSpec Solutions"
    logo_path: str = "assets/logo.png"
    primary_color: str = "#2E86AB"
    secondary_color: str = "#A23B72"
    font_family: str = "Arial"
    footer_text: str = "Confidential - Internal Use Only"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'company_name': self.company_name,
            'logo_path': self.logo_path,
            'primary_color': self.primary_color,
            'secondary_color': self.secondary_color,
            'font_family': self.font_family,
            'footer_text': self.footer_text
        }

# Default branding configuration
DEFAULT_BRANDING = BrandingConfig()