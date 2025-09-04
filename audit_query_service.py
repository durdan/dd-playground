from typing import List
from datetime import datetime
from models import OverrideAuditEntry
from audit_repository import AuditRepository

class AuditQueryService:
    def __init__(self, repository: AuditRepository):
        self._repository = repository
    
    def get_user_overrides(self, user_id: str) -> List[OverrideAuditEntry]:
        """Get all overrides performed by a user."""
        return self._repository.find_by_user(user_id)
    
    def get_entity_overrides(self, entity_type: str, entity_id: str) -> List[OverrideAuditEntry]:
        """Get all overrides for a specific entity."""
        return self._repository.find_by_entity(entity_type, entity_id)
    
    def get_overrides_by_date_range(self, start_date: datetime, end_date: datetime) -> List[OverrideAuditEntry]:
        """Get all overrides within a date range."""
        return self._repository.find_by_date_range(start_date, end_date)
    
    def get_all_overrides(self) -> List[OverrideAuditEntry]:
        """Get all override audit entries."""
        return self._repository.get_all()