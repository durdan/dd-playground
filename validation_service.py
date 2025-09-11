from typing import List
from .diagram_element import DiagramElement, Position, Size

class ValidationService:
    @staticmethod
    def validate_canvas_bounds(element: DiagramElement, canvas_width: float, canvas_height: float) -> bool:
        """Validate element is within canvas bounds"""
        if canvas_width <= 0 or canvas_height <= 0:
            raise ValueError("Canvas dimensions must be positive")
            
        bounds = element.get_bounds()
        return (bounds['left'] >= 0 and bounds['right'] <= canvas_width and
                bounds['top'] >= 0 and bounds['bottom'] <= canvas_height)
    
    @staticmethod
    def validate_no_overlaps(element: DiagramElement, other_elements: List[DiagramElement]) -> bool:
        """Validate element doesn't overlap with others"""
        return not any(element.overlaps_with(other) for other in other_elements if other.id != element.id)
    
    @staticmethod
    def validate_position_change(element: DiagramElement, new_position: Position, 
                                canvas_width: float, canvas_height: float,
                                other_elements: List[DiagramElement] = None) -> List[str]:
        """Validate position change and return list of errors"""
        errors = []
        
        # Create temporary element for validation
        temp_element = DiagramElement(
            element.id, new_position, element.size, element.element_type, element.properties
        )
        
        if not ValidationService.validate_canvas_bounds(temp_element, canvas_width, canvas_height):
            errors.append("Element would be outside canvas bounds")
        
        if other_elements and not ValidationService.validate_no_overlaps(temp_element, other_elements):
            errors.append("Element would overlap with existing elements")
        
        return errors