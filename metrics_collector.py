from datetime import datetime
from typing import Dict, Optional
from models import Metric, MetricType
from storage import TimeSeriesStorage

class MetricsCollector:
    def __init__(self, storage: TimeSeriesStorage):
        self._storage = storage
        self._counters: Dict[str, float] = {}
    
    def increment_counter(self, name: str, value: float = 1.0, 
                         labels: Optional[Dict[str, str]] = None):
        if name not in self._counters:
            self._counters[name] = 0
        
        self._counters[name] += value
        
        metric = Metric(
            name=name,
            value=self._counters[name],
            metric_type=MetricType.COUNTER,
            timestamp=datetime.now(),
            labels=labels or {}
        )
        self._storage.store_metric(metric)
    
    def set_gauge(self, name: str, value: float, 
                  labels: Optional[Dict[str, str]] = None):
        metric = Metric(
            name=name,
            value=value,
            metric_type=MetricType.GAUGE,
            timestamp=datetime.now(),
            labels=labels or {}
        )
        self._storage.store_metric(metric)
    
    def record_histogram(self, name: str, value: float,
                        labels: Optional[Dict[str, str]] = None):
        metric = Metric(
            name=name,
            value=value,
            metric_type=MetricType.HISTOGRAM,
            timestamp=datetime.now(),
            labels=labels or {}
        )
        self._storage.store_metric(metric)
    
    def get_counter_value(self, name: str) -> float:
        return self._counters.get(name, 0.0)