from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum

class TestType(Enum):
    UNIT = "unit"
    INTEGRATION = "integration"
    EDGE_CASE = "edge_case"
    ERROR_HANDLING = "error_handling"

class Priority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class TestScenario:
    name: str
    description: str
    test_type: TestType
    priority: Priority
    target_function: str
    target_file: str
    inputs: Dict[str, Any]
    expected_output: Any
    setup_code: Optional[str] = None
    teardown_code: Optional[str] = None
    assertions: List[str] = None
    
    def __post_init__(self):
        if self.assertions is None:
            self.assertions = []

@dataclass
class TestAnalysisResult:
    file_path: str
    functions_analyzed: List[str]
    coverage_gaps: List[str]
    complexity_scores: Dict[str, int]
    suggested_scenarios: List[TestScenario]
    risk_areas: List[str]