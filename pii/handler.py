from typing import Dict, List, Optional
from .detector import PIIDetector, PIIMatch
from security.encryption import EncryptionService
from security.access_control import AccessControl, Permission
from security.audit import AuditLogger

class PIIHandler:
    def __init__(self, encryption_service: EncryptionService, 
                 access_control: AccessControl, audit_logger: AuditLogger):
        self.detector = PIIDetector()
        self.encryption = encryption_service
        self.access_control = access_control
        self.audit = audit_logger
    
    def mask_pii(self, text: str, mask_char: str = '*') -> str:
        """Mask PII in text for display purposes"""
        if not text:
            return text
        
        matches = self.detector.detect_pii(text)
        if not matches:
            return text
        
        # Sort matches by start position in reverse order
        matches.sort(key=lambda x: x.start, reverse=True)
        
        masked_text = text
        for match in matches:
            if match.pii_type == 'email':
                # Mask email: j***@example.com
                parts = match.value.split('@')
                masked_value = parts[0][0] + mask_char * (len(parts[0]) - 1) + '@' + parts[1]
            elif match.pii_type == 'ssn':
                # Mask SSN: ***-**-1234
                masked_value = mask_char * 7 + match.value[-4:]
            elif match.pii_type == 'credit_card':
                # Mask credit card: ****-****-****-1234
                clean_value = match.value.replace('-', '').replace(' ', '')
                masked_value = mask_char * 12 + clean_value[-4:]
            else:
                # Default masking
                masked_value = mask_char * len(match.value)
            
            masked_text = masked_text[:match.start] + masked_value + masked_text[match.end:]
        
        return masked_text
    
    def encrypt_pii_data(self, data: Dict[str, str], user_id: str) -> Dict[str, str]:
        """Encrypt PII fields in data dictionary"""
        self.access_control.require_permission(user_id, Permission.WRITE_PII)
        
        encrypted_data = {}
        for key, value in data.items():
            if self.detector.has_pii(value):
                encrypted_data[key] = self.encryption.encrypt(value)
                self.audit.log_pii_access(user_id, key, "encrypt")
            else:
                encrypted_data[key] = value
        
        return encrypted_data
    
    def decrypt_pii_data(self, encrypted_data: Dict[str, str], user_id: str) -> Dict[str, str]:
        """Decrypt PII fields in data dictionary"""
        self.access_control.require_permission(user_id, Permission.READ_PII)
        
        decrypted_data = {}
        for key, value in encrypted_data.items():
            try:
                # Try to decrypt - if it fails, assume it wasn't encrypted
                decrypted_value = self.encryption.decrypt(value)
                if self.detector.has_pii(decrypted_value):
                    self.audit.log_pii_access(user_id, key, "decrypt")
                decrypted_data[key] = decrypted_value
            except ValueError:
                # Not encrypted data
                decrypted_data[key] = value
        
        return decrypted_data
    
    def anonymize_data(self, data: Dict[str, str]) -> Dict[str, str]:
        """Anonymize PII data by replacing with generic values"""
        anonymized = {}
        for key, value in data.items():
            matches = self.detector.detect_pii(value)
            if matches:
                anonymized_value = value
                for match in sorted(matches, key=lambda x: x.start, reverse=True):
                    replacement = self._get_anonymous_replacement(match.pii_type)
                    anonymized_value = (anonymized_value[:match.start] + 
                                      replacement + 
                                      anonymized_value[match.end:])
                anonymized[key] = anonymized_value
            else:
                anonymized[key] = value
        
        return anonymized
    
    def _get_anonymous_replacement(self, pii_type: str) -> str:
        """Get anonymous replacement for PII type"""
        replacements = {
            'email': 'user@example.com',
            'ssn': '000-00-0000',
            'phone': '000-000-0000',
            'credit_card': '0000-0000-0000-0000',
            'ip_address': '0.0.0.0'
        }
        return replacements.get(pii_type, '[REDACTED]')