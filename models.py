from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional
import uuid

@dataclass
class OverrideAuditEntry:
    id: str
    user_id: str
    timestamp: datetime
    reason: str
    field_name: str
    original_value: Any
    new_value: Any
    entity_type: str
    entity_id: str
    ip_address: Optional[str] = None
    
    def __post_init__(self):
        if not self.user_id.strip():
            raise ValueError("User ID is required")
        if not self.reason.strip():
            raise ValueError("Reason is required")
        if not self.field_name.strip():
            raise ValueError("Field name is required")