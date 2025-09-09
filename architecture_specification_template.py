from typing import List
from base_template import SpecificationTemplate
from template_types import TemplateSection

class ArchitectureSpecificationTemplate(SpecificationTemplate):
    def _create_sections(self) -> List[TemplateSection]:
        return [
            TemplateSection(
                title="Architecture Overview",
                subsections=[
                    TemplateSection("Purpose", "Purpose and scope of the architecture."),
                    TemplateSection("Architecture Goals", "Key architectural objectives and principles."),
                    TemplateSection("Constraints", "Technical and business constraints.")
                ]
            ),
            TemplateSection(
                title="System Context",
                subsections=[
                    TemplateSection("System Boundaries", "What is inside and outside the system."),
                    TemplateSection("External Dependencies", "External systems and services."),
                    TemplateSection("User Types", "Different types of system users.")
                ]
            ),
            TemplateSection(
                title="Architecture Views",
                subsections=[
                    TemplateSection("Logical View", "High-level system components and relationships."),
                    TemplateSection("Physical View", "Deployment and infrastructure architecture."),
                    TemplateSection("Process View", "Runtime behavior and interactions."),
                    TemplateSection("Development View", "Code organization and build structure.")
                ]
            ),
            TemplateSection(
                title="Component Design",
                subsections=[
                    TemplateSection("Core Components", "Main system components and their responsibilities."),
                    TemplateSection("Data Architecture", "Data models, storage, and flow."),
                    TemplateSection("Integration Architecture", "APIs, messaging, and communication.")
                ]
            ),
            TemplateSection(
                title="Quality Attributes",
                subsections=[
                    TemplateSection("Performance", "Performance requirements and design decisions."),
                    TemplateSection("Security", "Security architecture and measures."),
                    TemplateSection("Scalability", "Scalability considerations and patterns."),
                    TemplateSection("Reliability", "Fault tolerance and recovery mechanisms.")
                ]
            ),
            TemplateSection(
                title="Technology Stack",
                content="Selected technologies, frameworks, and tools with justification."
            ),
            TemplateSection(
                title="Architecture Decisions",
                content="Key architectural decisions and their rationale."
            )
        ]