from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any, Optional
from datetime import datetime

class ExportFormat(Enum):
    PDF = "pdf"
    DOCX = "docx"
    MARKDOWN = "md"

@dataclass
class ExportRequest:
    specification: Dict[str, Any]
    format: ExportFormat
    filename: Optional[str] = None
    options: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.options is None:
            self.options = {}

@dataclass
class ExportResult:
    success: bool
    file_path: Optional[str] = None
    error_message: Optional[str] = None
    generation_time_ms: int = 0
    cache_hit: bool = False

@dataclass
class ExportMetrics:
    total_exports: int = 0
    cache_hits: int = 0
    avg_generation_time_ms: float = 0.0
    format_stats: Dict[str, int] = None
    
    def __post_init__(self):
        if self.format_stats is None:
            self.format_stats = {}