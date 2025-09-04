"""Code quality checker that integrates with subagent verification."""

import subprocess
import json
import tempfile
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class QualityMetrics:
    """Quality metrics for a code file or project."""
    lint_score: float
    complexity_score: float
    format_issues: int
    total_lines: int
    maintainability_index: float
    
    def overall_score(self) -> float:
        """Calculate overall quality score (0-100)."""
        # Weighted average of different metrics
        weights = {
            'lint': 0.4,
            'complexity': 0.3,
            'format': 0.2,
            'maintainability': 0.1
        }
        
        format_score = max(0, 100 - (self.format_issues * 10))
        
        return (
            self.lint_score * weights['lint'] +
            self.complexity_score * weights['complexity'] +
            format_score * weights['format'] +
            self.maintainability_index * weights['maintainability']
        )


@dataclass
class QualityConfig:
    """Configuration for quality checks."""
    min_lint_score: float = 8.0
    max_complexity: int = 10
    max_format_issues: int = 0
    min_maintainability: float = 70.0
    min_overall_score: float = 80.0
    
    # Tool-specific settings
    pylint_rcfile: Optional[str] = None
    black_line_length: int = 88
    radon_min_rank: str = 'B'


class QualityChecker:
    """Runs code quality tools and aggregates results."""
    
    def __init__(self, config: QualityConfig = None):
        self.config = config or QualityConfig()
        self._validate_tools()
    
    def _validate_tools(self) -> None:
        """Ensure required tools are available."""
        required_tools = ['pylint', 'black', 'radon']
        missing = []
        
        for tool in required_tools:
            try:
                subprocess.run([tool, '--version'], 
                             capture_output=True, check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                missing.append(tool)
        
        if missing:
            raise RuntimeError(f"Missing required tools: {', '.join(missing)}")
    
    def check_file(self, file_path: str) -> QualityMetrics:
        """Run quality checks on a single file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not file_path.endswith('.py'):
            raise ValueError("Only Python files are supported")
        
        lint_score = self._run_pylint(file_path)
        complexity_score = self._run_radon_complexity(file_path)
        format_issues = self._run_black_check(file_path)
        maintainability = self._run_radon_maintainability(file_path)
        total_lines = self._count_lines(file_path)
        
        return QualityMetrics(
            lint_score=lint_score,
            complexity_score=complexity_score,
            format_issues=format_issues,
            total_lines=total_lines,
            maintainability_index=maintainability
        )
    
    def check_directory(self, dir_path: str) -> Dict[str, QualityMetrics]:
        """Run quality checks on all Python files in directory."""
        results = {}
        
        for py_file in Path(dir_path).rglob('*.py'):
            try:
                results[str(py_file)] = self.check_file(str(py_file))
            except Exception as e:
                # Log error but continue with other files
                print(f"Warning: Failed to check {py_file}: {e}")
        
        return results
    
    def _run_pylint(self, file_path: str) -> float:
        """Run pylint and return score."""
        cmd = ['pylint', '--output-format=json']
        if self.config.pylint_rcfile:
            cmd.extend(['--rcfile', self.config.pylint_rcfile])
        cmd.append(file_path)
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            # Pylint returns non-zero for issues, but we still want the score
            if result.stdout:
                # Extract score from pylint output
                lines = result.stderr.split('\n')
                for line in lines:
                    if 'Your code has been rated at' in line:
                        score_str = line.split('rated at ')[1].split('/')[0]
                        return float(score_str)
            return 0.0
        except Exception:
            return 0.0
    
    def _run_radon_complexity(self, file_path: str) -> float:
        """Run radon complexity analysis."""
        try:
            result = subprocess.run(
                ['radon', 'cc', '--json', file_path],
                capture_output=True, text=True, check=True
            )
            
            data = json.loads(result.stdout)
            if not data.get(file_path):
                return 100.0
            
            # Convert complexity grades to scores
            grade_scores = {'A': 100, 'B': 80, 'C': 60, 'D': 40, 'E': 20, 'F': 0}
            complexities = data[file_path]
            
            if not complexities:
                return 100.0
            
            total_score = sum(grade_scores.get(item.get('rank', 'F'), 0) 
                            for item in complexities)
            return total_score / len(complexities)
            
        except Exception:
            return 0.0
    
    def _run_radon_maintainability(self, file_path: str) -> float:
        """Run radon maintainability index."""
        try:
            result = subprocess.run(
                ['radon', 'mi', '--json', file_path],
                capture_output=True, text=True, check=True
            )
            
            data = json.loads(result.stdout)
            if file_path in data:
                return data[file_path]['mi']
            return 0.0
            
        except Exception:
            return 0.0
    
    def _run_black_check(self, file_path: str) -> int:
        """Check formatting with black."""
        try:
            result = subprocess.run(
                ['black', '--check', '--line-length', str(self.config.black_line_length), 
                 file_path],
                capture_output=True, text=True
            )
            # Black returns 0 if no changes needed, 1 if changes needed
            return 1 if result.returncode != 0 else 0
        except Exception:
            return 1
    
    def _count_lines(self, file_path: str) -> int:
        """Count total lines in file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return sum(1 for _ in f)
        except Exception:
            return 0
    
    def passes_quality_gates(self, metrics: QualityMetrics) -> bool:
        """Check if metrics pass all quality gates."""
        return (
            metrics.lint_score >= self.config.min_lint_score and
            metrics.complexity_score >= (100 - self.config.max_complexity * 10) and
            metrics.format_issues <= self.config.max_format_issues and
            metrics.maintainability_index >= self.config.min_maintainability and
            metrics.overall_score() >= self.config.min_overall_score
        )