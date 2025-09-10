import asyncio
import websockets
import logging
from chat_manager import ChatManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebSocketServer:
    def __init__(self, host='localhost', port=8765):
        self.host = host
        self.port = port
        self.chat_manager = ChatManager()
    
    async def start(self):
        """Start the WebSocket server"""
        logger.info(f"Starting WebSocket server on {self.host}:{self.port}")
        
        async with websockets.serve(
            self.chat_manager.handle_connection,
            self.host,
            self.port,
            ping_interval=20,
            ping_timeout=10
        ):
            logger.info("WebSocket server started successfully")
            await asyncio.Future()  # Run forever

if __name__ == "__main__":
    server = WebSocketServer()
    asyncio.run(server.start())