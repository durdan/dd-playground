from typing import Dict, Any
from .base import SpecificationHandler
from ..exceptions import ValidationError

class BusinessAnalysisHandler(SpecificationHandler):
    """Handler for business analysis specifications"""
    
    def validate_input(self, input_data: Dict[str, Any]) -> None:
        required_fields = ["project_name", "business_objectives"]
        for field in required_fields:
            if field not in input_data:
                raise ValidationError(f"Missing required field: {field}")
    
    def generate(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_input(input_data)
        
        content = {
            "title": f"Business Analysis: {input_data['project_name']}",
            "sections": {
                "executive_summary": self._generate_executive_summary(input_data),
                "business_objectives": input_data["business_objectives"],
                "stakeholders": input_data.get("stakeholders", []),
                "requirements": self._generate_requirements(input_data),
                "risks": input_data.get("risks", []),
                "success_criteria": input_data.get("success_criteria", [])
            }
        }
        
        if self.config.include_examples:
            content["sections"]["examples"] = self._generate_examples()
        
        return self._add_metadata(content)
    
    def _generate_executive_summary(self, input_data: Dict[str, Any]) -> str:
        return f"Business analysis for {input_data['project_name']} focusing on achieving defined objectives."
    
    def _generate_requirements(self, input_data: Dict[str, Any]) -> list:
        base_requirements = input_data.get("requirements", [])
        if self.config.detail_level == "high":
            base_requirements.extend(["Detailed requirement analysis", "Impact assessment"])
        return base_requirements
    
    def _generate_examples(self) -> list:
        return ["Sample business case", "ROI calculation example"]