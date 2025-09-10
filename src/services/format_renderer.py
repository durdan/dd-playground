import json
import yaml
from typing import Dict, Any
from ..models.specification_models import SpecificationOutput, OutputFormat, SpecificationSection

class FormatRenderer:
    @staticmethod
    def render(specification: SpecificationOutput) -> str:
        if specification.format == OutputFormat.JSON:
            return FormatRenderer._render_json(specification)
        elif specification.format == OutputFormat.MARKDOWN:
            return FormatRenderer._render_markdown(specification)
        elif specification.format == OutputFormat.YAML:
            return FormatRenderer._render_yaml(specification)
        else:
            raise ValueError(f"Unsupported format: {specification.format}")

    @staticmethod
    def _render_json(specification: SpecificationOutput) -> str:
        data = {
            "title": specification.title,
            "type": specification.specification_type.value,
            "sections": FormatRenderer._sections_to_dict(specification.sections),
            "metadata": specification.metadata
        }
        return json.dumps(data, indent=2)

    @staticmethod
    def _render_markdown(specification: SpecificationOutput) -> str:
        lines = [
            f"# {specification.title}",
            "",
            f"**Type:** {specification.specification_type.value.title()}",
            ""
        ]
        
        for section in specification.sections:
            lines.extend(FormatRenderer._section_to_markdown(section, level=2))
        
        if specification.metadata:
            lines.extend(["", "## Metadata", ""])
            for key, value in specification.metadata.items():
                lines.append(f"- **{key}:** {value}")
        
        return "\n".join(lines)

    @staticmethod
    def _render_yaml(specification: SpecificationOutput) -> str:
        data = {
            "title": specification.title,
            "type": specification.specification_type.value,
            "sections": FormatRenderer._sections_to_dict(specification.sections),
            "metadata": specification.metadata
        }
        return yaml.dump(data, default_flow_style=False, indent=2)

    @staticmethod
    def _sections_to_dict(sections: list) -> list:
        result = []
        for section in sections:
            section_dict = {
                "title": section.title,
                "content": section.content
            }
            if section.subsections:
                section_dict["subsections"] = FormatRenderer._sections_to_dict(section.subsections)
            result.append(section_dict)
        return result

    @staticmethod
    def _section_to_markdown(section: SpecificationSection, level: int = 2) -> list:
        lines = [
            f"{'#' * level} {section.title}",
            "",
            section.content,
            ""
        ]
        
        if section.subsections:
            for subsection in section.subsections:
                lines.extend(FormatRenderer._section_to_markdown(subsection, level + 1))
        
        return lines