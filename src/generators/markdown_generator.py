from typing import Dict, Any
from .base_generator import BaseFileGenerator

class MarkdownGenerator(BaseFileGenerator):
    def generate(self, specification: Dict[str, Any], output_path: str, options: Dict[str, Any]) -> None:
        """Generate Markdown file from specification."""
        self.validate_specification(specification)
        
        content = self._build_markdown_content(specification, options)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def get_file_extension(self) -> str:
        return "md"
    
    def _build_markdown_content(self, spec: Dict[str, Any], options: Dict[str, Any]) -> str:
        """Build markdown content from specification."""
        lines = []
        
        # Title
        lines.append(f"# {spec['title']}\n")
        
        # Metadata
        if 'metadata' in spec:
            lines.append("## Metadata\n")
            for key, value in spec['metadata'].items():
                lines.append(f"- **{key}**: {value}")
            lines.append("")
        
        # Main content
        if isinstance(spec['content'], str):
            lines.append(spec['content'])
        elif isinstance(spec['content'], list):
            for section in spec['content']:
                if isinstance(section, dict):
                    if 'heading' in section:
                        level = section.get('level', 2)
                        lines.append(f"{'#' * level} {section['heading']}\n")
                    if 'text' in section:
                        lines.append(section['text'] + "\n")
                else:
                    lines.append(str(section))
        
        # Sections
        if 'sections' in spec:
            for section in spec['sections']:
                lines.append(f"## {section.get('title', 'Section')}\n")
                lines.append(section.get('content', '') + "\n")
        
        return "\n".join(lines)