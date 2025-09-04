from typing import List, Optional
from datetime import datetime
from models import OverrideAuditEntry

class AuditRepository:
    def __init__(self):
        self._entries: List[OverrideAuditEntry] = []
    
    def save(self, entry: OverrideAuditEntry) -> None:
        """Save an audit entry."""
        self._entries.append(entry)
    
    def find_by_user(self, user_id: str) -> List[OverrideAuditEntry]:
        """Find all audit entries for a specific user."""
        return [entry for entry in self._entries if entry.user_id == user_id]
    
    def find_by_entity(self, entity_type: str, entity_id: str) -> List[OverrideAuditEntry]:
        """Find all audit entries for a specific entity."""
        return [entry for entry in self._entries 
                if entry.entity_type == entity_type and entry.entity_id == entity_id]
    
    def find_by_date_range(self, start_date: datetime, end_date: datetime) -> List[OverrideAuditEntry]:
        """Find all audit entries within a date range."""
        return [entry for entry in self._entries 
                if start_date <= entry.timestamp <= end_date]
    
    def get_all(self) -> List[OverrideAuditEntry]:
        """Get all audit entries."""
        return self._entries.copy()