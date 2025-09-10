import asyncio
from datetime import datetime
from typing import Dict, Set, List
from models import UserConnection
import logging

logger = logging.getLogger(__name__)

class ConnectionPool:
    def __init__(self):
        self.connections: Dict[str, UserConnection] = {}
        self.rooms: Dict[str, Set[str]] = {"general": set()}
        self._cleanup_task = None
    
    async def add_connection(self, user_id: str, username: str, websocket, room_id: str = "general"):
        """Add new connection to pool"""
        connection = UserConnection(
            user_id=user_id,
            username=username,
            websocket=websocket,
            last_heartbeat=datetime.now(),
            room_id=room_id
        )
        
        self.connections[user_id] = connection
        
        if room_id not in self.rooms:
            self.rooms[room_id] = set()
        self.rooms[room_id].add(user_id)
        
        logger.info(f"User {username} connected to room {room_id}")
        
        # Start cleanup task if not running
        if not self._cleanup_task:
            self._cleanup_task = asyncio.create_task(self._periodic_cleanup())
    
    async def remove_connection(self, user_id: str):
        """Remove connection from pool"""
        if user_id in self.connections:
            connection = self.connections[user_id]
            room_id = connection.room_id
            
            del self.connections[user_id]
            self.rooms[room_id].discard(user_id)
            
            logger.info(f"User {connection.username} disconnected from room {room_id}")
    
    def update_heartbeat(self, user_id: str):
        """Update last heartbeat for connection"""
        if user_id in self.connections:
            self.connections[user_id].last_heartbeat = datetime.now()
    
    def get_room_connections(self, room_id: str) -> List[UserConnection]:
        """Get all active connections in a room"""
        if room_id not in self.rooms:
            return []
        
        return [
            self.connections[user_id] 
            for user_id in self.rooms[room_id] 
            if user_id in self.connections
        ]
    
    async def broadcast_to_room(self, room_id: str, message: str, exclude_user: str = None):
        """Broadcast message to all connections in room"""
        connections = self.get_room_connections(room_id)
        
        tasks = []
        for connection in connections:
            if exclude_user and connection.user_id == exclude_user:
                continue
            
            tasks.append(self._send_safe(connection.websocket, message))
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _send_safe(self, websocket, message: str):
        """Send message with error handling"""
        try:
            await websocket.send(message)
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
    
    async def _periodic_cleanup(self):
        """Remove stale connections periodically"""
        while True:
            try:
                await asyncio.sleep(30)  # Check every 30 seconds
                stale_users = [
                    user_id for user_id, conn in self.connections.items()
                    if not conn.is_alive()
                ]
                
                for user_id in stale_users:
                    await self.remove_connection(user_id)
                    
            except Exception as e:
                logger.error(f"Cleanup error: {e}")