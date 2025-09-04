from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from enum import Enum
import json

class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class ExportFormat(Enum):
    JSON = "json"
    CSV = "csv"
    XML = "xml"

@dataclass
class LogEntry:
    timestamp: datetime
    level: LogLevel
    message: str
    crew_id: str
    agent_id: Optional[str] = None
    task_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        data['level'] = self.level.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LogEntry':
        data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        data['level'] = LogLevel(data['level'])
        return cls(**data)

@dataclass
class RetentionPolicy:
    minimum_retention_months: int = 12
    maximum_retention_months: int = 84  # 7 years default
    auto_cleanup_enabled: bool = True
    compliance_tags: Optional[list] = None
    
    def is_expired(self, log_date: datetime) -> bool:
        cutoff_date = datetime.now() - timedelta(days=self.maximum_retention_months * 30)
        return log_date < cutoff_date
    
    def is_within_minimum_retention(self, log_date: datetime) -> bool:
        cutoff_date = datetime.now() - timedelta(days=self.minimum_retention_months * 30)
        return log_date >= cutoff_date