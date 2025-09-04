from typing import List, Optional
from models import MetricData, TrendResult

class TrendAnalyzer:
    
    def analyze_trends(self, current_week: List[MetricData], 
                      previous_week: List[MetricData]) -> List[TrendResult]:
        """Analyze week-over-week trends for metrics."""
        trends = []
        
        current_metrics = self._group_by_metric(current_week)
        previous_metrics = self._group_by_metric(previous_week)
        
        for metric_name, current_values in current_metrics.items():
            current_avg = sum(current_values) / len(current_values)
            previous_values = previous_metrics.get(metric_name, [])
            
            if previous_values:
                previous_avg = sum(previous_values) / len(previous_values)
                change_percent = ((current_avg - previous_avg) / previous_avg) * 100
                trend_direction = self._determine_trend_direction(change_percent)
            else:
                previous_avg = None
                change_percent = None
                trend_direction = 'new'
            
            trends.append(TrendResult(
                metric_name=metric_name,
                current_value=current_avg,
                previous_value=previous_avg,
                change_percent=change_percent,
                trend_direction=trend_direction
            ))
        
        return trends
    
    def _group_by_metric(self, data: List[MetricData]) -> dict:
        """Group metric values by metric name."""
        grouped = {}
        for item in data:
            if item.metric_name not in grouped:
                grouped[item.metric_name] = []
            grouped[item.metric_name].append(item.value)
        return grouped
    
    def _determine_trend_direction(self, change_percent: float) -> str:
        """Determine trend direction based on percentage change."""
        if abs(change_percent) < 5:  # Less than 5% change is stable
            return 'stable'
        return 'up' if change_percent > 0 else 'down'