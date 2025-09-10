from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

class TemplateType(Enum):
    BUSINESS_ANALYSIS = "business_analysis"
    TEST_SPECIFICATION = "test_specification"
    ARCHITECTURE_SPEC = "architecture_spec"
    TECHNICAL_REQUIREMENTS = "technical_requirements"

@dataclass
class TemplateSection:
    title: str
    content: str
    level: int = 1
    is_required: bool = True
    placeholder: str = ""

@dataclass
class Template:
    name: str
    description: str
    sections: List[TemplateSection] = field(default_factory=list)
    metadata: Dict[str, str] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

class ValidationError(Exception):
    pass

class TemplateGenerator:
    def __init__(self):
        self.templates = SpecificationTemplates()
    
    def generate(self, template_type: TemplateType, project_name: str = "Project") -> Template:
        if not isinstance(template_type, TemplateType):
            raise ValidationError(f"Invalid template type: {template_type}")
        
        if not project_name or not project_name.strip():
            raise ValidationError("Project name cannot be empty")
        
        generator_map = {
            TemplateType.BUSINESS_ANALYSIS: self.templates.business_analysis,
            TemplateType.TEST_SPECIFICATION: self.templates.test_specification,
            TemplateType.ARCHITECTURE_SPEC: self.templates.architecture_spec,
            TemplateType.TECHNICAL_REQUIREMENTS: self.templates.technical_requirements
        }
        
        return generator_map[template_type](project_name.strip())

class SpecificationTemplates:
    def business_analysis(self, project_name: str) -> Template:
        sections = [
            TemplateSection("Executive Summary", 
                          "Brief overview of the business analysis findings and recommendations.",
                          level=1, placeholder="Summarize key findings in 2-3 paragraphs"),
            
            TemplateSection("Business Objectives", 
                          "Primary business goals and success criteria.",
                          level=1, placeholder="List 3-5 key business objectives"),
            
            TemplateSection("Current State Analysis", 
                          "Assessment of existing business processes and systems.",
                          level=1, placeholder="Describe current processes, pain points, and limitations"),
            
            TemplateSection("Stakeholder Analysis", 
                          "Key stakeholders and their requirements.",
                          level=1, placeholder="List stakeholders, roles, and their specific needs"),
            
            TemplateSection("Requirements Gathering", 
                          "Functional and non-functional requirements.",
                          level=1),
            
            TemplateSection("Functional Requirements", 
                          "What the system must do.",
                          level=2, placeholder="List specific functional requirements with IDs"),
            
            TemplateSection("Non-Functional Requirements", 
                          "Performance, security, and quality requirements.",
                          level=2, placeholder="Define performance, security, usability requirements"),
            
            TemplateSection("Gap Analysis", 
                          "Differences between current and desired state.",
                          level=1, placeholder="Identify gaps and their business impact"),
            
            TemplateSection("Proposed Solution", 
                          "Recommended approach to address identified gaps.",
                          level=1, placeholder="Describe proposed solution and rationale"),
            
            TemplateSection("Implementation Roadmap", 
                          "Phased approach to implementation.",
                          level=1, placeholder="Define phases, timelines, and dependencies"),
            
            TemplateSection("Risk Assessment", 
                          "Potential risks and mitigation strategies.",
                          level=1, placeholder="List risks with probability, impact, and mitigation plans"),
            
            TemplateSection("Success Metrics", 
                          "Key performance indicators for measuring success.",
                          level=1, placeholder="Define measurable success criteria")
        ]
        
        return Template(
            name=f"{project_name} - Business Analysis Document",
            description="Comprehensive business analysis specification",
            sections=sections,
            metadata={
                "type": "business_analysis",
                "version": "1.0",
                "project": project_name
            }
        )
    
    def test_specification(self, project_name: str) -> Template:
        sections = [
            TemplateSection("Test Overview", 
                          "Purpose, scope, and objectives of testing.",
                          level=1, placeholder="Define what will be tested and why"),
            
            TemplateSection("Test Scope", 
                          "Features and components to be tested.",
                          level=2, placeholder="List in-scope and out-of-scope items"),
            
            TemplateSection("Test Approach", 
                          "Testing strategy and methodology.",
                          level=2, placeholder="Describe testing levels, types, and techniques"),
            
            TemplateSection("Test Environment", 
                          "Hardware, software, and network configurations.",
                          level=1, placeholder="Specify test environment requirements"),
            
            TemplateSection("Test Data Requirements", 
                          "Data needed for test execution.",
                          level=1, placeholder="Define test data types and sources"),
            
            TemplateSection("Test Cases", 
                          "Detailed test scenarios and expected results.",
                          level=1),
            
            TemplateSection("Functional Test Cases", 
                          "Tests for functional requirements.",
                          level=2, placeholder="List test cases with steps and expected results"),
            
            TemplateSection("Non-Functional Test Cases", 
                          "Performance, security, and usability tests.",
                          level=2, placeholder="Define performance and security test scenarios"),
            
            TemplateSection("Test Execution Schedule", 
                          "Timeline for test execution phases.",
                          level=1, placeholder="Define test phases and milestones"),
            
            TemplateSection("Entry and Exit Criteria", 
                          "Conditions for starting and completing testing.",
                          level=1, placeholder="Define when testing can start and when it's complete"),
            
            TemplateSection("Defect Management", 
                          "Process for reporting and tracking defects.",
                          level=1, placeholder="Define defect lifecycle and severity levels"),
            
            TemplateSection("Test Deliverables", 
                          "Documents and artifacts to be produced.",
                          level=1, placeholder="List all test deliverables and their formats")
        ]
        
        return Template(
            name=f"{project_name} - Test Specification",
            description="Comprehensive test specification document",
            sections=sections,
            metadata={
                "type": "test_specification",
                "version": "1.0",
                "project": project_name
            }
        )
    
    def architecture_spec(self, project_name: str) -> Template:
        sections = [
            TemplateSection("Architecture Overview", 
                          "High-level system architecture and design principles.",
                          level=1, placeholder="Describe overall architecture vision and principles"),
            
            TemplateSection("System Context", 
                          "External systems and interfaces.",
                          level=1, placeholder="Define system boundaries and external dependencies"),
            
            TemplateSection("Architecture Drivers", 
                          "Key requirements influencing architecture decisions.",
                          level=1, placeholder="List quality attributes, constraints, and assumptions"),
            
            TemplateSection("System Architecture", 
                          "Logical and physical system structure.",
                          level=1),
            
            TemplateSection("Logical Architecture", 
                          "High-level components and their relationships.",
                          level=2, placeholder="Describe major components and their interactions"),
            
            TemplateSection("Physical Architecture", 
                          "Deployment view and infrastructure components.",
                          level=2, placeholder="Define deployment topology and infrastructure"),
            
            TemplateSection("Component Design", 
                          "Detailed design of major components.",
                          level=1, placeholder="Describe component responsibilities and interfaces"),
            
            TemplateSection("Data Architecture", 
                          "Data models, storage, and flow.",
                          level=1, placeholder="Define data models, storage strategy, and data flow"),
            
            TemplateSection("Security Architecture", 
                          "Security controls and mechanisms.",
                          level=1, placeholder="Define authentication, authorization, and security measures"),
            
            TemplateSection("Integration Architecture", 
                          "APIs, messaging, and integration patterns.",
                          level=1, placeholder="Describe integration patterns and API design"),
            
            TemplateSection("Technology Stack", 
                          "Frameworks, libraries, and tools.",
                          level=1, placeholder="List technologies with rationale for selection"),
            
            TemplateSection("Architecture Decisions", 
                          "Key decisions and their rationale.",
                          level=1, placeholder="Document ADRs (Architecture Decision Records)")
        ]
        
        return Template(
            name=f"{project_name} - Architecture Specification",
            description="Comprehensive system architecture specification",
            sections=sections,
            metadata={
                "type": "architecture_spec",
                "version": "1.0",
                "project": project_name
            }
        )
    
    def technical_requirements(self, project_name: str) -> Template:
        sections = [
            TemplateSection("Introduction", 
                          "Purpose, scope, and audience of this document.",
                          level=1, placeholder="Define document purpose and target audience"),
            
            TemplateSection("System Overview", 
                          "High-level description of the system.",
                          level=1, placeholder="Provide system context and key capabilities"),
            
            TemplateSection("Functional Requirements", 
                          "What the system must do.",
                          level=1),
            
            TemplateSection("User Requirements", 
                          "Requirements from user perspective.",
                          level=2, placeholder="Define user stories and use cases"),
            
            TemplateSection("System Requirements", 
                          "Detailed functional system requirements.",
                          level=2, placeholder="List specific system functions with IDs"),
            
            TemplateSection("Non-Functional Requirements", 
                          "Quality attributes and constraints.",
                          level=1),
            
            TemplateSection("Performance Requirements", 
                          "Response time, throughput, and capacity.",
                          level=2, placeholder="Define performance benchmarks and limits"),
            
            TemplateSection("Security Requirements", 
                          "Authentication, authorization, and data protection.",
                          level=2, placeholder="Specify security controls and compliance needs"),
            
            TemplateSection("Reliability Requirements", 
                          "Availability, fault tolerance, and recovery.",
                          level=2, placeholder="Define uptime, MTBF, and recovery requirements"),
            
            TemplateSection("Usability Requirements", 
                          "User experience and accessibility.",
                          level=2, placeholder="Define UX standards and accessibility requirements"),
            
            TemplateSection("Technical Constraints", 
                          "Technology, platform, and integration constraints.",
                          level=1, placeholder="List technical limitations and dependencies"),
            
            TemplateSection("Interface Requirements", 
                          "External system interfaces and APIs.",
                          level=1, placeholder="Define external interfaces and data formats"),
            
            TemplateSection("Data Requirements", 
                          "Data models, storage, and migration needs.",
                          level=1, placeholder="Specify data requirements and migration needs"),
            
            TemplateSection("Compliance Requirements", 
                          "Regulatory and standards compliance.",
                          level=1, placeholder="List applicable regulations and standards")
        ]
        
        return Template(
            name=f"{project_name} - Technical Requirements Specification",
            description="Comprehensive technical requirements document",
            sections=sections,
            metadata={
                "type": "technical_requirements",
                "version": "1.0",
                "project": project_name
            }
        )

class TemplateFormatter:
    @staticmethod
    def to_markdown(template: Template) -> str:
        if not template:
            raise ValidationError("Template cannot be None")
        
        lines = [
            f"# {template.name}",
            "",
            f"**Description:** {template.description}",
            f"**Created:** {template.created_at}",
            f"**Version:** {template.metadata.get('version', 'N/A')}",
            ""
        ]
        
        for section in template.sections:
            header_prefix = "#" * (section.level + 1)
            lines.append(f"{header_prefix} {section.title}")
            lines.append("")
            
            if section.content:
                lines.append(section.content)
            
            if section.placeholder:
                lines.append(f"*{section.placeholder}*")
            
            lines.append("")
        
        return "\n".join(lines)
    
    @staticmethod
    def to_plain_text(template: Template) -> str:
        if not template:
            raise ValidationError("Template cannot be None")
        
        lines = [
            template.name.upper(),
            "=" * len(template.name),
            "",
            f"Description: {template.description}",
            f"Created: {template.created_at}",
            f"Version: {template.metadata.get('version', 'N/A')}",
            ""
        ]
        
        for section in template.sections:
            indent = "  " * (section.level - 1)
            lines.append(f"{indent}{section.title}")
            lines.append(f"{indent}{'-' * len(section.title)}")
            
            if section.content:
                lines.append(f"{indent}{section.content}")
            
            if section.placeholder:
                lines.append(f"{indent}[{section.placeholder}]")
            
            lines.append("")
        
        return "\n".join(lines)