from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum

class MetricType(Enum):
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"

class LogLevel(Enum):
    DEBUG = "debug"
    INFO = "info"
    WARN = "warn"
    ERROR = "error"

@dataclass
class Metric:
    name: str
    value: float
    metric_type: MetricType
    timestamp: datetime
    labels: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.name:
            raise ValueError("Metric name cannot be empty")
        if self.value < 0 and self.metric_type == MetricType.COUNTER:
            raise ValueError("Counter values cannot be negative")

@dataclass
class LogEntry:
    message: str
    level: LogLevel
    timestamp: datetime
    service: str
    labels: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.message:
            raise ValueError("Log message cannot be empty")
        if not self.service:
            raise ValueError("Service name cannot be empty")

@dataclass
class TraceSpan:
    trace_id: str
    span_id: str
    operation: str
    start_time: datetime
    duration_ms: float
    service: str
    status: str = "ok"
    labels: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.trace_id or not self.span_id:
            raise ValueError("Trace ID and Span ID are required")
        if self.duration_ms < 0:
            raise ValueError("Duration cannot be negative")

@dataclass
class CostEntry:
    resource_id: str
    resource_type: str
    service: str
    cost: float
    usage_amount: float
    usage_unit: str
    timestamp: datetime
    labels: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.resource_id or not self.resource_type:
            raise ValueError("Resource ID and type are required")
        if self.cost < 0 or self.usage_amount < 0:
            raise ValueError("Cost and usage cannot be negative")

@dataclass
class Report:
    title: str
    report_type: str
    data: Dict[str, Any]
    generated_at: datetime
    time_range: Dict[str, datetime]