"""Integration with existing subagent verification system."""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import json

from .checker import QualityChecker, QualityMetrics, QualityConfig


@dataclass
class QualityReport:
    """Aggregated quality report for verification."""
    file_metrics: Dict[str, QualityMetrics]
    overall_score: float
    passed_gates: bool
    issues: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'file_metrics': {
                path: {
                    'lint_score': metrics.lint_score,
                    'complexity_score': metrics.complexity_score,
                    'format_issues': metrics.format_issues,
                    'total_lines': metrics.total_lines,
                    'maintainability_index': metrics.maintainability_index,
                    'overall_score': metrics.overall_score()
                }
                for path, metrics in self.file_metrics.items()
            },
            'overall_score': self.overall_score,
            'passed_gates': self.passed_gates,
            'issues': self.issues
        }


class QualityVerifier:
    """Quality verification component for subagent system."""
    
    def __init__(self, config: QualityConfig = None):
        self.checker = QualityChecker(config)
        self.config = config or QualityConfig()
    
    def verify_code_quality(self, code_path: str) -> QualityReport:
        """Verify code quality for a file or directory."""
        if code_path.endswith('.py'):
            file_metrics = {code_path: self.checker.check_file(code_path)}
        else:
            file_metrics = self.checker.check_directory(code_path)
        
        if not file_metrics:
            return QualityReport(
                file_metrics={},
                overall_score=0.0,
                passed_gates=False,
                issues=["No Python files found to analyze"]
            )
        
        # Calculate overall score and collect issues
        total_score = sum(metrics.overall_score() for metrics in file_metrics.values())
        overall_score = total_score / len(file_metrics)
        
        issues = []
        all_passed = True
        
        for file_path, metrics in file_metrics.items():
            if not self.checker.passes_quality_gates(metrics):
                all_passed = False
                file_issues = self._get_file_issues(file_path, metrics)
                issues.extend(file_issues)
        
        return QualityReport(
            file_metrics=file_metrics,
            overall_score=overall_score,
            passed_gates=all_passed,
            issues=issues
        )
    
    def _get_file_issues(self, file_path: str, metrics: QualityMetrics) -> List[str]:
        """Get specific issues for a file."""
        issues = []
        
        if metrics.lint_score < self.config.min_lint_score:
            issues.append(f"{file_path}: Lint score {metrics.lint_score:.1f} below threshold {self.config.min_lint_score}")
        
        if metrics.format_issues > self.config.max_format_issues:
            issues.append(f"{file_path}: {metrics.format_issues} formatting issues")
        
        if metrics.maintainability_index < self.config.min_maintainability:
            issues.append(f"{file_path}: Maintainability index {metrics.maintainability_index:.1f} below threshold {self.config.min_maintainability}")
        
        if metrics.overall_score() < self.config.min_overall_score:
            issues.append(f"{file_path}: Overall score {metrics.overall_score():.1f} below threshold {self.config.min_overall_score}")
        
        return issues


# Mock integration point - extend existing SubagentVerifier
class EnhancedSubagentVerifier:
    """Extended subagent verifier with quality checks."""
    
    def __init__(self, quality_config: QualityConfig = None):
        # Assume existing verifier exists
        # self.base_verifier = SubagentVerifier()
        self.quality_verifier = QualityVerifier(quality_config)
    
    def verify_with_quality(self, code_path: str, 
                          include_quality: bool = True) -> Dict[str, Any]:
        """Run verification including quality checks."""
        results = {
            'functional_tests': True,  # Mock existing verification
            'quality_report': None
        }
        
        if include_quality:
            quality_report = self.quality_verifier.verify_code_quality(code_path)
            results['quality_report'] = quality_report.to_dict()
            results['quality_passed'] = quality_report.passed_gates
        
        results['overall_passed'] = (
            results['functional_tests'] and 
            (not include_quality or results.get('quality_passed', True))
        )
        
        return results