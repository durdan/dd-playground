from typing import Dict, Any
from .base import SpecificationHandler
from ..exceptions import ValidationError

class TestSpecHandler(SpecificationHandler):
    """Handler for test specification documents"""
    
    def validate_input(self, input_data: Dict[str, Any]) -> None:
        required_fields = ["feature_name", "test_scenarios"]
        for field in required_fields:
            if field not in input_data:
                raise ValidationError(f"Missing required field: {field}")
    
    def generate(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_input(input_data)
        
        content = {
            "title": f"Test Specification: {input_data['feature_name']}",
            "sections": {
                "test_overview": self._generate_test_overview(input_data),
                "test_scenarios": self._process_test_scenarios(input_data["test_scenarios"]),
                "test_data": input_data.get("test_data", {}),
                "environment": input_data.get("environment", "staging"),
                "acceptance_criteria": input_data.get("acceptance_criteria", [])
            }
        }
        
        if self.config.detail_level == "high":
            content["sections"]["detailed_steps"] = self._generate_detailed_steps()
        
        return self._add_metadata(content)
    
    def _generate_test_overview(self, input_data: Dict[str, Any]) -> str:
        return f"Comprehensive test specification for {input_data['feature_name']}"
    
    def _process_test_scenarios(self, scenarios: list) -> list:
        processed = []
        for scenario in scenarios:
            processed_scenario = {
                "name": scenario.get("name", "Unnamed scenario"),
                "steps": scenario.get("steps", []),
                "expected_result": scenario.get("expected_result", "")
            }
            if self.config.include_examples:
                processed_scenario["example_data"] = scenario.get("example_data", {})
            processed.append(processed_scenario)
        return processed
    
    def _generate_detailed_steps(self) -> list:
        return ["Setup test environment", "Execute test cases", "Validate results", "Cleanup"]