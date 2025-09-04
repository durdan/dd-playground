import os
import json
import random
from enum import Enum
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path

class TaskType(Enum):
    CODE_COMPLETION = "code_completion"
    BUG_FIXING = "bug_fixing"
    REFACTORING = "refactoring"
    DOCUMENTATION = "documentation"
    TEST_GENERATION = "test_generation"
    API_USAGE = "api_usage"
    ALGORITHM_IMPLEMENTATION = "algorithm_implementation"

@dataclass
class SyntheticTask:
    task_id: str
    task_type: TaskType
    description: str
    input_data: Dict[str, Any]
    expected_output: Any
    evaluation_criteria: List[str]
    difficulty_level: int  # 1-5
    metadata: Dict[str, Any]

class TaskGenerator:
    def __init__(self, config_path: str = "config/task_config.json"):
        self.config = self._load_config(config_path)
        self.task_templates = self._load_task_templates()
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load task generation configuration."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._default_config()
    
    def _default_config(self) -> Dict[str, Any]:
        """Default configuration for task generation."""
        return {
            "max_tasks_per_type": 10,
            "difficulty_distribution": [0.2, 0.3, 0.3, 0.15, 0.05],
            "code_languages": ["python", "javascript", "java", "cpp"],
            "complexity_factors": {
                "lines_of_code": [10, 50, 100, 200, 500],
                "cyclomatic_complexity": [1, 3, 5, 8, 12]
            }
        }
    
    def _load_task_templates(self) -> Dict[TaskType, List[Dict]]:
        """Load task templates for different task types."""
        return {
            TaskType.CODE_COMPLETION: [
                {
                    "template": "Complete the following function: {function_signature}",
                    "context_required": ["function_signature", "docstring", "test_cases"]
                },
                {
                    "template": "Implement the missing method in class {class_name}",
                    "context_required": ["class_definition", "method_signature"]
                }
            ],
            TaskType.BUG_FIXING: [
                {
                    "template": "Fix the bug in the following code: {buggy_code}",
                    "context_required": ["buggy_code", "error_description", "expected_behavior"]
                }
            ],
            TaskType.REFACTORING: [
                {
                    "template": "Refactor this code to improve {improvement_aspect}: {original_code}",
                    "context_required": ["original_code", "improvement_aspect", "constraints"]
                }
            ]
        }
    
    def generate_tasks_for_repo(self, repo_path: str, num_tasks: int = 20) -> List[SyntheticTask]:
        """Generate synthetic tasks based on repository analysis."""
        if not os.path.exists(repo_path):
            raise ValueError(f"Repository path does not exist: {repo_path}")
        
        analyzer = RepoAnalyzer(repo_path)
        repo_info = analyzer.analyze()
        
        tasks = []
        task_distribution = self._calculate_task_distribution(repo_info, num_tasks)
        
        for task_type, count in task_distribution.items():
            for i in range(count):
                task = self._generate_single_task(task_type, repo_info, i)
                tasks.append(task)
        
        return tasks
    
    def _calculate_task_distribution(self, repo_info: Dict, num_tasks: int) -> Dict[TaskType, int]:
        """Calculate how many tasks of each type to generate."""
        distribution = {}
        
        # Base distribution
        if repo_info.get("has_tests", False):
            distribution[TaskType.TEST_GENERATION] = max(1, num_tasks // 6)
        
        if repo_info.get("has_documentation", False):
            distribution[TaskType.DOCUMENTATION] = max(1, num_tasks // 8)
        
        # Always include core task types
        distribution[TaskType.CODE_COMPLETION] = max(2, num_tasks // 4)
        distribution[TaskType.BUG_FIXING] = max(1, num_tasks // 5)
        distribution[TaskType.REFACTORING] = max(1, num_tasks // 6)
        
        # Fill remaining slots
        remaining = num_tasks - sum(distribution.values())
        if remaining > 0:
            distribution[TaskType.ALGORITHM_IMPLEMENTATION] = remaining
        
        return distribution
    
    def _generate_single_task(self, task_type: TaskType, repo_info: Dict, task_index: int) -> SyntheticTask:
        """Generate a single synthetic task."""
        task_id = f"{task_type.value}_{task_index:03d}"
        difficulty = self._select_difficulty()
        
        if task_type == TaskType.CODE_COMPLETION:
            return self._generate_code_completion_task(task_id, repo_info, difficulty)
        elif task_type == TaskType.BUG_FIXING:
            return self._generate_bug_fixing_task(task_id, repo_info, difficulty)
        elif task_type == TaskType.REFACTORING:
            return self._generate_refactoring_task(task_id, repo_info, difficulty)
        else:
            return self._generate_generic_task(task_id, task_type, repo_info, difficulty)
    
    def _select_difficulty(self) -> int:
        """Select difficulty level based on configured distribution."""
        weights = self.config["difficulty_distribution"]
        return random.choices(range(1, 6), weights=weights)[0]
    
    def _generate_code_completion_task(self, task_id: str, repo_info: Dict, difficulty: int) -> SyntheticTask:
        """Generate a code completion task."""
        functions = repo_info.get("functions", [])
        if not functions:
            # Generate synthetic function
            function_name = f"process_data_{random.randint(1, 100)}"
            function_signature = f"def {function_name}(data: List[Dict]) -> Dict:"
        else:
            func = random.choice(functions)
            function_signature = func.get("signature", "def example_function():")
        
        return SyntheticTask(
            task_id=task_id,
            task_type=TaskType.CODE_COMPLETION,
            description=f"Complete the implementation of: {function_signature}",
            input_data={
                "function_signature": function_signature,
                "context": repo_info.get("context", ""),
                "requirements": self._generate_requirements(difficulty)
            },
            expected_output="# Implementation will be provided by golden test",
            evaluation_criteria=["correctness", "efficiency", "style", "completeness"],
            difficulty_level=difficulty,
            metadata={"language": repo_info.get("primary_language", "python")}
        )
    
    def _generate_bug_fixing_task(self, task_id: str, repo_info: Dict, difficulty: int) -> SyntheticTask:
        """Generate a bug fixing task."""
        buggy_code = self._create_buggy_code(difficulty, repo_info.get("primary_language", "python"))
        
        return SyntheticTask(
            task_id=task_id,
            task_type=TaskType.BUG_FIXING,
            description="Fix the bug in the provided code",
            input_data={
                "buggy_code": buggy_code,
                "error_description": "Function produces incorrect output",
                "test_cases": self._generate_test_cases(difficulty)
            },
            expected_output="# Fixed code will be provided by golden test",
            evaluation_criteria=["bug_fixed", "no_new_bugs", "maintains_functionality"],
            difficulty_level=difficulty,
            metadata={"bug_type": "logic_error"}
        )
    
    def _generate_refactoring_task(self, task_id: str, repo_info: Dict, difficulty: int) -> SyntheticTask:
        """Generate a refactoring task."""
        aspects = ["readability", "performance", "maintainability", "modularity"]
        improvement_aspect = random.choice(aspects)
        
        return SyntheticTask(
            task_id=task_id,
            task_type=TaskType.REFACTORING,
            description=f"Refactor code to improve {improvement_aspect}",
            input_data={
                "original_code": self._generate_refactorable_code(difficulty),
                "improvement_aspect": improvement_aspect,
                "constraints": ["maintain_functionality", "preserve_api"]
            },
            expected_output="# Refactored code will be provided by golden test",
            evaluation_criteria=["functionality_preserved", f"{improvement_aspect}_improved", "code_quality"],
            difficulty_level=difficulty,
            metadata={"refactoring_type": improvement_aspect}
        )
    
    def _generate_generic_task(self, task_id: str, task_type: TaskType, repo_info: Dict, difficulty: int) -> SyntheticTask:
        """Generate a generic task for other task types."""
        return SyntheticTask(
            task_id=task_id,
            task_type=task_type,
            description=f"Generic {task_type.value} task",
            input_data={"placeholder": "data"},
            expected_output="placeholder_output",
            evaluation_criteria=["correctness"],
            difficulty_level=difficulty,
            metadata={}
        )
    
    def _generate_requirements(self, difficulty: int) -> List[str]:
        """Generate requirements based on difficulty level."""
        base_requirements = ["Handle empty input", "Return correct data type"]
        
        if difficulty >= 2:
            base_requirements.append("Include error handling")
        if difficulty >= 3:
            base_requirements.extend(["Optimize for performance", "Add input validation"])
        if difficulty >= 4:
            base_requirements.append("Support concurrent access")
        if difficulty >= 5:
            base_requirements.extend(["Implement caching", "Add comprehensive logging"])
        
        return base_requirements
    
    def _create_buggy_code(self, difficulty: int, language: str) -> str:
        """Create buggy code based on difficulty and language."""
        if language == "python":
            if difficulty <= 2:
                return """
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)  # Bug: doesn't handle empty list
"""
            else:
                return """
def binary_search(arr, target):
    left, right = 0, len(arr)  # Bug: should be len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
"""
        return "# Buggy code placeholder"
    
    def _generate_refactorable_code(self, difficulty: int) -> str:
        """Generate code that needs refactoring."""
        if difficulty <= 2:
            return """
def process_user_data(data):
    result = []
    for item in data:
        if item['age'] > 18 and item['status'] == 'active' and item['verified'] == True:
            result.append({'name': item['name'], 'email': item['email'], 'age': item['age']})
    return result
"""
        else:
            return """
class DataProcessor:
    def __init__(self):
        self.data = []
        self.processed = []
        self.errors = []
    
    def process_all(self, input_data):
        for item in input_data:
            try:
                if self.validate_item(item):
                    processed_item = self.transform_item(item)
                    if self.additional_validation(processed_item):
                        self.processed.append(processed_item)
                    else:
                        self.errors.append(f"Validation failed for {item}")
                else:
                    self.errors.append(f"Invalid item: {item}")
            except Exception as e:
                self.errors.append(f"Error processing {item}: {e}")
        return self.processed
    
    def validate_item(self, item):
        return isinstance(item, dict) and 'id' in item and 'data' in item
    
    def transform_item(self, item):
        return {'id': item['id'], 'processed_data': item['data'].upper()}
    
    def additional_validation(self, item):
        return len(item['processed_data']) > 0
"""
    
    def _generate_test_cases(self, difficulty: int) -> List[Dict]:
        """Generate test cases based on difficulty."""
        base_cases = [
            {"input": [1, 2, 3], "expected": 2.0},
            {"input": [5], "expected": 5.0}
        ]
        
        if difficulty >= 2:
            base_cases.append({"input": [], "expected": "error"})
        if difficulty >= 3:
            base_cases.extend([
                {"input": [-1, 0, 1], "expected": 0.0},
                {"input": [1.5, 2.5], "expected": 2.0}
            ])
        
        return base_cases