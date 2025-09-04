"""Test configuration and coverage thresholds."""
from dataclasses import dataclass
from typing import Dict, List, Optional
import os

@dataclass
class CoverageThresholds:
    """Coverage threshold configuration."""
    line_coverage: float = 80.0
    branch_coverage: float = 70.0
    function_coverage: float = 85.0
    
    def validate(self) -> None:
        """Validate threshold values are reasonable."""
        thresholds = [self.line_coverage, self.branch_coverage, self.function_coverage]
        for threshold in thresholds:
            if not 0 <= threshold <= 100:
                raise ValueError(f"Coverage threshold must be between 0-100, got {threshold}")

@dataclass
class TestConfig:
    """Main test configuration."""
    test_directory: str = "tests"
    source_directory: str = "src"
    coverage_thresholds: CoverageThresholds = None
    test_pattern: str = "test_*.py"
    exclude_patterns: List[str] = None
    parallel_execution: bool = True
    max_workers: Optional[int] = None
    
    def __post_init__(self):
        if self.coverage_thresholds is None:
            self.coverage_thresholds = CoverageThresholds()
        if self.exclude_patterns is None:
            self.exclude_patterns = ["__pycache__", "*.pyc", ".git"]
        if self.max_workers is None:
            self.max_workers = min(4, os.cpu_count() or 1)
        
        self.coverage_thresholds.validate()

# Global test configuration
TEST_CONFIG = TestConfig()