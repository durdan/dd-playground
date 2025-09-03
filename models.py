from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: int
    username: str
    password_hash: str
    role: str
    
    def is_admin(self) -> bool:
        return self.role == 'admin'