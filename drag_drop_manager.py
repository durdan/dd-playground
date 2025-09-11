from typing import Optional, Dict, Any, List
from .diagram_element import DiagramElement, Position
from .event_emitter import EventEmitter
from .validation_service import ValidationService

class DragDropManager:
    def __init__(self, canvas_width: float, canvas_height: float):
        if canvas_width <= 0 or canvas_height <= 0:
            raise ValueError("Canvas dimensions must be positive")
            
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.dragging_element: Optional[DiagramElement] = None
        self.drag_offset: Optional[Position] = None
        self.events = EventEmitter()
        self.allow_overlaps = False
        self.snap_to_grid = False
        self.grid_size = 10
    
    def start_drag(self, element: DiagramElement, mouse_x: float, mouse_y: float) -> bool:
        """Start dragging an element"""
        if self.dragging_element is not None:
            return False  # Already dragging something
        
        if not element.contains_point(mouse_x, mouse_y):
            return False  # Click not on element
        
        self.dragging_element = element
        self.drag_offset = Position(
            mouse_x - element.position.x,
            mouse_y - element.position.y
        )
        element.is_dragging = True
        
        self.events.emit('drag_start', element, mouse_x, mouse_y)
        return True
    
    def update_drag(self, mouse_x: float, mouse_y: float, other_elements: List[DiagramElement] = None) -> bool:
        """Update drag position"""
        if not self.dragging_element or not self.drag_offset:
            return False
        
        new_x = mouse_x - self.drag_offset.x
        new_y = mouse_y - self.drag_offset.y
        
        if self.snap_to_grid:
            new_x = round(new_x / self.grid_size) * self.grid_size
            new_y = round(new_y / self.grid_size) * self.grid_size
        
        new_position = Position(new_x, new_y)
        
        # Validate the move
        validation_errors = ValidationService.validate_position_change(
            self.dragging_element, new_position, self.canvas_width, self.canvas_height,
            other_elements if not self.allow_overlaps else None
        )
        
        if not validation_errors:
            self.dragging_element.move_to(new_position)
            self.events.emit('drag_move', self.dragging_element, mouse_x, mouse_y)
            return True
        
        return False
    
    def end_drag(self, mouse_x: float, mouse_y: float) -> Optional[DiagramElement]:
        """End drag operation"""
        if not self.dragging_element:
            return None
        
        element = self.dragging_element
        element.is_dragging = False
        
        self.events.emit('drag_end', element, mouse_x, mouse_y)
        
        self.dragging_element = None
        self.drag_offset = None
        
        return element
    
    def cancel_drag(self, original_position: Position) -> Optional[DiagramElement]:
        """Cancel drag and restore original position"""
        if not self.dragging_element:
            return None
        
        element = self.dragging_element
        element.move_to(original_position)
        element.is_dragging = False
        
        self.events.emit('drag_cancel', element)
        
        self.dragging_element = None
        self.drag_offset = None
        
        return element