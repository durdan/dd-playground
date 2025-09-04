from datetime import datetime, timedelta
from typing import List, Iterator, Optional
from models import LogEntry, RetentionPolicy
from storage import FileSystemStorage
from exporter import ComplianceExporter

class LogRetentionManager:
    def __init__(self, storage: FileSystemStorage, policy: RetentionPolicy):
        self.storage = storage
        self.policy = policy
        self.exporter = ComplianceExporter()
    
    def store_crewai_log(self, level: str, message: str, crew_id: str, 
                        agent_id: Optional[str] = None, task_id: Optional[str] = None,
                        metadata: Optional[dict] = None) -> None:
        """Store a CrewAI log entry."""
        if not crew_id:
            raise ValueError("crew_id is required")
        
        from models import LogLevel
        try:
            log_level = LogLevel(level.upper())
        except ValueError:
            raise ValueError(f"Invalid log level: {level}")
        
        log_entry = LogEntry(
            timestamp=datetime.now(),
            level=log_level,
            message=message,
            crew_id=crew_id,
            agent_id=agent_id,
            task_id=task_id,
            metadata=metadata
        )
        
        self.storage.store_log(log_entry)
    
    def get_logs_for_compliance(self, start_date: datetime, 
                               end_date: datetime) -> Iterator[LogEntry]:
        """Retrieve logs for compliance reporting."""
        if start_date > end_date:
            raise ValueError("start_date must be before end_date")
        
        return self.storage.get_logs_by_date_range(start_date, end_date)
    
    def export_compliance_logs(self, start_date: datetime, end_date: datetime,
                              output_path: str, format_type: str = "json") -> str:
        """Export logs for compliance purposes."""
        from models import ExportFormat
        
        try:
            export_format = ExportFormat(format_type.lower())
        except ValueError:
            raise ValueError(f"Invalid export format: {format_type}")
        
        logs = self.get_logs_for_compliance(start_date, end_date)
        return self.exporter.export_logs(logs, output_path, export_format)
    
    def cleanup_expired_logs(self) -> dict:
        """Remove logs that exceed maximum retention period."""
        if not self.policy.auto_cleanup_enabled:
            return {"status": "cleanup_disabled", "removed_count": 0}
        
        cutoff_date = datetime.now() - timedelta(days=self.policy.maximum_retention_months * 30)
        removed_count = self.storage.cleanup_expired_logs(cutoff_date)
        
        return {
            "status": "completed",
            "cutoff_date": cutoff_date.isoformat(),
            "removed_count": removed_count
        }
    
    def get_retention_status(self) -> dict:
        """Get current retention status and statistics."""
        log_dates = self.storage.get_all_log_dates()
        
        if not log_dates:
            return {
                "oldest_log": None,
                "newest_log": None,
                "total_days": 0,
                "within_minimum_retention": True,
                "compliance_status": "no_logs"
            }
        
        oldest_log = min(log_dates)
        newest_log = max(log_dates)
        total_days = (newest_log - oldest_log).days
        
        within_minimum = self.policy.is_within_minimum_retention(oldest_log)
        
        return {
            "oldest_log": oldest_log.isoformat(),
            "newest_log": newest_log.isoformat(),
            "total_days": total_days,
            "within_minimum_retention": within_minimum,
            "compliance_status": "compliant" if within_minimum else "at_risk",
            "policy": {
                "minimum_months": self.policy.minimum_retention_months,
                "maximum_months": self.policy.maximum_retention_months
            }
        }