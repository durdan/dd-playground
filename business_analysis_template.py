from typing import List
from base_template import SpecificationTemplate
from template_types import TemplateSection

class BusinessAnalysisTemplate(SpecificationTemplate):
    def _create_sections(self) -> List[TemplateSection]:
        return [
            TemplateSection(
                title="Executive Summary",
                content="Brief overview of the business analysis findings and recommendations."
            ),
            TemplateSection(
                title="Business Context",
                subsections=[
                    TemplateSection("Current State Analysis", "Description of current business processes and systems."),
                    TemplateSection("Problem Statement", "Clear definition of business problems to be addressed."),
                    TemplateSection("Stakeholder Analysis", "Identification and analysis of key stakeholders.")
                ]
            ),
            TemplateSection(
                title="Requirements Analysis",
                subsections=[
                    TemplateSection("Functional Requirements", "Detailed functional requirements."),
                    TemplateSection("Non-Functional Requirements", "Performance, security, and other quality requirements."),
                    TemplateSection("Business Rules", "Key business rules and constraints.")
                ]
            ),
            TemplateSection(
                title="Solution Options",
                subsections=[
                    TemplateSection("Option 1", "Description of first solution option."),
                    TemplateSection("Option 2", "Description of second solution option."),
                    TemplateSection("Recommendation", "Recommended solution with justification.")
                ]
            ),
            TemplateSection(
                title="Impact Analysis",
                subsections=[
                    TemplateSection("Cost-Benefit Analysis", "Financial impact assessment."),
                    TemplateSection("Risk Assessment", "Identification and mitigation of risks."),
                    TemplateSection("Change Impact", "Impact on people, processes, and technology.")
                ]
            ),
            TemplateSection(
                title="Implementation Plan",
                content="High-level implementation roadmap and timeline."
            ),
            TemplateSection(
                title="Appendices",
                content="Supporting documentation and references.",
                is_required=False
            )
        ]