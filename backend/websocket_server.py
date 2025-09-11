import asyncio
import json
import logging
from typing import Dict, Set
import websockets
from websockets.server import WebSocketServerProtocol

from chat_service import ChatService
from spec_generator_service import SpecGeneratorService
from message_router import MessageRouter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebSocketServer:
    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port
        self.connections: Set[WebSocketServerProtocol] = set()
        self.chat_service = ChatService()
        self.spec_service = SpecGeneratorService()
        self.message_router = MessageRouter(self.chat_service, self.spec_service)
        
    async def register_connection(self, websocket: WebSocketServerProtocol):
        """Register a new WebSocket connection."""
        self.connections.add(websocket)
        logger.info(f"Client connected. Total connections: {len(self.connections)}")
        
        # Send welcome message
        await self.send_to_client(websocket, {
            "type": "system",
            "message": "Connected to chat server",
            "timestamp": self.chat_service.get_timestamp()
        })
        
    async def unregister_connection(self, websocket: WebSocketServerProtocol):
        """Unregister a WebSocket connection."""
        self.connections.discard(websocket)
        logger.info(f"Client disconnected. Total connections: {len(self.connections)}")
        
    async def send_to_client(self, websocket: WebSocketServerProtocol, message: Dict):
        """Send message to a specific client."""
        try:
            await websocket.send(json.dumps(message))
        except websockets.exceptions.ConnectionClosed:
            await self.unregister_connection(websocket)
            
    async def broadcast_to_all(self, message: Dict):
        """Broadcast message to all connected clients."""
        if not self.connections:
            return
            
        disconnected = set()
        for websocket in self.connections:
            try:
                await websocket.send(json.dumps(message))
            except websockets.exceptions.ConnectionClosed:
                disconnected.add(websocket)
                
        # Clean up disconnected clients
        for websocket in disconnected:
            await self.unregister_connection(websocket)
            
    async def handle_client(self, websocket: WebSocketServerProtocol, path: str):
        """Handle individual client connection."""
        await self.register_connection(websocket)
        
        try:
            async for raw_message in websocket:
                try:
                    message = json.loads(raw_message)
                    response = await self.message_router.route_message(message)
                    
                    if response.get("broadcast"):
                        await self.broadcast_to_all(response)
                    else:
                        await self.send_to_client(websocket, response)
                        
                except json.JSONDecodeError:
                    await self.send_to_client(websocket, {
                        "type": "error",
                        "message": "Invalid JSON format"
                    })
                except Exception as e:
                    logger.error(f"Error handling message: {e}")
                    await self.send_to_client(websocket, {
                        "type": "error",
                        "message": "Internal server error"
                    })
                    
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.unregister_connection(websocket)
            
    async def start_server(self):
        """Start the WebSocket server."""
        logger.info(f"Starting WebSocket server on {self.host}:{self.port}")
        
        server = await websockets.serve(
            self.handle_client,
            self.host,
            self.port
        )
        
        logger.info("WebSocket server started successfully")
        await server.wait_closed()

if __name__ == "__main__":
    server = WebSocketServer()
    asyncio.run(server.start_server())