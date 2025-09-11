import asyncio
import json
from typing import Dict, Optional
from datetime import datetime

class SpecGeneratorService:
    def __init__(self):
        self.current_spec: Optional[Dict] = None
        self.generation_in_progress = False
        
    async def generate_spec(self, requirements: str) -> Dict:
        """Generate API specification from requirements."""
        if not requirements or not requirements.strip():
            raise ValueError("Requirements cannot be empty")
            
        if self.generation_in_progress:
            return {
                "type": "spec_error",
                "message": "Specification generation already in progress"
            }
            
        self.generation_in_progress = True
        
        try:
            # Send initial status
            status_message = {
                "type": "spec_status",
                "status": "generating",
                "message": "Starting specification generation...",
                "timestamp": datetime.now().isoformat(),
                "broadcast": True
            }
            
            # Simulate spec generation process
            await asyncio.sleep(1)  # Simulate processing time
            
            # Generate mock specification
            spec = self._create_mock_spec(requirements)
            self.current_spec = spec
            
            return {
                "type": "spec_update",
                "spec": spec,
                "timestamp": datetime.now().isoformat(),
                "broadcast": True
            }
            
        finally:
            self.generation_in_progress = False
            
    def _create_mock_spec(self, requirements: str) -> Dict:
        """Create a mock API specification."""
        return {
            "openapi": "3.0.0",
            "info": {
                "title": "Generated API",
                "version": "1.0.0",
                "description": f"API generated from: {requirements[:100]}..."
            },
            "paths": {
                "/api/data": {
                    "get": {
                        "summary": "Get data",
                        "responses": {
                            "200": {
                                "description": "Success",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "data": {"type": "array"},
                                                "status": {"type": "string"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        
    def get_current_spec(self) -> Optional[Dict]:
        """Get the current specification."""
        return self.current_spec
        
    def clear_spec(self):
        """Clear the current specification."""
        self.current_spec = None