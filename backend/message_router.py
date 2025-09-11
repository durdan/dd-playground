from typing import Dict
from chat_service import ChatService
from spec_generator_service import SpecGeneratorService

class MessageRouter:
    def __init__(self, chat_service: ChatService, spec_service: SpecGeneratorService):
        self.chat_service = chat_service
        self.spec_service = spec_service
        
    async def route_message(self, message: Dict) -> Dict:
        """Route message to appropriate handler."""
        message_type = message.get("type")
        
        if message_type == "chat":
            return self._handle_chat_message(message)
        elif message_type == "generate_spec":
            return await self._handle_spec_generation(message)
        elif message_type == "get_history":
            return self._handle_get_history(message)
        elif message_type == "get_spec":
            return self._handle_get_spec()
        else:
            return {
                "type": "error",
                "message": f"Unknown message type: {message_type}"
            }
            
    def _handle_chat_message(self, message: Dict) -> Dict:
        """Handle chat message."""
        try:
            username = message.get("username", "Anonymous")
            content = message.get("content", "")
            
            return self.chat_service.create_chat_message(username, content)
        except ValueError as e:
            return {
                "type": "error",
                "message": str(e)
            }
            
    async def _handle_spec_generation(self, message: Dict) -> Dict:
        """Handle spec generation request."""
        try:
            requirements = message.get("requirements", "")
            return await self.spec_service.generate_spec(requirements)
        except ValueError as e:
            return {
                "type": "error",
                "message": str(e)
            }
            
    def _handle_get_history(self, message: Dict) -> Dict:
        """Handle get message history request."""
        try:
            limit = message.get("limit", 50)
            history = self.chat_service.get_message_history(limit)
            return {
                "type": "history",
                "messages": history
            }
        except ValueError as e:
            return {
                "type": "error",
                "message": str(e)
            }
            
    def _handle_get_spec(self) -> Dict:
        """Handle get current spec request."""
        spec = self.spec_service.get_current_spec()
        return {
            "type": "current_spec",
            "spec": spec
        }