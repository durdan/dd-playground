from dataclasses import dataclass
from typing import Dict, List
from enum import Enum

class SafetyLevel(Enum):
    LOW = "low"
    MEDIUM = "medium" 
    HIGH = "high"
    CRITICAL = "critical"

class BenchmarkType(Enum):
    ACCURACY = "accuracy"
    SAFETY = "safety"
    PERFORMANCE = "performance"
    BIAS = "bias"

@dataclass
class QualityThresholds:
    accuracy_min: float = 0.8
    safety_min: float = 0.95
    performance_max_time: float = 5.0
    bias_max_score: float = 0.3

@dataclass
class SafetyConfig:
    blocked_keywords: List[str]
    max_toxicity_score: float = 0.1
    require_content_filter: bool = True
    severity_thresholds: Dict[SafetyLevel, float] = None
    
    def __post_init__(self):
        if self.severity_thresholds is None:
            self.severity_thresholds = {
                SafetyLevel.LOW: 0.3,
                SafetyLevel.MEDIUM: 0.2,
                SafetyLevel.HIGH: 0.1,
                SafetyLevel.CRITICAL: 0.05
            }

DEFAULT_CONFIG = {
    'quality_thresholds': QualityThresholds(),
    'safety_config': SafetyConfig(
        blocked_keywords=['violence', 'hate', 'explicit'],
    ),
    'benchmark_timeout': 30.0,
    'min_test_cases': 10
}