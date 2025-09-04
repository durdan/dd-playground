import time
from typing import Dict, Any, List
from collections import defaultdict, deque
from datetime import datetime, timedelta
from .manager import OperationMetrics

class MetricsCollector:
    """Collects and aggregates operation metrics."""
    
    def __init__(self, max_retention_hours: int = 24):
        self.max_retention_hours = max_retention_hours
        self.metrics: deque = deque()
        self.operation_counts = defaultdict(int)
        self.operation_durations = defaultdict(list)
        self.error_counts = defaultdict(int)
    
    def record_metrics(self, metrics: OperationMetrics):
        """Record metrics for an operation."""
        self.metrics.append(metrics)
        self._cleanup_old_metrics()
        
        # Update aggregated metrics
        self.operation_counts[metrics.operation_type] += 1
        
        if metrics.duration_ms is not None:
            self.operation_durations[metrics.operation_type].append(metrics.duration_ms)
        
        if metrics.status == "failed":
            self.error_counts[metrics.operation_type] += 1
    
    def _cleanup_old_metrics(self):
        """Remove metrics older than retention period."""
        cutoff_time = datetime.now() - timedelta(hours=self.max_retention_hours)
        
        while self.metrics and self.metrics[0].start_time < cutoff_time:
            self.metrics.popleft()
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of collected metrics."""
        self._cleanup_old_metrics()
        
        summary = {
            "total_operations": len(self.metrics),
            "operation_counts": dict(self.operation_counts),
            "error_counts": dict(self.error_counts),
            "average_durations": {},
            "success_rates": {}
        }
        
        # Calculate average durations
        for op_type, durations in self.operation_durations.items():
            if durations:
                summary["average_durations"][op_type] = sum(durations) / len(durations)
        
        # Calculate success rates
        for op_type, total_count in self.operation_counts.items():
            error_count = self.error_counts.get(op_type, 0)
            success_rate = ((total_count - error_count) / total_count) * 100
            summary["success_rates"][op_type] = success_rate
        
        return summary
    
    def get_recent_failures(self, limit: int = 10) -> List[OperationMetrics]:
        """Get recent failed operations."""
        failures = [m for m in self.metrics if m.status == "failed"]
        return sorted(failures, key=lambda x: x.start_time, reverse=True)[:limit]