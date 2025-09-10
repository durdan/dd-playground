from typing import List
from models import SpecificationType, SpecificationNeeds, Requirement

class SpecificationClassifier:
    """Identifies what types of specifications are needed based on requirements."""
    
    def __init__(self):
        self.type_indicators = {
            SpecificationType.FUNCTIONAL: [
                'user', 'workflow', 'process', 'business', 'feature', 'functionality'
            ],
            SpecificationType.TECHNICAL: [
                'api', 'database', 'server', 'architecture', 'technology', 'framework'
            ],
            SpecificationType.UI_UX: [
                'interface', 'design', 'layout', 'user experience', 'responsive', 'mobile'
            ],
            SpecificationType.API: [
                'endpoint', 'rest', 'graphql', 'integration', 'service', 'microservice'
            ],
            SpecificationType.DATABASE: [
                'data', 'storage', 'sql', 'nosql', 'schema', 'model'
            ],
            SpecificationType.SECURITY: [
                'authentication', 'authorization', 'security', 'permission', 'access'
            ],
            SpecificationType.PERFORMANCE: [
                'performance', 'speed', 'optimization', 'scalability', 'load'
            ],
            SpecificationType.INTEGRATION: [
                'integration', 'third-party', 'external', 'webhook', 'sync'
            ]
        }
    
    def classify_specification_needs(self, requirements: List[Requirement]) -> SpecificationNeeds:
        """Classify what specification types are needed."""
        if not requirements:
            raise ValueError("Requirements list cannot be empty")
        
        needed_types = self._identify_needed_types(requirements)
        complexity = self._assess_complexity(requirements, needed_types)
        effort = self._estimate_effort(requirements, complexity)
        dependencies = self._identify_dependencies(requirements)
        
        return SpecificationNeeds(
            types=needed_types,
            complexity=complexity,
            estimated_effort=effort,
            dependencies=dependencies
        )
    
    def _identify_needed_types(self, requirements: List[Requirement]) -> List[SpecificationType]:
        """Identify which specification types are needed."""
        type_scores = {spec_type: 0 for spec_type in SpecificationType}
        
        for requirement in requirements:
            all_text = f"{requirement.text} {' '.join(requirement.keywords)} {' '.join(requirement.entities)}"
            text_lower = all_text.lower()
            
            for spec_type, indicators in self.type_indicators.items():
                score = sum(1 for indicator in indicators if indicator in text_lower)
                type_scores[spec_type] += score
        
        # Return types with non-zero scores
        needed_types = [spec_type for spec_type, score in type_scores.items() if score > 0]
        
        # Always include functional if we have requirements
        if needed_types and SpecificationType.FUNCTIONAL not in needed_types:
            needed_types.append(SpecificationType.FUNCTIONAL)
        
        return needed_types or [SpecificationType.FUNCTIONAL]
    
    def _assess_complexity(self, requirements: List[Requirement], needed_types: List[SpecificationType]) -> str:
        """Assess overall complexity based on requirements and needed types."""
        req_count = len(requirements)
        type_count = len(needed_types)
        
        # Count high-priority requirements
        high_priority_count = sum(1 for req in requirements if req.priority in [req.priority.HIGH, req.priority.CRITICAL])
        
        if req_count <= 3 and type_count <= 2:
            return "simple"
        elif req_count <= 8 and type_count <= 4:
            return "moderate"
        else:
            return "complex"
    
    def _estimate_effort(self, requirements: List[Requirement], complexity: str) -> str:
        """Estimate development effort."""
        effort_map = {
            "simple": "low",
            "moderate": "medium",
            "complex": "high"
        }
        
        base_effort = effort_map[complexity]
        
        # Adjust based on critical requirements
        critical_count = sum(1 for req in requirements if req.priority == req.priority.CRITICAL)
        if critical_count > 2 and base_effort != "high":
            return "medium" if base_effort == "low" else "high"
        
        return base_effort
    
    def _identify_dependencies(self, requirements: List[Requirement]) -> List[str]:
        """Identify potential dependencies between requirements."""
        dependencies = []
        
        # Look for common entities across requirements
        all_entities = []
        for req in requirements:
            all_entities.extend(req.entities)
        
        # Find entities mentioned in multiple requirements
        from collections import Counter
        entity_counts = Counter(all_entities)
        shared_entities = [entity for entity, count in entity_counts.items() if count > 1]
        
        dependencies.extend(shared_entities)
        
        return list(set(dependencies))