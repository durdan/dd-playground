from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
import json

@dataclass
class Message:
    id: Optional[str]
    content: str
    role: str  # 'user' or 'assistant'
    timestamp: datetime
    metadata: Optional[dict] = None

@dataclass
class ConversationThread:
    id: Optional[str]
    title: str
    parent_id: Optional[str]
    created_at: datetime
    updated_at: datetime
    messages: List[Message]
    metadata: Optional[dict] = None
    
    def add_message(self, content: str, role: str, metadata: Optional[dict] = None):
        """Add a message to this conversation thread."""
        message = Message(
            id=None,  # Will be set by storage layer
            content=content,
            role=role,
            timestamp=datetime.utcnow(),
            metadata=metadata
        )
        self.messages.append(message)
        self.updated_at = datetime.utcnow()
        return message
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'title': self.title,
            'parent_id': self.parent_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'messages': [
                {
                    'id': msg.id,
                    'content': msg.content,
                    'role': msg.role,
                    'timestamp': msg.timestamp.isoformat(),
                    'metadata': msg.metadata
                }
                for msg in self.messages
            ],
            'metadata': self.metadata
        }