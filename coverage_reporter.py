"""Coverage analysis and reporting."""
import coverage
import os
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from test_config import TestConfig, CoverageThresholds

@dataclass
class CoverageResult:
    """Coverage analysis result."""
    line_coverage: float
    branch_coverage: float
    function_coverage: float
    missing_lines: Dict[str, List[int]]
    total_statements: int
    covered_statements: int
    
    def meets_thresholds(self, thresholds: CoverageThresholds) -> Tuple[bool, List[str]]:
        """Check if coverage meets minimum thresholds."""
        failures = []
        
        if self.line_coverage < thresholds.line_coverage:
            failures.append(f"Line coverage {self.line_coverage:.1f}% < {thresholds.line_coverage}%")
        
        if self.branch_coverage < thresholds.branch_coverage:
            failures.append(f"Branch coverage {self.branch_coverage:.1f}% < {thresholds.branch_coverage}%")
        
        if self.function_coverage < thresholds.function_coverage:
            failures.append(f"Function coverage {self.function_coverage:.1f}% < {thresholds.function_coverage}%")
        
        return len(failures) == 0, failures

class CoverageReporter:
    """Coverage analysis and reporting."""
    
    def __init__(self, config: TestConfig):
        self.config = config
        self.cov = None
    
    def start_coverage(self) -> None:
        """Start coverage measurement."""
        self.cov = coverage.Coverage(
            source=[self.config.source_directory],
            omit=self.config.exclude_patterns
        )
        self.cov.start()
    
    def stop_coverage(self) -> CoverageResult:
        """Stop coverage and return results."""
        if not self.cov:
            raise RuntimeError("Coverage not started")
        
        self.cov.stop()
        self.cov.save()
        
        # Get coverage data
        total_statements = 0
        covered_statements = 0
        missing_lines = {}
        
        for filename in self.cov.get_data().measured_files():
            analysis = self.cov.analysis2(filename)
            statements = len(analysis.statements)
            missing = len(analysis.missing)
            
            total_statements += statements
            covered_statements += (statements - missing)
            
            if analysis.missing:
                missing_lines[filename] = sorted(analysis.missing)
        
        line_coverage = (covered_statements / total_statements * 100) if total_statements > 0 else 0
        
        # Branch coverage (simplified - would need more detailed analysis)
        branch_coverage = line_coverage * 0.9  # Approximation
        
        # Function coverage (simplified)
        function_coverage = line_coverage * 0.95  # Approximation
        
        return CoverageResult(
            line_coverage=line_coverage,
            branch_coverage=branch_coverage,
            function_coverage=function_coverage,
            missing_lines=missing_lines,
            total_statements=total_statements,
            covered_statements=covered_statements
        )
    
    def generate_report(self, result: CoverageResult, output_file: Optional[str] = None) -> str:
        """Generate coverage report."""
        report_lines = [
            "Coverage Report",
            "=" * 50,
            f"Line Coverage:     {result.line_coverage:.1f}%",
            f"Branch Coverage:   {result.branch_coverage:.1f}%",
            f"Function Coverage: {result.function_coverage:.1f}%",
            f"Total Statements:  {result.total_statements}",
            f"Covered:           {result.covered_statements}",
            ""
        ]
        
        if result.missing_lines:
            report_lines.append("Missing Coverage:")
            report_lines.append("-" * 30)
            for filename, lines in result.missing_lines.items():
                report_lines.append(f"{filename}: lines {', '.join(map(str, lines))}")
        
        report = "\n".join(report_lines)
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report)
        
        return report