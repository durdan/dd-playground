import ast
import inspect
from typing import List, Dict, Any
from crewai import Agent
from ..models.test_scenario import TestAnalysisResult, TestScenario, TestType, Priority

class TestAnalysisAgent(Agent):
    def __init__(self):
        super().__init__(
            role="Test Analysis Specialist",
            goal="Analyze code to identify comprehensive testing requirements and coverage gaps",
            backstory="Expert in static code analysis and test coverage assessment with deep understanding of software quality metrics",
            verbose=True
        )
    
    def analyze_code_file(self, file_path: str) -> TestAnalysisResult:
        """Analyze a Python file to identify testing needs."""
        try:
            with open(file_path, 'r') as file:
                source_code = file.read()
            
            tree = ast.parse(source_code)
            analyzer = CodeAnalyzer()
            
            functions = analyzer.extract_functions(tree)
            complexity_scores = analyzer.calculate_complexity(tree)
            coverage_gaps = analyzer.identify_coverage_gaps(file_path)
            risk_areas = analyzer.identify_risk_areas(tree)
            
            scenarios = self._generate_test_scenarios(functions, complexity_scores)
            
            return TestAnalysisResult(
                file_path=file_path,
                functions_analyzed=list(functions.keys()),
                coverage_gaps=coverage_gaps,
                complexity_scores=complexity_scores,
                suggested_scenarios=scenarios,
                risk_areas=risk_areas
            )
        except Exception as e:
            raise ValueError(f"Failed to analyze file {file_path}: {str(e)}")
    
    def _generate_test_scenarios(self, functions: Dict[str, Any], complexity_scores: Dict[str, int]) -> List[TestScenario]:
        """Generate initial test scenarios based on function analysis."""
        scenarios = []
        
        for func_name, func_info in functions.items():
            complexity = complexity_scores.get(func_name, 1)
            
            # Basic happy path test
            scenarios.append(TestScenario(
                name=f"test_{func_name}_happy_path",
                description=f"Test normal execution of {func_name}",
                test_type=TestType.UNIT,
                priority=Priority.HIGH,
                target_function=func_name,
                target_file=func_info.get('file', ''),
                inputs=self._infer_sample_inputs(func_info),
                expected_output=None  # To be determined by generation agent
            ))
            
            # Error handling tests for complex functions
            if complexity > 3:
                scenarios.append(TestScenario(
                    name=f"test_{func_name}_error_handling",
                    description=f"Test error handling in {func_name}",
                    test_type=TestType.ERROR_HANDLING,
                    priority=Priority.MEDIUM,
                    target_function=func_name,
                    target_file=func_info.get('file', ''),
                    inputs=self._generate_error_inputs(func_info),
                    expected_output="exception"
                ))
        
        return scenarios
    
    def _infer_sample_inputs(self, func_info: Dict[str, Any]) -> Dict[str, Any]:
        """Infer sample inputs based on function signature."""
        inputs = {}
        params = func_info.get('parameters', [])
        
        for param in params:
            param_name = param.get('name', '')
            param_type = param.get('type', 'Any')
            
            if 'int' in param_type.lower():
                inputs[param_name] = 42
            elif 'str' in param_type.lower():
                inputs[param_name] = "test_string"
            elif 'list' in param_type.lower():
                inputs[param_name] = [1, 2, 3]
            elif 'dict' in param_type.lower():
                inputs[param_name] = {"key": "value"}
            else:
                inputs[param_name] = None
        
        return inputs
    
    def _generate_error_inputs(self, func_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate inputs that should trigger error conditions."""
        error_inputs = {}
        params = func_info.get('parameters', [])
        
        for param in params:
            param_name = param.get('name', '')
            # Generate invalid inputs
            error_inputs[param_name] = None
        
        return error_inputs

class CodeAnalyzer:
    def extract_functions(self, tree: ast.AST) -> Dict[str, Dict[str, Any]]:
        """Extract function information from AST."""
        functions = {}
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions[node.name] = {
                    'name': node.name,
                    'parameters': self._extract_parameters(node),
                    'return_type': self._extract_return_type(node),
                    'docstring': ast.get_docstring(node),
                    'line_number': node.lineno
                }
        
        return functions
    
    def calculate_complexity(self, tree: ast.AST) -> Dict[str, int]:
        """Calculate cyclomatic complexity for functions."""
        complexity_scores = {}
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                complexity = 1  # Base complexity
                
                for child in ast.walk(node):
                    if isinstance(child, (ast.If, ast.While, ast.For, ast.Try)):
                        complexity += 1
                    elif isinstance(child, ast.BoolOp):
                        complexity += len(child.values) - 1
                
                complexity_scores[node.name] = complexity
        
        return complexity_scores
    
    def identify_coverage_gaps(self, file_path: str) -> List[str]:
        """Identify potential coverage gaps (simplified)."""
        # In a real implementation, this would integrate with coverage.py
        return ["Error handling paths", "Edge cases", "Integration scenarios"]
    
    def identify_risk_areas(self, tree: ast.AST) -> List[str]:
        """Identify high-risk areas that need thorough testing."""
        risk_areas = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Check for complex conditions
                if any(isinstance(child, ast.BoolOp) for child in ast.walk(node)):
                    risk_areas.append(f"Complex boolean logic in {node.name}")
                
                # Check for exception handling
                if any(isinstance(child, ast.Try) for child in ast.walk(node)):
                    risk_areas.append(f"Exception handling in {node.name}")
        
        return risk_areas
    
    def _extract_parameters(self, func_node: ast.FunctionDef) -> List[Dict[str, str]]:
        """Extract parameter information from function node."""
        parameters = []
        
        for arg in func_node.args.args:
            param_info = {'name': arg.arg}
            
            if arg.annotation:
                if isinstance(arg.annotation, ast.Name):
                    param_info['type'] = arg.annotation.id
                else:
                    param_info['type'] = 'Any'
            else:
                param_info['type'] = 'Any'
            
            parameters.append(param_info)
        
        return parameters
    
    def _extract_return_type(self, func_node: ast.FunctionDef) -> str:
        """Extract return type annotation."""
        if func_node.returns:
            if isinstance(func_node.returns, ast.Name):
                return func_node.returns.id
        return 'Any'