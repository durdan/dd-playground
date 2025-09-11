from typing import List, Optional
from models.specification_template import SpecificationTemplate, TemplateType
from subagents.mermaid_specialist import MermaidSpecialist
from subagents.task_verifier import TaskVerifier, ValidationResult
from repositories.template_repository import TemplateRepository

class TemplateService:
    """Business logic layer coordinating template operations with subagents"""
    
    def __init__(self, repository: TemplateRepository):
        self.repository = repository
        self.mermaid_specialist = MermaidSpecialist()
        self.task_verifier = TaskVerifier()
    
    def create_template(self, template: SpecificationTemplate) -> SpecificationTemplate:
        """Create a new template with validation and diagram generation"""
        # Validate template completeness
        validation_result = self.task_verifier.validate_template_completeness(template)
        if not validation_result.is_valid:
            raise ValueError(f"Template validation failed: {', '.join(validation_result.errors)}")
        
        # Generate Mermaid diagram if not provided
        if not template.mermaid_diagram:
            try:
                template.mermaid_diagram = self.mermaid_specialist.generate_structure_diagram(template)
            except ValueError as e:
                # Continue without diagram if generation fails
                pass
        
        return self.repository.save(template)
    
    def get_template(self, template_id: str) -> Optional[SpecificationTemplate]:
        """Get template by ID"""
        return self.repository.get_by_id(template_id)
    
    def list_templates(self, template_type: Optional[TemplateType] = None) -> List[SpecificationTemplate]:
        """List all templates, optionally filtered by type"""
        if template_type:
            return self.repository.get_by_type(template_type)
        return self.repository.get_all()
    
    def update_template(self, template: SpecificationTemplate) -> SpecificationTemplate:
        """Update existing template with validation"""
        validation_result = self.task_verifier.validate_template_completeness(template)
        if not validation_result.is_valid:
            raise ValueError(f"Template validation failed: {', '.join(validation_result.errors)}")
        
        return self.repository.save(template)
    
    def validate_template(self, template: SpecificationTemplate) -> ValidationResult:
        """Validate template and return detailed results"""
        return self.task_verifier.validate_template_completeness(template)
    
    def regenerate_diagram(self, template_id: str) -> SpecificationTemplate:
        """Regenerate Mermaid diagram for existing template"""
        template = self.repository.get_by_id(template_id)
        if not template:
            raise ValueError(f"Template not found: {template_id}")
        
        template.mermaid_diagram = self.mermaid_specialist.generate_structure_diagram(template)
        return self.repository.save(template)