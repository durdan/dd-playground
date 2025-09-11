from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class Position:
    x: float
    y: float
    
    def __post_init__(self):
        if not isinstance(self.x, (int, float)) or not isinstance(self.y, (int, float)):
            raise ValueError("Position coordinates must be numeric")

@dataclass
class Size:
    width: float
    height: float
    
    def __post_init__(self):
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Size dimensions must be positive")

class DiagramElement:
    def __init__(self, element_id: str, position: Position, size: Size, 
                 element_type: str = "rectangle", properties: Optional[Dict[str, Any]] = None):
        if not element_id or not isinstance(element_id, str):
            raise ValueError("Element ID must be a non-empty string")
        if not element_type or not isinstance(element_type, str):
            raise ValueError("Element type must be a non-empty string")
            
        self.id = element_id
        self.position = position
        self.size = size
        self.element_type = element_type
        self.properties = properties or {}
        self.is_dragging = False
        self.is_selected = False
    
    def get_bounds(self) -> Dict[str, float]:
        """Get element boundaries"""
        return {
            'left': self.position.x,
            'right': self.position.x + self.size.width,
            'top': self.position.y,
            'bottom': self.position.y + self.size.height
        }
    
    def contains_point(self, x: float, y: float) -> bool:
        """Check if point is within element bounds"""
        bounds = self.get_bounds()
        return (bounds['left'] <= x <= bounds['right'] and 
                bounds['top'] <= y <= bounds['bottom'])
    
    def move_to(self, new_position: Position):
        """Move element to new position"""
        self.position = new_position
    
    def overlaps_with(self, other: 'DiagramElement') -> bool:
        """Check if this element overlaps with another"""
        self_bounds = self.get_bounds()
        other_bounds = other.get_bounds()
        
        return not (self_bounds['right'] < other_bounds['left'] or
                   self_bounds['left'] > other_bounds['right'] or
                   self_bounds['bottom'] < other_bounds['top'] or
                   self_bounds['top'] > other_bounds['bottom'])