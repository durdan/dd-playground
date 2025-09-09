from typing import List
from base_template import SpecificationTemplate
from template_types import TemplateSection

class RequirementsTemplate(SpecificationTemplate):
    def _create_sections(self) -> List[TemplateSection]:
        return [
            TemplateSection(
                title="Introduction",
                subsections=[
                    TemplateSection("Purpose", "Purpose of this requirements document."),
                    TemplateSection("Scope", "Scope of the system or project."),
                    TemplateSection("Definitions", "Glossary of terms and abbreviations."),
                    TemplateSection("References", "Related documents and standards.")
                ]
            ),
            TemplateSection(
                title="Overall Description",
                subsections=[
                    TemplateSection("Product Perspective", "Relationship to other systems."),
                    TemplateSection("Product Functions", "Summary of major functions."),
                    TemplateSection("User Classes", "Different types of users."),
                    TemplateSection("Operating Environment", "Hardware and software environment."),
                    TemplateSection("Assumptions", "Assumptions made during requirements gathering.")
                ]
            ),
            TemplateSection(
                title="Functional Requirements",
                subsections=[
                    TemplateSection("User Management", "Requirements for user registration, authentication, etc."),
                    TemplateSection("Core Features", "Main functional requirements."),
                    TemplateSection("Reporting", "Reporting and analytics requirements."),
                    TemplateSection("Administration", "System administration requirements.")
                ]
            ),
            TemplateSection(
                title="Non-Functional Requirements",
                subsections=[
                    TemplateSection("Performance", "Response time, throughput, capacity requirements."),
                    TemplateSection("Security", "Authentication, authorization, data protection."),
                    TemplateSection("Usability", "User interface and user experience requirements."),
                    TemplateSection("Reliability", "Availability, fault tolerance, recovery."),
                    TemplateSection("Compatibility", "Browser, device, and system compatibility.")
                ]
            ),
            TemplateSection(
                title="Interface Requirements",
                subsections=[
                    TemplateSection("User Interfaces", "GUI requirements and mockups."),
                    TemplateSection("Hardware Interfaces", "Hardware interaction requirements."),
                    TemplateSection("Software Interfaces", "Integration with other systems."),
                    TemplateSection("Communication Interfaces", "Network and protocol requirements.")
                ]
            ),
            TemplateSection(
                title="Data Requirements",
                content="Data models, storage requirements, and data migration needs."
            ),
            TemplateSection(
                title="Acceptance Criteria",
                content="Criteria for accepting the delivered system."
            )
        ]