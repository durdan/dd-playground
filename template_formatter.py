from typing import List
from template_types import TemplateSection

class TemplateFormatter:
    @staticmethod
    def to_markdown(title: str, version: str, sections: List[TemplateSection]) -> str:
        """Format template as Markdown."""
        output = [f"# {title}", f"**Version:** {version}", ""]
        
        for section in sections:
            output.extend(TemplateFormatter._format_section_markdown(section, 2))
            output.append("")
        
        return "\n".join(output)
    
    @staticmethod
    def _format_section_markdown(section: TemplateSection, level: int) -> List[str]:
        """Format a single section as Markdown."""
        lines = []
        header = "#" * level
        required_marker = " *(Required)*" if section.is_required else " *(Optional)*"
        lines.append(f"{header} {section.title}{required_marker}")
        
        if section.content:
            lines.append("")
            lines.append(section.content)
        
        for subsection in section.subsections:
            lines.append("")
            lines.extend(TemplateFormatter._format_section_markdown(subsection, level + 1))
        
        return lines
    
    @staticmethod
    def to_plain_text(title: str, version: str, sections: List[TemplateSection]) -> str:
        """Format template as plain text."""
        output = [title, "=" * len(title), f"Version: {version}", ""]
        
        for section in sections:
            output.extend(TemplateFormatter._format_section_text(section, 0))
            output.append("")
        
        return "\n".join(output)
    
    @staticmethod
    def _format_section_text(section: TemplateSection, indent_level: int) -> List[str]:
        """Format a single section as plain text."""
        lines = []
        indent = "  " * indent_level
        required_marker = " (Required)" if section.is_required else " (Optional)"
        lines.append(f"{indent}{section.title}{required_marker}")
        lines.append(f"{indent}{'-' * (len(section.title) + len(required_marker))}")
        
        if section.content:
            lines.append(f"{indent}{section.content}")
        
        for subsection in section.subsections:
            lines.append("")
            lines.extend(TemplateFormatter._format_section_text(subsection, indent_level + 1))
        
        return lines