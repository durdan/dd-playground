from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import threading
from models import Metric, LogEntry, TraceSpan, CostEntry

class TimeSeriesStorage:
    def __init__(self):
        self._metrics: List[Metric] = []
        self._logs: List[LogEntry] = []
        self._traces: List[TraceSpan] = []
        self._costs: List[CostEntry] = []
        self._lock = threading.RLock()
    
    def store_metric(self, metric: Metric):
        with self._lock:
            self._metrics.append(metric)
    
    def store_log(self, log: LogEntry):
        with self._lock:
            self._logs.append(log)
    
    def store_trace(self, trace: TraceSpan):
        with self._lock:
            self._traces.append(trace)
    
    def store_cost(self, cost: CostEntry):
        with self._lock:
            self._costs.append(cost)
    
    def get_metrics(self, start_time: Optional[datetime] = None, 
                   end_time: Optional[datetime] = None,
                   metric_name: Optional[str] = None) -> List[Metric]:
        with self._lock:
            filtered = self._metrics
            
            if start_time:
                filtered = [m for m in filtered if m.timestamp >= start_time]
            if end_time:
                filtered = [m for m in filtered if m.timestamp <= end_time]
            if metric_name:
                filtered = [m for m in filtered if m.name == metric_name]
                
            return filtered.copy()
    
    def get_logs(self, start_time: Optional[datetime] = None,
                end_time: Optional[datetime] = None,
                service: Optional[str] = None) -> List[LogEntry]:
        with self._lock:
            filtered = self._logs
            
            if start_time:
                filtered = [l for l in filtered if l.timestamp >= start_time]
            if end_time:
                filtered = [l for l in filtered if l.timestamp <= end_time]
            if service:
                filtered = [l for l in filtered if l.service == service]
                
            return filtered.copy()
    
    def get_traces(self, start_time: Optional[datetime] = None,
                  end_time: Optional[datetime] = None,
                  service: Optional[str] = None) -> List[TraceSpan]:
        with self._lock:
            filtered = self._traces
            
            if start_time:
                filtered = [t for t in filtered if t.start_time >= start_time]
            if end_time:
                filtered = [t for t in filtered if t.start_time <= end_time]
            if service:
                filtered = [t for t in filtered if t.service == service]
                
            return filtered.copy()
    
    def get_costs(self, start_time: Optional[datetime] = None,
                 end_time: Optional[datetime] = None,
                 service: Optional[str] = None) -> List[CostEntry]:
        with self._lock:
            filtered = self._costs
            
            if start_time:
                filtered = [c for c in filtered if c.timestamp >= start_time]
            if end_time:
                filtered = [c for c in filtered if c.timestamp <= end_time]
            if service:
                filtered = [c for c in filtered if c.service == service]
                
            return filtered.copy()