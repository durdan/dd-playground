from typing import List
from models import Requirement, Priority
from nlp_processor import NLPProcessor
import uuid

class RequirementExtractor:
    """Extracts structured requirements from conversation text."""
    
    def __init__(self):
        self.nlp_processor = NLPProcessor()
    
    def extract_requirements(self, conversation_text: str) -> List[Requirement]:
        """Extract individual requirements from conversation text."""
        if not conversation_text or not conversation_text.strip():
            raise ValueError("Conversation text cannot be empty")
        
        # Split conversation into sentences/statements
        sentences = self._split_into_statements(conversation_text)
        
        requirements = []
        for sentence in sentences:
            if self._is_requirement_statement(sentence):
                requirement = self._create_requirement(sentence)
                requirements.append(requirement)
        
        return requirements
    
    def _split_into_statements(self, text: str) -> List[str]:
        """Split text into individual statements."""
        import re
        # Split on sentence boundaries, keeping meaningful statements
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]
    
    def _is_requirement_statement(self, statement: str) -> bool:
        """Determine if a statement contains a requirement."""
        requirement_indicators = [
            'need', 'want', 'require', 'should', 'must', 'have to',
            'would like', 'looking for', 'expect', 'feature', 'functionality'
        ]
        
        statement_lower = statement.lower()
        return any(indicator in statement_lower for indicator in requirement_indicators)
    
    def _create_requirement(self, statement: str) -> Requirement:
        """Create a structured requirement from a statement."""
        entities = self.nlp_processor.extract_entities(statement)
        keywords = self.nlp_processor.extract_keywords(statement)
        category = self.nlp_processor.categorize_requirement(statement, entities, keywords)
        priority_str = self.nlp_processor.detect_priority(statement)
        confidence = self.nlp_processor.calculate_confidence(statement, entities, keywords)
        
        # Convert priority string to enum
        priority = Priority(priority_str)
        
        return Requirement(
            id=str(uuid.uuid4()),
            text=statement.strip(),
            category=category,
            priority=priority,
            entities=entities,
            keywords=keywords,
            confidence=confidence
        )