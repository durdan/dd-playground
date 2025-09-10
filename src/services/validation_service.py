from typing import List, Optional
from ..models.specification_models import SpecificationRequest, SpecificationOutput

class ValidationError(Exception):
    pass

class ValidationService:
    @staticmethod
    def validate_request(request: SpecificationRequest) -> None:
        errors = []
        
        if not request.title or not request.title.strip():
            errors.append("Title is required")
        
        if not request.description or not request.description.strip():
            errors.append("Description is required")
        
        if not request.requirements or len(request.requirements) == 0:
            errors.append("At least one requirement is required")
        
        for i, req in enumerate(request.requirements):
            if not req or not req.strip():
                errors.append(f"Requirement {i+1} cannot be empty")
        
        if errors:
            raise ValidationError("; ".join(errors))

    @staticmethod
    def validate_output(output: SpecificationOutput) -> None:
        errors = []
        
        if not output.title or not output.title.strip():
            errors.append("Generated specification must have a title")
        
        if not output.sections or len(output.sections) == 0:
            errors.append("Generated specification must have at least one section")
        
        for i, section in enumerate(output.sections):
            if not section.title or not section.title.strip():
                errors.append(f"Section {i+1} must have a title")
            if not section.content or not section.content.strip():
                errors.append(f"Section {i+1} must have content")
        
        if errors:
            raise ValidationError("; ".join(errors))