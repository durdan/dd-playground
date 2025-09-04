from datetime import datetime
from typing import Dict, List, Optional
import uuid
from models import LogEntry, TraceSpan, LogLevel
from storage import TimeSeriesStorage
from metrics_collector import MetricsCollector

class ObservabilityService:
    def __init__(self, storage: TimeSeriesStorage):
        self._storage = storage
        self._metrics = MetricsCollector(storage)
        self._active_traces: Dict[str, List[TraceSpan]] = {}
    
    def log(self, message: str, level: LogLevel, service: str,
            labels: Optional[Dict[str, str]] = None):
        log_entry = LogEntry(
            message=message,
            level=level,
            timestamp=datetime.now(),
            service=service,
            labels=labels or {}
        )
        self._storage.store_log(log_entry)
        
        # Auto-increment log counters
        self._metrics.increment_counter(
            f"logs_total",
            labels={"level": level.value, "service": service}
        )
    
    def start_trace(self, operation: str, service: str,
                   trace_id: Optional[str] = None) -> str:
        if not trace_id:
            trace_id = str(uuid.uuid4())
        
        span_id = str(uuid.uuid4())
        
        span = TraceSpan(
            trace_id=trace_id,
            span_id=span_id,
            operation=operation,
            start_time=datetime.now(),
            duration_ms=0,
            service=service
        )
        
        if trace_id not in self._active_traces:
            self._active_traces[trace_id] = []
        self._active_traces[trace_id].append(span)
        
        return span_id
    
    def end_trace(self, span_id: str, status: str = "ok",
                 labels: Optional[Dict[str, str]] = None):
        # Find and complete the span
        for trace_id, spans in self._active_traces.items():
            for span in spans:
                if span.span_id == span_id:
                    duration = (datetime.now() - span.start_time).total_seconds() * 1000
                    span.duration_ms = duration
                    span.status = status
                    if labels:
                        span.labels.update(labels)
                    
                    self._storage.store_trace(span)
                    
                    # Record trace metrics
                    self._metrics.record_histogram(
                        "trace_duration_ms",
                        duration,
                        labels={"operation": span.operation, "service": span.service}
                    )
                    
                    spans.remove(span)
                    if not spans:
                        del self._active_traces[trace_id]
                    return
        
        raise ValueError(f"Span {span_id} not found")
    
    def get_metrics_collector(self) -> MetricsCollector:
        return self._metrics