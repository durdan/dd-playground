from typing import Dict, Any
from .base_generator import BaseFileGenerator

class PDFGenerator(BaseFileGenerator):
    def generate(self, specification: Dict[str, Any], output_path: str, options: Dict[str, Any]) -> None:
        """Generate PDF file from specification."""
        self.validate_specification(specification)
        
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
        except ImportError:
            raise ImportError("reportlab is required for PDF generation. Install with: pip install reportlab")
        
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
        )
        story.append(Paragraph(specification['title'], title_style))
        story.append(Spacer(1, 12))
        
        # Metadata
        if 'metadata' in specification:
            story.append(Paragraph("Metadata", styles['Heading2']))
            for key, value in specification['metadata'].items():
                story.append(Paragraph(f"<b>{key}:</b> {value}", styles['Normal']))
            story.append(Spacer(1, 12))
        
        # Content
        content = specification['content']
        if isinstance(content, str):
            story.append(Paragraph(content, styles['Normal']))
        elif isinstance(content, list):
            for item in content:
                if isinstance(item, dict):
                    if 'heading' in item:
                        story.append(Paragraph(item['heading'], styles['Heading2']))
                    if 'text' in item:
                        story.append(Paragraph(item['text'], styles['Normal']))
                        story.append(Spacer(1, 6))
                else:
                    story.append(Paragraph(str(item), styles['Normal']))
        
        # Sections
        if 'sections' in specification:
            for section in specification['sections']:
                story.append(Paragraph(section.get('title', 'Section'), styles['Heading2']))
                story.append(Paragraph(section.get('content', ''), styles['Normal']))
                story.append(Spacer(1, 12))
        
        doc.build(story)
    
    def get_file_extension(self) -> str:
        return "pdf"