from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum

class TestType(Enum):
    UNIT = "unit"
    INTEGRATION = "integration"
    EDGE_CASE = "edge_case"
    PERFORMANCE = "performance"

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class TestSpecification:
    """Specification for test generation"""
    module_name: str
    source_code: str
    framework: str = "pytest"
    coverage_target: float = 0.8
    include_edge_cases: bool = True
    include_performance_tests: bool = False

@dataclass
class GenerationResult:
    """Result of test generation process"""
    test_suite: 'TestSuite'
    coverage_estimate: float
    generation_time: float
    warnings: List[str]
    success: bool