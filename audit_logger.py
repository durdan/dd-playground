from datetime import datetime
from typing import Any, Optional
import uuid
from models import OverrideAuditEntry
from audit_repository import AuditRepository

class AuditLogger:
    def __init__(self, repository: AuditRepository):
        self._repository = repository
    
    def log_override(self, 
                    user_id: str,
                    reason: str,
                    field_name: str,
                    original_value: Any,
                    new_value: Any,
                    entity_type: str,
                    entity_id: str,
                    ip_address: Optional[str] = None) -> str:
        """Log an override event and return the audit entry ID."""
        
        entry = OverrideAuditEntry(
            id=str(uuid.uuid4()),
            user_id=user_id,
            timestamp=datetime.utcnow(),
            reason=reason,
            field_name=field_name,
            original_value=original_value,
            new_value=new_value,
            entity_type=entity_type,
            entity_id=entity_id,
            ip_address=ip_address
        )
        
        self._repository.save(entry)
        return entry.id