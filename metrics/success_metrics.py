from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
import json
from pathlib import Path

class MetricType(Enum):
    ACCURACY = "accuracy"
    PRECISION = "precision"
    RECALL = "recall"
    F1_SCORE = "f1_score"
    LOSS = "loss"
    CUSTOM = "custom"

@dataclass
class Metric:
    """Individual metric definition."""
    name: str
    metric_type: MetricType
    target_value: float
    current_value: Optional[float] = None
    threshold: Optional[float] = None
    higher_is_better: bool = True
    
    def __post_init__(self):
        if not self.name:
            raise ValueError("Metric name cannot be empty")
    
    def is_target_met(self) -> bool:
        """Check if current value meets the target."""
        if self.current_value is None:
            return False
        
        if self.higher_is_better:
            return self.current_value >= self.target_value
        else:
            return self.current_value <= self.target_value
    
    def update_value(self, value: float):
        """Update the current metric value."""
        self.current_value = value

@dataclass
class SuccessMetrics:
    """Collection of success metrics for the project."""
    metrics: Dict[str, Metric] = field(default_factory=dict)
    
    def add_metric(self, metric: Metric):
        """Add a new metric."""
        self.metrics[metric.name] = metric
    
    def remove_metric(self, name: str) -> bool:
        """Remove a metric by name."""
        if name in self.metrics:
            del self.metrics[name]
            return True
        return False
    
    def update_metric(self, name: str, value: float) -> bool:
        """Update a metric's current value."""
        if name in self.metrics:
            self.metrics[name].update_value(value)
            return True
        return False
    
    def get_metric(self, name: str) -> Optional[Metric]:
        """Get a metric by name."""
        return self.metrics.get(name)
    
    def list_metrics(self) -> List[str]:
        """Get list of all metric names."""
        return list(self.metrics.keys())
    
    def get_summary(self) -> Dict[str, Dict[str, any]]:
        """Get summary of all metrics."""
        summary = {}
        for name, metric in self.metrics.items():
            summary[name] = {
                'type': metric.metric_type.value,
                'target': metric.target_value,
                'current': metric.current_value,
                'target_met': metric.is_target_met(),
                'higher_is_better': metric.higher_is_better
            }
        return summary
    
    def all_targets_met(self) -> bool:
        """Check if all metrics meet their targets."""
        return all(metric.is_target_met() for metric in self.metrics.values())
    
    def save(self, filepath: str):
        """Save metrics to JSON file."""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        data = {}
        for name, metric in self.metrics.items():
            data[name] = {
                'name': metric.name,
                'metric_type': metric.metric_type.value,
                'target_value': metric.target_value,
                'current_value': metric.current_value,
                'threshold': metric.threshold,
                'higher_is_better': metric.higher_is_better
            }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    @classmethod
    def load(cls, filepath: str) -> 'SuccessMetrics':
        """Load metrics from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        metrics = cls()
        for name, metric_data in data.items():
            metric = Metric(
                name=metric_data['name'],
                metric_type=MetricType(metric_data['metric_type']),
                target_value=metric_data['target_value'],
                current_value=metric_data.get('current_value'),
                threshold=metric_data.get('threshold'),
                higher_is_better=metric_data.get('higher_is_better', True)
            )
            metrics.add_metric(metric)
        
        return metrics