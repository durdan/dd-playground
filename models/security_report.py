from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum

class SeverityLevel(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class Finding(BaseModel):
    id: str
    title: str
    description: str
    severity: SeverityLevel
    category: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    remediation: Optional[str] = None

class ScanResult(BaseModel):
    tool_name: str
    scan_type: str
    target: str
    timestamp: datetime
    findings: List[Finding]
    summary: Dict[str, int]
    
class SecurityReport(BaseModel):
    scan_id: str
    target: str
    timestamp: datetime
    scan_results: List[ScanResult]
    overall_summary: Dict[str, int]
    recommendations: List[str]