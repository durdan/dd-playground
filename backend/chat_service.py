import time
from datetime import datetime
from typing import Dict, List

class ChatService:
    def __init__(self):
        self.message_history: List[Dict] = []
        
    def get_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        return datetime.now().isoformat()
        
    def create_chat_message(self, username: str, content: str) -> Dict:
        """Create a formatted chat message."""
        if not username or not username.strip():
            raise ValueError("Username cannot be empty")
        if not content or not content.strip():
            raise ValueError("Message content cannot be empty")
            
        message = {
            "type": "chat",
            "username": username.strip(),
            "content": content.strip(),
            "timestamp": self.get_timestamp(),
            "broadcast": True
        }
        
        self.message_history.append(message)
        return message
        
    def get_message_history(self, limit: int = 50) -> List[Dict]:
        """Get recent message history."""
        if limit <= 0:
            raise ValueError("Limit must be positive")
            
        return self.message_history[-limit:]
        
    def clear_history(self):
        """Clear message history."""
        self.message_history.clear()