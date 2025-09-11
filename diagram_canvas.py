from typing import List, Optional, Dict, Any
from .diagram_element import DiagramElement, Position, Size
from .drag_drop_manager import DragDropManager
from .event_emitter import EventEmitter

class DiagramCanvas:
    def __init__(self, width: float, height: float):
        if width <= 0 or height <= 0:
            raise ValueError("Canvas dimensions must be positive")
            
        self.width = width
        self.height = height
        self.elements: Dict[str, DiagramElement] = {}
        self.drag_manager = DragDropManager(width, height)
        self.events = EventEmitter()
        self.selected_elements: List[str] = []
    
    def add_element(self, element: DiagramElement) -> bool:
        """Add element to canvas"""
        if element.id in self.elements:
            raise ValueError(f"Element with ID '{element.id}' already exists")
        
        # Validate element fits in canvas
        bounds = element.get_bounds()
        if (bounds['right'] > self.width or bounds['bottom'] > self.height or
            bounds['left'] < 0 or bounds['top'] < 0):
            raise ValueError("Element exceeds canvas boundaries")
        
        # Check for overlaps if not allowed
        if not self.drag_manager.allow_overlaps:
            for existing in self.elements.values():
                if element.overlaps_with(existing):
                    raise ValueError("Element overlaps with existing element")
        
        self.elements[element.id] = element
        self.events.emit('element_added', element)
        return True
    
    def remove_element(self, element_id: str) -> bool:
        """Remove element from canvas"""
        if element_id not in self.elements:
            return False
        
        element = self.elements.pop(element_id)
        if element_id in self.selected_elements:
            self.selected_elements.remove(element_id)
        
        self.events.emit('element_removed', element)
        return True
    
    def get_element(self, element_id: str) -> Optional[DiagramElement]:
        """Get element by ID"""
        return self.elements.get(element_id)
    
    def get_element_at_position(self, x: float, y: float) -> Optional[DiagramElement]:
        """Get topmost element at position"""
        # Return elements in reverse order (topmost first)
        for element in reversed(list(self.elements.values())):
            if element.contains_point(x, y):
                return element
        return None
    
    def select_element(self, element_id: str) -> bool:
        """Select an element"""
        if element_id not in self.elements:
            return False
        
        if element_id not in self.selected_elements:
            self.selected_elements.append(element_id)
            self.elements[element_id].is_selected = True
            self.events.emit('element_selected', self.elements[element_id])
        
        return True
    
    def deselect_element(self, element_id: str) -> bool:
        """Deselect an element"""
        if element_id in self.selected_elements:
            self.selected_elements.remove(element_id)
            self.elements[element_id].is_selected = False
            self.events.emit('element_deselected', self.elements[element_id])
            return True
        return False
    
    def clear_selection(self):
        """Clear all selections"""
        for element_id in self.selected_elements.copy():
            self.deselect_element(element_id)
    
    def handle_mouse_down(self, x: float, y: float) -> bool:
        """Handle mouse down event"""
        element = self.get_element_at_position(x, y)
        if element:
            self.clear_selection()
            self.select_element(element.id)
            return self.drag_manager.start_drag(element, x, y)
        else:
            self.clear_selection()
        return False
    
    def handle_mouse_move(self, x: float, y: float) -> bool:
        """Handle mouse move event"""
        other_elements = [e for e in self.elements.values() 
                         if e.id != (self.drag_manager.dragging_element.id 
                                   if self.drag_manager.dragging_element else None)]
        return self.drag_manager.update_drag(x, y, other_elements)
    
    def handle_mouse_up(self, x: float, y: float) -> Optional[DiagramElement]:
        """Handle mouse up event"""
        return self.drag_manager.end_drag(x, y)
    
    def get_canvas_state(self) -> Dict[str, Any]:
        """Get current canvas state"""
        return {
            'width': self.width,
            'height': self.height,
            'element_count': len(self.elements),
            'selected_count': len(self.selected_elements),
            'is_dragging': self.drag_manager.dragging_element is not None
        }