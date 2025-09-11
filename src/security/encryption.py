import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class SecurityManager:
    def __init__(self, password: str):
        """Initialize with a password for encryption."""
        self.password = password.encode()
        self._key = self._derive_key()
        self._cipher = Fernet(self._key)
    
    def _derive_key(self) -> bytes:
        """Derive encryption key from password."""
        salt = b'conversation_salt_2023'  # In production, use random salt per user
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.password))
        return key
    
    def encrypt(self, data: str) -> str:
        """Encrypt sensitive data."""
        if not data:
            return data
        encrypted = self._cipher.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt sensitive data."""
        if not encrypted_data:
            return encrypted_data
        try:
            decoded = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted = self._cipher.decrypt(decoded)
            return decrypted.decode()
        except Exception as e:
            raise ValueError(f"Failed to decrypt data: {e}")
    
    def hash_for_search(self, content: str) -> str:
        """Create searchable hash of content (one-way)."""
        digest = hashes.Hash(hashes.SHA256())
        digest.update(content.lower().encode())
        return base64.urlsafe_b64encode(digest.finalize()).decode()[:16]