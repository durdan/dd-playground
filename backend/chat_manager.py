import json
from typing import Optional
from message_handler import MessageHandler
from connection_pool import ConnectionPool
from models import ChatMessage

class ChatManager:
    def __init__(self):
        self.message_handler = MessageHandler()
        self.connection_pool = ConnectionPool()
        self.message_history = []  # In production, use proper storage
        self.max_history = 100
    
    async def handle_connection(self, websocket, path):
        """Handle new WebSocket connection"""
        user_id = None
        try:
            # Wait for initial join message
            raw_message = await websocket.recv()
            message = self.message_handler.validate_message(raw_message)
            
            if not message or message['type'] != 'join':
                await websocket.send(json.dumps({
                    'type': 'error',
                    'message': 'First message must be join type'
                }))
                return
            
            user_id = message['user_id']
            username = message['username']
            room_id = message.get('room_id', 'general')
            
            await self.connection_pool.add_connection(user_id, username, websocket, room_id)
            
            # Send recent message history
            await self._send_history(websocket, room_id)
            
            # Notify room about new user
            await self._broadcast_user_joined(user_id, username, room_id)
            
            # Handle incoming messages
            async for raw_message in websocket:
                await self._process_incoming_message(raw_message, user_id)
                
        except Exception as e:
            print(f"Connection error: {e}")
        finally:
            if user_id:
                await self.connection_pool.remove_connection(user_id)
    
    async def _process_incoming_message(self, raw_message: str, user_id: str):
        """Process and route incoming message"""
        message = self.message_handler.validate_message(raw_message)
        if not message:
            return
        
        if message['type'] == 'heartbeat':
            self.connection_pool.update_heartbeat(user_id)
            return
        
        chat_message = self.message_handler.process_message(message)
        if chat_message:
            await self._handle_chat_message(chat_message)
    
    async def _handle_chat_message(self, chat_message: ChatMessage):
        """Handle and broadcast chat message"""
        # Store message (with size limit)
        self.message_history.append(chat_message)
        if len(self.message_history) > self.max_history:
            self.message_history.pop(0)
        
        # Broadcast to room
        message_json = json.dumps({
            'type': 'message',
            'data': chat_message.to_dict()
        })
        
        await self.connection_pool.broadcast_to_room(
            chat_message.room_id, 
            message_json
        )
    
    async def _send_history(self, websocket, room_id: str):
        """Send recent message history to new connection"""
        room_messages = [
            msg for msg in self.message_history[-20:] 
            if msg.room_id == room_id
        ]
        
        if room_messages:
            history_data = json.dumps({
                'type': 'history',
                'messages': [msg.to_dict() for msg in room_messages]
            })
            await websocket.send(history_data)
    
    async def _broadcast_user_joined(self, user_id: str, username: str, room_id: str):
        """Broadcast user joined notification"""
        notification = json.dumps({
            'type': 'user_joined',
            'user_id': user_id,
            'username': username,
            'room_id': room_id
        })
        
        await self.connection_pool.broadcast_to_room(
            room_id, 
            notification, 
            exclude_user=user_id
        )