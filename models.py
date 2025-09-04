from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Dict, Any, Optional

class PIIType(Enum):
    EMAIL = "email"
    SSN = "ssn"
    PHONE = "phone"
    CREDIT_CARD = "credit_card"

class AccessLevel(Enum):
    READ = "read"
    WRITE = "write"
    ADMIN = "admin"

@dataclass
class RedactionResult:
    original_text: str
    redacted_text: str
    pii_found: List[PIIType]
    redaction_count: int

@dataclass
class RetentionPolicy:
    log_type: str
    retention_days: int
    auto_delete: bool = True

@dataclass
class AuditEvent:
    timestamp: datetime
    user_id: str
    action: str
    resource: str
    success: bool
    details: Dict[str, Any]

@dataclass
class User:
    user_id: str
    access_level: AccessLevel
    allowed_resources: List[str]