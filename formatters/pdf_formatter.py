from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from models.specification import Specification
from formatters.base_formatter import BaseFormatter

class PDFFormatter(BaseFormatter):
    def format(self, spec: Specification, output_path: str) -> str:
        """Generate PDF format"""
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Custom styles with branding
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=24,
            textColor=colors.HexColor(self.branding.primary_color),
            spaceAfter=30
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor(self.branding.secondary_color),
            spaceBefore=20,
            spaceAfter=12
        )
        
        # Title page
        story.append(Paragraph(spec.title, title_style))
        story.append(Spacer(1, 20))
        
        # Metadata table
        metadata = [
            ['Company:', self.branding.company_name],
            ['Version:', spec.version],
            ['Created:', spec.created_at.strftime('%Y-%m-%d %H:%M:%S')],
        ]
        
        table = Table(metadata, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        
        story.append(table)
        story.append(PageBreak())
        
        # Table of contents
        story.append(Paragraph("Table of Contents", heading_style))
        for i, section in enumerate(spec.sections, 1):
            indent = "&nbsp;" * (section.level - 1) * 4
            toc_entry = f"{indent}{i}. {section.title}"
            story.append(Paragraph(toc_entry, styles['Normal']))
        
        story.append(PageBreak())
        
        # Content sections
        for section in spec.sections:
            if section.level == 1:
                story.append(Paragraph(section.title, heading_style))
            else:
                sub_style = ParagraphStyle(
                    f'Heading{section.level}',
                    parent=styles[f'Heading{min(section.level, 3)}'],
                    fontSize=14 - section.level,
                    spaceBefore=15,
                    spaceAfter=8
                )
                story.append(Paragraph(section.title, sub_style))
            
            # Process content paragraphs
            paragraphs = section.content.split('\n\n')
            for para in paragraphs:
                if para.strip():
                    story.append(Paragraph(para.strip(), styles['Normal']))
                    story.append(Spacer(1, 6))
        
        # Footer
        story.append(Spacer(1, 30))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.grey,
            alignment=1  # center
        )
        story.append(Paragraph(self.branding.footer_text, footer_style))
        
        doc.build(story)
        return output_path