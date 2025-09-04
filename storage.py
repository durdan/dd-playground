import os
import json
import gzip
from pathlib import Path
from datetime import datetime
from typing import List, Iterator, Optional
from models import LogEntry

class FileSystemStorage:
    def __init__(self, base_path: str = "./compliance_logs"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def store_log(self, log_entry: LogEntry) -> None:
        """Store a single log entry with date-based partitioning."""
        date_path = self._get_date_path(log_entry.timestamp)
        date_path.mkdir(parents=True, exist_ok=True)
        
        log_file = date_path / f"{log_entry.timestamp.strftime('%H')}.jsonl.gz"
        
        with gzip.open(log_file, 'at', encoding='utf-8') as f:
            f.write(json.dumps(log_entry.to_dict()) + '\n')
    
    def get_logs_by_date_range(self, start_date: datetime, end_date: datetime) -> Iterator[LogEntry]:
        """Retrieve logs within a date range."""
        current_date = start_date.date()
        end_date = end_date.date()
        
        while current_date <= end_date:
            date_path = self.base_path / str(current_date.year) / f"{current_date.month:02d}" / f"{current_date.day:02d}"
            
            if date_path.exists():
                for hour_file in date_path.glob("*.jsonl.gz"):
                    yield from self._read_log_file(hour_file)
            
            current_date = (datetime.combine(current_date, datetime.min.time()) + 
                          timedelta(days=1)).date()
    
    def get_all_log_dates(self) -> List[datetime]:
        """Get all dates that have log entries."""
        dates = []
        for year_dir in self.base_path.iterdir():
            if not year_dir.is_dir() or not year_dir.name.isdigit():
                continue
            for month_dir in year_dir.iterdir():
                if not month_dir.is_dir():
                    continue
                for day_dir in month_dir.iterdir():
                    if not day_dir.is_dir():
                        continue
                    try:
                        date = datetime(int(year_dir.name), int(month_dir.name), int(day_dir.name))
                        dates.append(date)
                    except ValueError:
                        continue
        return sorted(dates)
    
    def cleanup_expired_logs(self, cutoff_date: datetime) -> int:
        """Remove logs older than cutoff date. Returns count of removed files."""
        removed_count = 0
        
        for year_dir in self.base_path.iterdir():
            if not year_dir.is_dir() or not year_dir.name.isdigit():
                continue
            
            year = int(year_dir.name)
            if year < cutoff_date.year:
                # Remove entire year
                import shutil
                shutil.rmtree(year_dir)
                removed_count += len(list(year_dir.rglob("*.jsonl.gz")))
                continue
            
            for month_dir in year_dir.iterdir():
                if not month_dir.is_dir():
                    continue
                
                month = int(month_dir.name)
                if year == cutoff_date.year and month < cutoff_date.month:
                    import shutil
                    shutil.rmtree(month_dir)
                    removed_count += len(list(month_dir.rglob("*.jsonl.gz")))
                    continue
                
                for day_dir in month_dir.iterdir():
                    if not day_dir.is_dir():
                        continue
                    
                    day = int(day_dir.name)
                    log_date = datetime(year, month, day)
                    
                    if log_date < cutoff_date:
                        import shutil
                        shutil.rmtree(day_dir)
                        removed_count += len(list(day_dir.rglob("*.jsonl.gz")))
        
        return removed_count
    
    def _get_date_path(self, timestamp: datetime) -> Path:
        return (self.base_path / 
                str(timestamp.year) / 
                f"{timestamp.month:02d}" / 
                f"{timestamp.day:02d}")
    
    def _read_log_file(self, file_path: Path) -> Iterator[LogEntry]:
        try:
            with gzip.open(file_path, 'rt', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        yield LogEntry.from_dict(json.loads(line))
        except Exception as e:
            print(f"Error reading log file {file_path}: {e}")