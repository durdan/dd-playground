from typing import Any, Optional, Dict
from audit_logger import AuditLogger

class OverrideService:
    def __init__(self, audit_logger: AuditLogger):
        self._audit_logger = audit_logger
        # Simulated data store
        self._data: Dict[str, Dict[str, Any]] = {}
    
    def override_field(self,
                      user_id: str,
                      reason: str,
                      entity_type: str,
                      entity_id: str,
                      field_name: str,
                      new_value: Any,
                      ip_address: Optional[str] = None) -> str:
        """Override a field value and log the action."""
        
        # Get current value
        entity_key = f"{entity_type}:{entity_id}"
        if entity_key not in self._data:
            self._data[entity_key] = {}
        
        original_value = self._data[entity_key].get(field_name)
        
        # Perform the override
        self._data[entity_key][field_name] = new_value
        
        # Log the override
        audit_id = self._audit_logger.log_override(
            user_id=user_id,
            reason=reason,
            field_name=field_name,
            original_value=original_value,
            new_value=new_value,
            entity_type=entity_type,
            entity_id=entity_id,
            ip_address=ip_address
        )
        
        return audit_id
    
    def get_field_value(self, entity_type: str, entity_id: str, field_name: str) -> Any:
        """Get current field value."""
        entity_key = f"{entity_type}:{entity_id}"
        return self._data.get(entity_key, {}).get(field_name)