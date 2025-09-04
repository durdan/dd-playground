from typing import List
from datetime import date, timedelta
from models import MetricData

class DataRepository:
    """Simple in-memory data repository. In practice, this would connect to a database."""
    
    def __init__(self):
        self._data: List[MetricData] = []
    
    def add_metrics(self, metrics: List[MetricData]) -> None:
        """Add metrics to the repository."""
        for metric in metrics:
            if not isinstance(metric, MetricData):
                raise ValueError("Invalid metric data")
        self._data.extend(metrics)
    
    def get_metrics_for_week(self, week_ending: date) -> List[MetricData]:
        """Get all metrics for a specific week (7 days ending on given date)."""
        week_start = week_ending - timedelta(days=6)
        return [
            metric for metric in self._data
            if week_start <= metric.date <= week_ending
        ]
    
    def get_metrics_for_date_range(self, start_date: date, end_date: date) -> List[MetricData]:
        """Get metrics within a date range."""
        return [
            metric for metric in self._data
            if start_date <= metric.date <= end_date
        ]