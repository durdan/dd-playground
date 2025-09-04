from agents.base_agent import BaseAgent
from models import TaskRequest, AgentResponse, AgentRole, TaskStatus

class TestGenerator(BaseAgent):
    def __init__(self):
        super().__init__(AgentRole.TEST_GENERATOR)
    
    def process(self, request: TaskRequest) -> AgentResponse:
        """Generate test cases for the given task/code"""
        if not request.code and not request.description:
            return self._create_response(
                TaskStatus.FAILED,
                {},
                errors=["Need either code or description to generate tests"]
            )
        
        test_cases = []
        test_types = []
        
        # Generate different types of tests based on content
        if request.code:
            test_cases.extend(self._generate_unit_tests(request.code))
            test_types.append("unit")
        
        if request.description:
            test_cases.extend(self._generate_integration_tests(request.description))
            test_types.append("integration")
        
        # Generate edge case tests
        edge_cases = self._generate_edge_case_tests(request)
        test_cases.extend(edge_cases)
        
        if edge_cases:
            test_types.append("edge_case")
        
        feedback = [f"Generated {len(test_cases)} test cases"]
        suggestions = [
            "Review generated tests for completeness",
            "Consider adding performance tests for critical paths"
        ]
        
        return self._create_response(
            TaskStatus.COMPLETED,
            {
                "test_cases": test_cases,
                "test_types": test_types,
                "coverage_estimate": self._estimate_coverage(test_cases)
            },
            feedback=feedback,
            suggestions=suggestions
        )
    
    def _generate_unit_tests(self, code: str) -> list:
        """Generate unit test cases from code"""
        tests = []
        
        # Find function definitions
        lines = code.split('\n')
        for line in lines:
            if line.strip().startswith('def ') and not line.strip().startswith('def _'):
                func_name = line.split('def ')[1].split('(')[0]
                tests.append({
                    "type": "unit",
                    "name": f"test_{func_name}_success",
                    "description": f"Test {func_name} with valid input"
                })
                tests.append({
                    "type": "unit", 
                    "name": f"test_{func_name}_invalid_input",
                    "description": f"Test {func_name} with invalid input"
                })
        
        return tests
    
    def _generate_integration_tests(self, description: str) -> list:
        """Generate integration tests from description"""
        tests = []
        
        # Basic integration test based on description keywords
        if any(word in description.lower() for word in ['api', 'service', 'database']):
            tests.append({
                "type": "integration",
                "name": "test_end_to_end_workflow",
                "description": "Test complete workflow integration"
            })
        
        if 'user' in description.lower():
            tests.append({
                "type": "integration",
                "name": "test_user_interaction",
                "description": "Test user interaction scenarios"
            })
        
        return tests
    
    def _generate_edge_case_tests(self, request: TaskRequest) -> list:
        """Generate edge case tests"""
        tests = [
            {
                "type": "edge_case",
                "name": "test_empty_input",
                "description": "Test behavior with empty input"
            },
            {
                "type": "edge_case", 
                "name": "test_null_input",
                "description": "Test behavior with null/None input"
            }
        ]
        
        # Add specific edge cases based on requirements
        for req in request.requirements:
            if 'number' in req.lower():
                tests.append({
                    "type": "edge_case",
                    "name": "test_boundary_values",
                    "description": "Test with boundary numerical values"
                })
                break
        
        return tests
    
    def _estimate_coverage(self, test_cases: list) -> str:
        """Estimate test coverage based on number and types of tests"""
        if len(test_cases) >= 6:
            return "High"
        elif len(test_cases) >= 3:
            return "Medium"
        else:
            return "Low"