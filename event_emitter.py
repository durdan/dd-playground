from typing import Dict, List, Callable, Any

class EventEmitter:
    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = {}
    
    def on(self, event: str, callback: Callable):
        """Register event listener"""
        if not isinstance(event, str) or not event:
            raise ValueError("Event name must be a non-empty string")
        if not callable(callback):
            raise ValueError("Callback must be callable")
            
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(callback)
    
    def off(self, event: str, callback: Callable):
        """Remove event listener"""
        if event in self._listeners and callback in self._listeners[event]:
            self._listeners[event].remove(callback)
    
    def emit(self, event: str, *args, **kwargs):
        """Emit event to all listeners"""
        if event in self._listeners:
            for callback in self._listeners[event]:
                try:
                    callback(*args, **kwargs)
                except Exception as e:
                    # Log error but don't stop other listeners
                    print(f"Error in event listener for '{event}': {e}")