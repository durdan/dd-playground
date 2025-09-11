from typing import List, Dict, Tuple
from models.specification_template import SpecificationTemplate, TemplateSection

class ValidationResult:
    def __init__(self):
        self.is_valid = True
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.completeness_score = 0.0
    
    def add_error(self, message: str):
        self.errors.append(message)
        self.is_valid = False
    
    def add_warning(self, message: str):
        self.warnings.append(message)

class TaskVerifier:
    """Subagent specialized in validating template completeness and quality"""
    
    def __init__(self):
        self.required_sections_by_type = {
            "api_specification": [
                "overview", "endpoints", "authentication", 
                "data_models", "error_handling", "examples"
            ],
            "database_schema": [
                "overview", "tables", "relationships", 
                "indexes", "constraints", "migrations"
            ],
            "system_architecture": [
                "overview", "components", "data_flow", 
                "deployment", "scalability", "monitoring"
            ],
            "user_interface": [
                "overview", "wireframes", "components", 
                "user_flows", "responsive_design", "accessibility"
            ],
            "business_process": [
                "overview", "process_flow", "stakeholders", 
                "inputs_outputs", "success_criteria", "exceptions"
            ],
            "security_requirements": [
                "overview", "authentication", "authorization", 
                "data_protection", "network_security", "compliance"
            ]
        }
    
    def validate_template_completeness(self, template: SpecificationTemplate) -> ValidationResult:
        """Validate that template has all required sections and proper structure"""
        result = ValidationResult()
        
        # Basic validation
        self._validate_basic_fields(template, result)
        
        # Section validation
        self._validate_sections(template, result)
        
        # Completeness scoring
        result.completeness_score = self._calculate_completeness_score(template)
        
        return result
    
    def _validate_basic_fields(self, template: SpecificationTemplate, result: ValidationResult):
        """Validate basic template fields"""
        if not template.name or not template.name.strip():
            result.add_error("Template name is required")
        
        if not template.description or not template.description.strip():
            result.add_error("Template description is required")
        
        if not template.sections:
            result.add_error("Template must have at least one section")
        
        if template.mermaid_diagram and not self._is_valid_mermaid(template.mermaid_diagram):
            result.add_warning("Mermaid diagram syntax may be invalid")
    
    def _validate_sections(self, template: SpecificationTemplate, result: ValidationResult):
        """Validate template sections"""
        template_type_key = template.template_type.value
        required_sections = self.required_sections_by_type.get(template_type_key, [])
        
        section_names = [section.name.lower().replace(" ", "_") for section in template.sections]
        
        # Check for missing required sections
        for required in required_sections:
            if required not in section_names:
                result.add_error(f"Missing required section: {required}")
        
        # Validate individual sections
        for section in template.sections:
            self._validate_section(section, result)
    
    def _validate_section(self, section: TemplateSection, result: ValidationResult):
        """Validate individual section"""
        if not section.name or not section.name.strip():
            result.add_error("Section name is required")
        
        if not section.description or not section.description.strip():
            result.add_error(f"Section '{section.name}' must have a description")
        
        if section.required and not section.placeholder:
            result.add_warning(f"Required section '{section.name}' should have placeholder text")
    
    def _calculate_completeness_score(self, template: SpecificationTemplate) -> float:
        """Calculate completeness score (0.0 to 1.0)"""
        template_type_key = template.template_type.value
        required_sections = self.required_sections_by_type.get(template_type_key, [])
        
        if not required_sections:
            return 1.0
        
        section_names = [section.name.lower().replace(" ", "_") for section in template.sections]
        present_sections = sum(1 for req in required_sections if req in section_names)
        
        base_score = present_sections / len(required_sections)
        
        # Bonus points for additional quality indicators
        bonus = 0.0
        if template.mermaid_diagram:
            bonus += 0.1
        if any(section.validation_rules for section in template.sections):
            bonus += 0.05
        if all(section.placeholder for section in template.sections if section.required):
            bonus += 0.05
        
        return min(1.0, base_score + bonus)
    
    def _is_valid_mermaid(self, diagram: str) -> bool:
        """Basic Mermaid syntax validation"""
        diagram = diagram.strip()
        if not diagram:
            return False
        
        # Check for common Mermaid diagram types
        valid_starts = [
            'graph', 'flowchart', 'sequenceDiagram', 'classDiagram', 
            'erDiagram', 'gantt', 'pie', 'gitgraph'
        ]
        
        first_line = diagram.split('\n')[0].strip().lower()
        return any(first_line.startswith(start) for start in valid_starts)