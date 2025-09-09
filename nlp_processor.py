from dataclasses import dataclass
from typing import List, Dict, Set, Optional
from enum import Enum
import re


class SpecType(Enum):
    API = "api"
    DATABASE = "database"
    UI = "ui"
    SYSTEM_ARCHITECTURE = "system_architecture"
    SECURITY = "security"
    PERFORMANCE = "performance"


class RequirementType(Enum):
    FUNCTIONAL = "functional"
    NON_FUNCTIONAL = "non_functional"
    CONSTRAINT = "constraint"


@dataclass
class Requirement:
    text: str
    type: RequirementType
    priority: str = "medium"  # high, medium, low
    entities: List[str] = None
    
    def __post_init__(self):
        if self.entities is None:
            self.entities = []


@dataclass
class StructuredInput:
    requirements: List[Requirement]
    spec_types: Set[SpecType]
    entities: Dict[str, List[str]]  # entity_type -> [entity_names]
    context: Dict[str, str]  # additional context info


class TextPreprocessor:
    """Handles text cleaning and normalization."""
    
    @staticmethod
    def clean_text(text: str) -> str:
        if not text or not isinstance(text, str):
            return ""
        
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text.strip())
        return text
    
    @staticmethod
    def extract_sentences(text: str) -> List[str]:
        """Split text into sentences."""
        text = TextPreprocessor.clean_text(text)
        if not text:
            return []
        
        # Simple sentence splitting
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]


class RequirementExtractor:
    """Extracts and categorizes requirements from text."""
    
    def __init__(self):
        self.functional_keywords = {
            'should', 'must', 'shall', 'will', 'can', 'allow', 'enable',
            'provide', 'support', 'create', 'generate', 'process', 'handle'
        }
        
        self.non_functional_keywords = {
            'performance', 'scalability', 'security', 'reliability', 'availability',
            'usability', 'maintainability', 'fast', 'secure', 'responsive'
        }
        
        self.constraint_keywords = {
            'cannot', 'must not', 'limited', 'restricted', 'only', 'maximum',
            'minimum', 'within', 'budget', 'deadline', 'constraint'
        }
    
    def extract_requirements(self, text: str) -> List[Requirement]:
        """Extract requirements from text."""
        if not text:
            return []
        
        sentences = TextPreprocessor.extract_sentences(text)
        requirements = []
        
        for sentence in sentences:
            req_type = self._classify_requirement(sentence)
            if req_type:
                priority = self._determine_priority(sentence)
                entities = self._extract_entities(sentence)
                
                requirement = Requirement(
                    text=sentence,
                    type=req_type,
                    priority=priority,
                    entities=entities
                )
                requirements.append(requirement)
        
        return requirements
    
    def _classify_requirement(self, sentence: str) -> Optional[RequirementType]:
        """Classify sentence as functional, non-functional, or constraint."""
        sentence_lower = sentence.lower()
        
        # Check for constraint indicators first
        if any(keyword in sentence_lower for keyword in self.constraint_keywords):
            return RequirementType.CONSTRAINT
        
        # Check for non-functional indicators
        if any(keyword in sentence_lower for keyword in self.non_functional_keywords):
            return RequirementType.NON_FUNCTIONAL
        
        # Check for functional indicators
        if any(keyword in sentence_lower for keyword in self.functional_keywords):
            return RequirementType.FUNCTIONAL
        
        # If it looks like a requirement but doesn't match patterns, assume functional
        if any(word in sentence_lower for word in ['system', 'user', 'application', 'feature']):
            return RequirementType.FUNCTIONAL
        
        return None
    
    def _determine_priority(self, sentence: str) -> str:
        """Determine priority based on keywords."""
        sentence_lower = sentence.lower()
        
        high_priority_words = {'critical', 'essential', 'must', 'required', 'urgent'}
        low_priority_words = {'nice to have', 'optional', 'could', 'might', 'wish'}
        
        if any(word in sentence_lower for word in high_priority_words):
            return "high"
        elif any(word in sentence_lower for word in low_priority_words):
            return "low"
        
        return "medium"
    
    def _extract_entities(self, sentence: str) -> List[str]:
        """Extract potential entities (nouns, technical terms)."""
        # Simple entity extraction - look for capitalized words and technical terms
        entities = []
        
        # Find capitalized words (potential proper nouns)
        capitalized = re.findall(r'\b[A-Z][a-z]+\b', sentence)
        entities.extend(capitalized)
        
        # Find technical terms
        tech_patterns = [
            r'\b\w+API\b', r'\bAPI\w*\b',  # API related
            r'\b\w*DB\b', r'\bdatabase\b',  # Database related
            r'\bUI\b', r'\bGUI\b',  # UI related
            r'\b\w+Service\b', r'\bservice\w*\b'  # Service related
        ]
        
        for pattern in tech_patterns:
            matches = re.findall(pattern, sentence, re.IGNORECASE)
            entities.extend(matches)
        
        return list(set(entities))  # Remove duplicates


class SpecTypeIdentifier:
    """Identifies what types of specifications are needed."""
    
    def __init__(self):
        self.spec_indicators = {
            SpecType.API: {
                'api', 'endpoint', 'rest', 'graphql', 'service', 'microservice',
                'request', 'response', 'json', 'http', 'webhook'
            },
            SpecType.DATABASE: {
                'database', 'db', 'table', 'schema', 'sql', 'nosql', 'mongodb',
                'postgresql', 'mysql', 'data', 'storage', 'persistence'
            },
            SpecType.UI: {
                'ui', 'interface', 'frontend', 'web', 'mobile', 'app', 'screen',
                'page', 'form', 'button', 'menu', 'dashboard', 'user interface'
            },
            SpecType.SYSTEM_ARCHITECTURE: {
                'architecture', 'system', 'component', 'module', 'integration',
                'deployment', 'infrastructure', 'scalability', 'distributed'
            },
            SpecType.SECURITY: {
                'security', 'authentication', 'authorization', 'encryption',
                'secure', 'login', 'password', 'token', 'ssl', 'https'
            },
            SpecType.PERFORMANCE: {
                'performance', 'speed', 'fast', 'latency', 'throughput',
                'optimization', 'cache', 'load', 'response time'
            }
        }
    
    def identify_spec_types(self, requirements: List[Requirement]) -> Set[SpecType]:
        """Identify needed specification types based on requirements."""
        if not requirements:
            return set()
        
        spec_types = set()
        all_text = ' '.join([req.text.lower() for req in requirements])
        
        for spec_type, keywords in self.spec_indicators.items():
            if any(keyword in all_text for keyword in keywords):
                spec_types.add(spec_type)
        
        # Default to system architecture if no specific types identified
        if not spec_types:
            spec_types.add(SpecType.SYSTEM_ARCHITECTURE)
        
        return spec_types


class InputStructurer:
    """Structures user input for spec generators."""
    
    def structure_input(self, requirements: List[Requirement], 
                       spec_types: Set[SpecType]) -> StructuredInput:
        """Convert requirements and spec types into structured format."""
        entities = self._group_entities(requirements)
        context = self._extract_context(requirements)
        
        return StructuredInput(
            requirements=requirements,
            spec_types=spec_types,
            entities=entities,
            context=context
        )
    
    def _group_entities(self, requirements: List[Requirement]) -> Dict[str, List[str]]:
        """Group entities by type."""
        entities = {
            'technical_terms': [],
            'components': [],
            'data_objects': [],
            'other': []
        }
        
        for req in requirements:
            for entity in req.entities:
                entity_lower = entity.lower()
                
                if any(term in entity_lower for term in ['api', 'service', 'db', 'database']):
                    entities['technical_terms'].append(entity)
                elif any(term in entity_lower for term in ['component', 'module', 'system']):
                    entities['components'].append(entity)
                elif entity.isupper() or entity.istitle():
                    entities['data_objects'].append(entity)
                else:
                    entities['other'].append(entity)
        
        # Remove duplicates
        for key in entities:
            entities[key] = list(set(entities[key]))
        
        return entities
    
    def _extract_context(self, requirements: List[Requirement]) -> Dict[str, str]:
        """Extract contextual information."""
        context = {}
        
        # Count requirement types
        functional_count = sum(1 for req in requirements if req.type == RequirementType.FUNCTIONAL)
        non_functional_count = sum(1 for req in requirements if req.type == RequirementType.NON_FUNCTIONAL)
        constraint_count = sum(1 for req in requirements if req.type == RequirementType.CONSTRAINT)
        
        context['requirement_distribution'] = f"Functional: {functional_count}, Non-functional: {non_functional_count}, Constraints: {constraint_count}"
        
        # Identify high priority requirements
        high_priority = [req.text for req in requirements if req.priority == "high"]
        if high_priority:
            context['high_priority_requirements'] = '; '.join(high_priority[:3])  # Top 3
        
        return context


class NLPProcessor:
    """Main NLP processing orchestrator."""
    
    def __init__(self):
        self.requirement_extractor = RequirementExtractor()
        self.spec_type_identifier = SpecTypeIdentifier()
        self.input_structurer = InputStructurer()
    
    def process(self, user_input: str) -> StructuredInput:
        """Process user input and return structured data."""
        if not user_input or not isinstance(user_input, str):
            raise ValueError("User input must be a non-empty string")
        
        # Extract requirements
        requirements = self.requirement_extractor.extract_requirements(user_input)
        
        if not requirements:
            raise ValueError("No valid requirements found in input")
        
        # Identify needed specification types
        spec_types = self.spec_type_identifier.identify_spec_types(requirements)
        
        # Structure the input
        structured_input = self.input_structurer.structure_input(requirements, spec_types)
        
        return structured_input
    
    def get_summary(self, structured_input: StructuredInput) -> Dict[str, any]:
        """Get a summary of the processed input."""
        return {
            'total_requirements': len(structured_input.requirements),
            'requirement_types': {
                req_type.value: sum(1 for req in structured_input.requirements if req.type == req_type)
                for req_type in RequirementType
            },
            'spec_types_needed': [spec_type.value for spec_type in structured_input.spec_types],
            'priority_distribution': {
                priority: sum(1 for req in structured_input.requirements if req.priority == priority)
                for priority in ['high', 'medium', 'low']
            },
            'total_entities': sum(len(entities) for entities in structured_input.entities.values())
        }