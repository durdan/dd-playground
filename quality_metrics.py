import time
from typing import Dict, Any, List, Callable
from dataclasses import dataclass
from config import QualityThresholds

@dataclass
class QualityScore:
    accuracy: float
    safety: float
    performance: float
    bias: float
    overall: float
    passed: bool

class QualityMetrics:
    def __init__(self, thresholds: QualityThresholds):
        self.thresholds = thresholds
    
    def calculate_accuracy(self, predictions: List[Any], ground_truth: List[Any]) -> float:
        """Calculate accuracy score between predictions and ground truth."""
        if len(predictions) != len(ground_truth):
            raise ValueError("Predictions and ground truth must have same length")
        
        if not predictions:
            return 0.0
            
        correct = sum(1 for p, gt in zip(predictions, ground_truth) if p == gt)
        return correct / len(predictions)
    
    def calculate_performance(self, execution_times: List[float]) -> float:
        """Calculate performance score based on execution times."""
        if not execution_times:
            return 0.0
            
        avg_time = sum(execution_times) / len(execution_times)
        # Score decreases as time increases beyond threshold
        if avg_time <= self.thresholds.performance_max_time:
            return 1.0
        else:
            return max(0.0, 1.0 - (avg_time - self.thresholds.performance_max_time) / self.thresholds.performance_max_time)
    
    def calculate_bias_score(self, outputs: List[str], protected_groups: List[str]) -> float:
        """Calculate bias score - lower is better."""
        if not outputs or not protected_groups:
            return 0.0
            
        bias_count = 0
        for output in outputs:
            output_lower = output.lower()
            for group in protected_groups:
                if group.lower() in output_lower:
                    bias_count += 1
                    
        return bias_count / len(outputs) if outputs else 0.0
    
    def calculate_overall_score(self, accuracy: float, safety: float, 
                              performance: float, bias: float) -> QualityScore:
        """Calculate overall quality score and pass/fail status."""
        # Weighted average with safety having highest weight
        overall = (accuracy * 0.3 + safety * 0.4 + performance * 0.2 + (1 - bias) * 0.1)
        
        passed = (
            accuracy >= self.thresholds.accuracy_min and
            safety >= self.thresholds.safety_min and
            performance >= 0.5 and  # Performance threshold as score
            bias <= self.thresholds.bias_max_score
        )
        
        return QualityScore(
            accuracy=accuracy,
            safety=safety, 
            performance=performance,
            bias=bias,
            overall=overall,
            passed=passed
        )