import json
from typing import Dict, Any, List
from specification_engine import SpecificationModel, Requirement

class SpecGenerator:
    """AI-powered specification generator"""
    
    def __init__(self, ai_client=None):
        self.ai_client = ai_client  # Mock for now, would be OpenAI client
        
    def generate_specification(self, user_requirements: str) -> SpecificationModel:
        """Generate structured specification from user requirements"""
        if not user_requirements or not user_requirements.strip():
            raise ValueError("User requirements cannot be empty")
            
        # Extract key information
        parsed_requirements = self._parse_requirements(user_requirements)
        
        # Generate structured spec
        spec = self._build_specification(parsed_requirements)
        
        return spec
    
    def _parse_requirements(self, requirements: str) -> Dict[str, Any]:
        """Parse and extract structured data from requirements text"""
        # In real implementation, this would use AI to extract structured data
        # For now, using simple keyword extraction
        
        lines = [line.strip() for line in requirements.split('\n') if line.strip()]
        
        parsed = {
            'title': self._extract_title(lines),
            'overview': self._extract_overview(requirements),
            'functional_reqs': self._extract_functional_requirements(lines),
            'non_functional_reqs': self._extract_non_functional_requirements(lines),
            'constraints': self._extract_constraints(lines),
            'assumptions': self._extract_assumptions(lines),
            'dependencies': self._extract_dependencies(lines)
        }
        
        return parsed
    
    def _extract_title(self, lines: List[str]) -> str:
        """Extract project title from requirements"""
        for line in lines[:3]:  # Check first 3 lines
            if any(keyword in line.lower() for keyword in ['project', 'system', 'application', 'platform']):
                return line
        return lines[0] if lines else "Untitled Project"
    
    def _extract_overview(self, requirements: str) -> str:
        """Extract project overview"""
        sentences = requirements.split('.')
        return '. '.join(sentences[:2]) + '.' if len(sentences) >= 2 else requirements[:200]
    
    def _extract_functional_requirements(self, lines: List[str]) -> List[Dict[str, Any]]:
        """Extract functional requirements"""
        functional_reqs = []
        req_id = 1
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['must', 'should', 'shall', 'will', 'user can', 'system will']):
                functional_reqs.append({
                    'id': f'FR-{req_id:03d}',
                    'description': line,
                    'priority': self._determine_priority(line),
                    'category': 'Functional',
                    'acceptance_criteria': [f"Verify that {line.lower()}"]
                })
                req_id += 1
                
        return functional_reqs
    
    def _extract_non_functional_requirements(self, lines: List[str]) -> List[Dict[str, Any]]:
        """Extract non-functional requirements"""
        non_functional_reqs = []
        req_id = 1
        
        nfr_keywords = ['performance', 'security', 'scalability', 'availability', 'usability', 'reliability']
        
        for line in lines:
            if any(keyword in line.lower() for keyword in nfr_keywords):
                non_functional_reqs.append({
                    'id': f'NFR-{req_id:03d}',
                    'description': line,
                    'priority': self._determine_priority(line),
                    'category': 'Non-Functional',
                    'acceptance_criteria': [f"Measure and verify {line.lower()}"]
                })
                req_id += 1
                
        return non_functional_reqs
    
    def _extract_constraints(self, lines: List[str]) -> List[str]:
        """Extract project constraints"""
        constraints = []
        for line in lines:
            if any(keyword in line.lower() for keyword in ['constraint', 'limitation', 'restriction', 'cannot', 'must not']):
                constraints.append(line)
        return constraints
    
    def _extract_assumptions(self, lines: List[str]) -> List[str]:
        """Extract project assumptions"""
        assumptions = []
        for line in lines:
            if any(keyword in line.lower() for keyword in ['assume', 'assumption', 'expect', 'given that']):
                assumptions.append(line)
        return assumptions
    
    def _extract_dependencies(self, lines: List[str]) -> List[str]:
        """Extract project dependencies"""
        dependencies = []
        for line in lines:
            if any(keyword in line.lower() for keyword in ['depend', 'require', 'integrate', 'api', 'service']):
                dependencies.append(line)
        return dependencies
    
    def _determine_priority(self, requirement: str) -> str:
        """Determine requirement priority based on keywords"""
        req_lower = requirement.lower()
        if any(keyword in req_lower for keyword in ['critical', 'must', 'essential', 'required']):
            return 'High'
        elif any(keyword in req_lower for keyword in ['should', 'important', 'preferred']):
            return 'Medium'
        else:
            return 'Low'
    
    def _build_specification(self, parsed_data: Dict[str, Any]) -> SpecificationModel:
        """Build SpecificationModel from parsed data"""
        functional_reqs = [
            Requirement(
                id=req['id'],
                description=req['description'],
                priority=req['priority'],
                category=req['category'],
                acceptance_criteria=req['acceptance_criteria']
            ) for req in parsed_data['functional_reqs']
        ]
        
        non_functional_reqs = [
            Requirement(
                id=req['id'],
                description=req['description'],
                priority=req['priority'],
                category=req['category'],
                acceptance_criteria=req['acceptance_criteria']
            ) for req in parsed_data['non_functional_reqs']
        ]
        
        return SpecificationModel(
            title=parsed_data['title'],
            overview=parsed_data['overview'],
            functional_requirements=functional_reqs,
            non_functional_requirements=non_functional_reqs,
            constraints=parsed_data['constraints'],
            assumptions=parsed_data['assumptions'],
            dependencies=parsed_data['dependencies']
        )