import hashlib
import json
import os
from datetime import datetime
from typing import Optional, List
from cryptography.fernet import Fernet
from models import User, AccessLevel, AuditEvent

class SecurityControls:
    def __init__(self, audit_log_path: str = "audit_logs"):
        self.audit_log_path = audit_log_path
        self.users: dict[str, User] = {}
        self._encryption_key = self._get_or_create_key()
        self._cipher = Fernet(self._encryption_key)
        self._ensure_audit_path_exists()
    
    def _ensure_audit_path_exists(self):
        os.makedirs(self.audit_log_path, exist_ok=True)
    
    def _get_or_create_key(self) -> bytes:
        key_file = "encryption.key"
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            return key
    
    def register_user(self, user: User):
        if not user.user_id:
            raise ValueError("User ID is required")
        self.users[user.user_id] = user
    
    def authenticate_user(self, user_id: str, action: str, resource: str) -> bool:
        if not user_id or not action or not resource:
            return False
        
        user = self.users.get(user_id)
        if not user:
            self._log_audit_event(user_id, action, resource, False, {"error": "User not found"})
            return False
        
        # Check resource access
        if resource not in user.allowed_resources and "*" not in user.allowed_resources:
            self._log_audit_event(user_id, action, resource, False, {"error": "Resource access denied"})
            return False
        
        # Check action permissions
        required_level = self._get_required_access_level(action)
        if not self._has_sufficient_access(user.access_level, required_level):
            self._log_audit_event(user_id, action, resource, False, {"error": "Insufficient permissions"})
            return False
        
        self._log_audit_event(user_id, action, resource, True, {})
        return True
    
    def _get_required_access_level(self, action: str) -> AccessLevel:
        admin_actions = ["delete", "configure", "manage_users"]
        write_actions = ["create", "update", "redact"]
        
        if action in admin_actions:
            return AccessLevel.ADMIN
        elif action in write_actions:
            return AccessLevel.WRITE
        else:
            return AccessLevel.READ
    
    def _has_sufficient_access(self, user_level: AccessLevel, required_level: AccessLevel) -> bool:
        level_hierarchy = {
            AccessLevel.READ: 1,
            AccessLevel.WRITE: 2,
            AccessLevel.ADMIN: 3
        }
        return level_hierarchy[user_level] >= level_hierarchy[required_level]
    
    def encrypt_data(self, data: str) -> str:
        if not data:
            raise ValueError("Data cannot be empty")
        return self._cipher.encrypt(data.encode()).decode()
    
    def decrypt_data(self, encrypted_data: str) -> str:
        if not encrypted_data:
            raise ValueError("Encrypted data cannot be empty")
        return self._cipher.decrypt(encrypted_data.encode()).decode()
    
    def _log_audit_event(self, user_id: str, action: str, resource: str, success: bool, details: dict):
        event = AuditEvent(
            timestamp=datetime.now(),
            user_id=user_id,
            action=action,
            resource=resource,
            success=success,
            details=details
        )
        
        audit_file = os.path.join(self.audit_log_path, f"audit_{datetime.now().strftime('%Y%m%d')}.json")
        
        audit_logs = []
        if os.path.exists(audit_file):
            with open(audit_file, 'r') as f:
                audit_logs = json.load(f)
        
        audit_logs.append({
            "timestamp": event.timestamp.isoformat(),
            "user_id": event.user_id,
            "action": event.action,
            "resource": event.resource,
            "success": event.success,
            "details": event.details
        })
        
        with open(audit_file, 'w') as f:
            json.dump(audit_logs, f, indent=2)
    
    def get_audit_logs(self, days_back: int = 7) -> List[dict]:
        if days_back <= 0:
            raise ValueError("Days back must be positive")
        
        logs = []
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        for filename in os.listdir(self.audit_log_path):
            if filename.startswith("audit_") and filename.endswith('.json'):
                file_path = os.path.join(self.audit_log_path, filename)
                
                try:
                    with open(file_path, 'r') as f:
                        file_logs = json.load(f)
                    
                    for log in file_logs:
                        log_time = datetime.fromisoformat(log['timestamp'])
                        if log_time >= cutoff_date:
                            logs.append(log)
                
                except (json.JSONDecodeError, KeyError, ValueError):
                    continue
        
        return sorted(logs, key=lambda x: x['timestamp'])