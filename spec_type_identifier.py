from typing import List
from spec_types import SpecType

class SpecTypeIdentifier:
    """Identifies the type of specification based on requirements."""
    
    def __init__(self):
        self.type_keywords = {
            SpecType.API: ['api', 'endpoint', 'rest', 'graphql', 'service', 'request', 'response'],
            SpecType.UI: ['ui', 'interface', 'frontend', 'component', 'button', 'form', 'page'],
            SpecType.ALGORITHM: ['algorithm', 'sort', 'search', 'optimize', 'calculate', 'solve'],
            SpecType.DATA_STRUCTURE: ['data structure', 'array', 'list', 'tree', 'graph', 'hash'],
            SpecType.SYSTEM_DESIGN: ['system', 'architecture', 'scalable', 'distributed', 'microservice'],
            SpecType.DATABASE: ['database', 'sql', 'table', 'schema', 'query', 'storage']
        }
    
    def identify_spec_type(self, requirements: List[str]) -> SpecType:
        """Identify specification type from requirements."""
        if not requirements:
            return SpecType.GENERAL
        
        combined_text = ' '.join(requirements).lower()
        type_scores = {}
        
        for spec_type, keywords in self.type_keywords.items():
            score = sum(1 for keyword in keywords if keyword in combined_text)
            if score > 0:
                type_scores[spec_type] = score
        
        if not type_scores:
            return SpecType.GENERAL
        
        return max(type_scores, key=type_scores.get)