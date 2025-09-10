import asyncio
import json
import websockets
import uuid
from datetime import datetime
from typing import Dict, Set
from specification import SpecificationManager
from comment_system import CommentManager
from user_session import UserSessionManager

class CollaborationServer:
    def __init__(self):
        self.spec_manager = SpecificationManager()
        self.comment_manager = CommentManager()
        self.session_manager = UserSessionManager()
        self.connections: Dict[str, websockets.WebSocketServerProtocol] = {}
        
    async def register_user(self, websocket, user_data):
        """Register a new user connection"""
        user_id = str(uuid.uuid4())
        username = user_data.get('username', f'User_{user_id[:8]}')
        
        self.connections[user_id] = websocket
        self.session_manager.add_user(user_id, username)
        
        # Send current state to new user
        await self.send_to_user(user_id, {
            'type': 'init',
            'user_id': user_id,
            'specification': self.spec_manager.get_current_spec(),
            'comments': self.comment_manager.get_all_comments(),
            'active_users': self.session_manager.get_active_users(),
            'versions': self.spec_manager.get_version_history()
        })
        
        # Notify others of new user
        await self.broadcast_except_user(user_id, {
            'type': 'user_joined',
            'user': {'id': user_id, 'username': username}
        })
        
        return user_id
    
    async def unregister_user(self, user_id):
        """Remove user connection"""
        if user_id in self.connections:
            username = self.session_manager.get_username(user_id)
            del self.connections[user_id]
            self.session_manager.remove_user(user_id)
            
            await self.broadcast({
                'type': 'user_left',
                'user': {'id': user_id, 'username': username}
            })
    
    async def handle_message(self, user_id, message):
        """Process incoming messages from users"""
        try:
            data = json.loads(message)
            msg_type = data.get('type')
            
            if msg_type == 'spec_update':
                await self.handle_spec_update(user_id, data)
            elif msg_type == 'add_comment':
                await self.handle_add_comment(user_id, data)
            elif msg_type == 'resolve_comment':
                await self.handle_resolve_comment(user_id, data)
            elif msg_type == 'cursor_position':
                await self.handle_cursor_update(user_id, data)
            else:
                print(f"Unknown message type: {msg_type}")
                
        except json.JSONDecodeError:
            await self.send_error(user_id, "Invalid JSON message")
        except Exception as e:
            await self.send_error(user_id, f"Error processing message: {str(e)}")
    
    async def handle_spec_update(self, user_id, data):
        """Handle specification content updates"""
        content = data.get('content', '')
        section = data.get('section', 'main')
        
        if not content.strip():
            await self.send_error(user_id, "Content cannot be empty")
            return
            
        username = self.session_manager.get_username(user_id)
        version_id = self.spec_manager.update_specification(content, section, username)
        
        await self.broadcast_except_user(user_id, {
            'type': 'spec_updated',
            'content': content,
            'section': section,
            'version_id': version_id,
            'updated_by': username,
            'timestamp': datetime.now().isoformat()
        })
    
    async def handle_add_comment(self, user_id, data):
        """Handle new comment creation"""
        text = data.get('text', '').strip()
        section = data.get('section', 'main')
        line_number = data.get('line_number', 0)
        
        if not text:
            await self.send_error(user_id, "Comment text cannot be empty")
            return
            
        username = self.session_manager.get_username(user_id)
        comment = self.comment_manager.add_comment(text, section, line_number, user_id, username)
        
        await self.broadcast({
            'type': 'comment_added',
            'comment': comment
        })
    
    async def handle_resolve_comment(self, user_id, data):
        """Handle comment resolution"""
        comment_id = data.get('comment_id')
        
        if not comment_id:
            await self.send_error(user_id, "Comment ID required")
            return
            
        username = self.session_manager.get_username(user_id)
        success = self.comment_manager.resolve_comment(comment_id, user_id, username)
        
        if success:
            await self.broadcast({
                'type': 'comment_resolved',
                'comment_id': comment_id,
                'resolved_by': username
            })
        else:
            await self.send_error(user_id, "Comment not found or already resolved")
    
    async def handle_cursor_update(self, user_id, data):
        """Handle cursor position updates for user awareness"""
        position = data.get('position', 0)
        section = data.get('section', 'main')
        username = self.session_manager.get_username(user_id)
        
        await self.broadcast_except_user(user_id, {
            'type': 'cursor_update',
            'user_id': user_id,
            'username': username,
            'position': position,
            'section': section
        })
    
    async def send_to_user(self, user_id, message):
        """Send message to specific user"""
        if user_id in self.connections:
            try:
                await self.connections[user_id].send(json.dumps(message))
            except websockets.exceptions.ConnectionClosed:
                await self.unregister_user(user_id)
    
    async def send_error(self, user_id, error_message):
        """Send error message to user"""
        await self.send_to_user(user_id, {
            'type': 'error',
            'message': error_message
        })
    
    async def broadcast(self, message):
        """Broadcast message to all connected users"""
        if self.connections:
            await asyncio.gather(
                *[self.send_to_user(user_id, message) for user_id in self.connections],
                return_exceptions=True
            )
    
    async def broadcast_except_user(self, exclude_user_id, message):
        """Broadcast message to all users except specified one"""
        targets = [uid for uid in self.connections if uid != exclude_user_id]
        if targets:
            await asyncio.gather(
                *[self.send_to_user(user_id, message) for user_id in targets],
                return_exceptions=True
            )
    
    async def handle_connection(self, websocket, path):
        """Handle new WebSocket connection"""
        user_id = None
        try:
            # Wait for initial user data
            initial_message = await websocket.recv()
            user_data = json.loads(initial_message)
            
            if user_data.get('type') != 'join':
                await websocket.send(json.dumps({'type': 'error', 'message': 'Expected join message'}))
                return
                
            user_id = await self.register_user(websocket, user_data)
            
            # Handle subsequent messages
            async for message in websocket:
                await self.handle_message(user_id, message)
                
        except websockets.exceptions.ConnectionClosed:
            pass
        except Exception as e:
            print(f"Connection error: {e}")
        finally:
            if user_id:
                await self.unregister_user(user_id)

async def main():
    server = CollaborationServer()
    print("Starting collaboration server on localhost:8765")
    await websockets.serve(server.handle_connection, "localhost", 8765)
    await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())