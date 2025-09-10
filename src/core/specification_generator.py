import re
from typing import List, Dict, Any
from ..models.specification_models import (
    SpecificationRequest, SpecificationOutput, SpecificationSection, OutputFormat
)
from ..clients.llm_client import LLMClient
from ..services.validation_service import ValidationService
from ..services.format_renderer import FormatRenderer

class SpecificationGenerator:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
        self.validation_service = ValidationService()

    def generate(self, request: SpecificationRequest) -> str:
        # Validate input
        self.validation_service.validate_request(request)
        
        # Generate raw specification content
        raw_content = self.llm_client.generate_specification(request)
        
        # Parse and structure the content
        specification = self._parse_specification(raw_content, request)
        
        # Validate output
        self.validation_service.validate_output(specification)
        
        # Render in requested format
        return FormatRenderer.render(specification)

    def _parse_specification(self, raw_content: str, request: SpecificationRequest) -> SpecificationOutput:
        sections = self._extract_sections(raw_content)
        metadata = self._extract_metadata(request, raw_content)
        
        return SpecificationOutput(
            title=request.title,
            specification_type=request.specification_type,
            sections=sections,
            metadata=metadata,
            raw_content=raw_content,
            format=request.output_format
        )

    def _extract_sections(self, content: str) -> List[SpecificationSection]:
        sections = []
        
        # Split content by headers (assuming markdown-style headers)
        header_pattern = r'^(#{1,6})\s+(.+)$'
        lines = content.split('\n')
        
        current_section = None
        current_content = []
        
        for line in lines:
            header_match = re.match(header_pattern, line)
            
            if header_match:
                # Save previous section if exists
                if current_section:
                    current_section.content = '\n'.join(current_content).strip()
                    sections.append(current_section)
                
                # Start new section
                header_level = len(header_match.group(1))
                title = header_match.group(2).strip()
                current_section = SpecificationSection(title=title, content="")
                current_content = []
            else:
                if current_section:
                    current_content.append(line)
        
        # Add final section
        if current_section:
            current_section.content = '\n'.join(current_content).strip()
            sections.append(current_section)
        
        # If no sections found, create a single section with all content
        if not sections:
            sections.append(SpecificationSection(
                title="Specification",
                content=content.strip()
            ))
        
        return sections

    def _extract_metadata(self, request: SpecificationRequest, raw_content: str) -> Dict[str, Any]:
        return {
            "generated_from": {
                "requirements_count": len(request.requirements),
                "has_constraints": bool(request.constraints),
                "has_context": bool(request.context)
            },
            "content_stats": {
                "character_count": len(raw_content),
                "line_count": len(raw_content.split('\n')),
                "word_count": len(raw_content.split())
            }
        }