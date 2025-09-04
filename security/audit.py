import json
import datetime
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict

@dataclass
class AuditEvent:
    timestamp: str
    user_id: str
    action: str
    resource: str
    result: str
    details: Optional[Dict[str, Any]] = None

class AuditLogger:
    def __init__(self, log_file: str = "audit.log"):
        self.log_file = log_file
    
    def log_event(self, user_id: str, action: str, resource: str, 
                  result: str, details: Optional[Dict[str, Any]] = None) -> None:
        """Log security and compliance events"""
        if not all([user_id, action, resource, result]):
            raise ValueError("All audit fields are required")
        
        event = AuditEvent(
            timestamp=datetime.datetime.utcnow().isoformat(),
            user_id=user_id,
            action=action,
            resource=resource,
            result=result,
            details=details or {}
        )
        
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(asdict(event)) + '\n')
    
    def log_pii_access(self, user_id: str, pii_type: str, operation: str) -> None:
        """Log PII access for compliance"""
        self.log_event(
            user_id=user_id,
            action=f"pii_{operation}",
            resource=pii_type,
            result="success",
            details={"compliance": "gdpr", "data_category": "personal"}
        )
    
    def log_security_event(self, user_id: str, event_type: str, success: bool) -> None:
        """Log security events"""
        self.log_event(
            user_id=user_id,
            action=event_type,
            resource="security",
            result="success" if success else "failure"
        )