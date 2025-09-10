from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional
import json

@dataclass
class ChatMessage:
    user_id: str
    username: str
    content: str
    timestamp: datetime
    message_id: str
    room_id: str = "general"
    
    def to_dict(self):
        return {
            **asdict(self),
            'timestamp': self.timestamp.isoformat()
        }
    
    def to_json(self):
        return json.dumps(self.to_dict())

@dataclass
class UserConnection:
    user_id: str
    username: str
    websocket: object
    last_heartbeat: datetime
    room_id: str = "general"
    
    def is_alive(self, timeout_seconds: int = 30) -> bool:
        return (datetime.now() - self.last_heartbeat).seconds < timeout_seconds