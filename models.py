from dataclasses import dataclass
from datetime import date
from typing import List, Optional

@dataclass
class MetricData:
    date: date
    metric_name: str
    value: float
    
    def __post_init__(self):
        if not self.metric_name.strip():
            raise ValueError("Metric name cannot be empty")
        if self.value < 0:
            raise ValueError("Metric value cannot be negative")

@dataclass
class TrendResult:
    metric_name: str
    current_value: float
    previous_value: Optional[float]
    change_percent: Optional[float]
    trend_direction: str  # 'up', 'down', 'stable'

@dataclass
class OutlierResult:
    metric_name: str
    outlier_values: List[float]
    outlier_dates: List[date]
    threshold_lower: float
    threshold_upper: float

@dataclass
class WeeklyReport:
    week_ending: date
    trends: List[TrendResult]
    outliers: List[OutlierResult]
    summary: str