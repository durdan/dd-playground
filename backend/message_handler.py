import json
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from models import ChatMessage

class MessageHandler:
    def __init__(self):
        self.message_types = {
            'chat': self._handle_chat_message,
            'join': self._handle_join_room,
            'leave': self._handle_leave_room,
            'heartbeat': self._handle_heartbeat
        }
    
    def validate_message(self, raw_message: str) -> Optional[Dict[str, Any]]:
        """Validate and parse incoming message"""
        try:
            message = json.loads(raw_message)
            required_fields = ['type', 'user_id', 'username']
            
            if not all(field in message for field in required_fields):
                raise ValueError("Missing required fields")
            
            if message['type'] not in self.message_types:
                raise ValueError(f"Unknown message type: {message['type']}")
            
            return message
        except (json.JSONDecodeError, ValueError) as e:
            return None
    
    def process_message(self, message: Dict[str, Any]) -> Optional[ChatMessage]:
        """Process validated message and return ChatMessage if applicable"""
        handler = self.message_types.get(message['type'])
        return handler(message) if handler else None
    
    def _handle_chat_message(self, message: Dict[str, Any]) -> ChatMessage:
        if not message.get('content', '').strip():
            raise ValueError("Empty message content")
        
        return ChatMessage(
            user_id=message['user_id'],
            username=message['username'],
            content=message['content'].strip(),
            timestamp=datetime.now(),
            message_id=str(uuid.uuid4()),
            room_id=message.get('room_id', 'general')
        )
    
    def _handle_join_room(self, message: Dict[str, Any]) -> None:
        # Room joining logic handled by chat_manager
        return None
    
    def _handle_leave_room(self, message: Dict[str, Any]) -> None:
        # Room leaving logic handled by chat_manager
        return None
    
    def _handle_heartbeat(self, message: Dict[str, Any]) -> None:
        # Heartbeat handled by connection_pool
        return None