from typing import Dict, Any
from .base import SpecificationHandler
from ..exceptions import ValidationError

class ArchitectureSpecHandler(SpecificationHandler):
    """Handler for architecture specification documents"""
    
    def validate_input(self, input_data: Dict[str, Any]) -> None:
        required_fields = ["system_name", "components"]
        for field in required_fields:
            if field not in input_data:
                raise ValidationError(f"Missing required field: {field}")
    
    def generate(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_input(input_data)
        
        content = {
            "title": f"Architecture Specification: {input_data['system_name']}",
            "sections": {
                "overview": self._generate_overview(input_data),
                "components": self._process_components(input_data["components"]),
                "data_flow": input_data.get("data_flow", []),
                "security": input_data.get("security_requirements", {}),
                "scalability": input_data.get("scalability_requirements", {}),
                "deployment": input_data.get("deployment_strategy", {})
            }
        }
        
        if self.config.include_diagrams:
            content["sections"]["diagrams"] = self._generate_diagram_specs()
        
        return self._add_metadata(content)
    
    def _generate_overview(self, input_data: Dict[str, Any]) -> str:
        return f"Architecture specification for {input_data['system_name']} system"
    
    def _process_components(self, components: list) -> list:
        processed = []
        for component in components:
            processed_component = {
                "name": component.get("name", "Unnamed component"),
                "responsibility": component.get("responsibility", ""),
                "interfaces": component.get("interfaces", []),
                "dependencies": component.get("dependencies", [])
            }
            if self.config.detail_level == "high":
                processed_component["implementation_details"] = component.get("implementation_details", {})
            processed.append(processed_component)
        return processed
    
    def _generate_diagram_specs(self) -> list:
        return ["System context diagram", "Component diagram", "Deployment diagram"]