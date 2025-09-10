from models.specification import Specification
from formatters.base_formatter import BaseFormatter

class MarkdownFormatter(BaseFormatter):
    def format(self, spec: Specification, output_path: str) -> str:
        """Generate Markdown format"""
        content = []
        
        # Header with branding
        content.append(f"# {spec.title}")
        content.append(f"**Company:** {self.branding.company_name}")
        content.append(f"**Version:** {spec.version}")
        content.append(f"**Created:** {spec.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        content.append("\n---\n")
        
        # Table of contents
        content.append("## Table of Contents")
        for i, section in enumerate(spec.sections, 1):
            indent = "  " * (section.level - 1)
            content.append(f"{indent}{i}. [{section.title}](#{self._anchor_link(section.title)})")
        content.append("\n")
        
        # Sections
        for section in spec.sections:
            heading = "#" * (section.level + 1)
            content.append(f"{heading} {section.title}")
            content.append(section.content)
            content.append("\n")
        
        # Footer
        content.append("---")
        content.append(f"*{self.branding.footer_text}*")
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))
        
        return output_path
    
    def _anchor_link(self, title: str) -> str:
        """Convert title to markdown anchor link"""
        return title.lower().replace(' ', '-').replace('/', '').replace('(', '').replace(')', '')