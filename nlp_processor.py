import re
from typing import List, Dict, Set, Tuple
from collections import Counter

class NLPProcessor:
    """Core NLP subagent for processing natural language text."""
    
    def __init__(self):
        self.technical_keywords = {
            'api', 'database', 'server', 'client', 'authentication', 'authorization',
            'endpoint', 'rest', 'graphql', 'sql', 'nosql', 'cache', 'redis',
            'microservice', 'docker', 'kubernetes', 'aws', 'azure', 'gcp'
        }
        
        self.ui_keywords = {
            'interface', 'ui', 'ux', 'design', 'layout', 'responsive', 'mobile',
            'desktop', 'button', 'form', 'navigation', 'menu', 'dashboard',
            'component', 'widget', 'theme', 'styling'
        }
        
        self.functional_keywords = {
            'user', 'customer', 'admin', 'login', 'register', 'search', 'filter',
            'create', 'update', 'delete', 'manage', 'process', 'workflow',
            'notification', 'email', 'report', 'export', 'import'
        }
        
        self.priority_indicators = {
            'critical': ['critical', 'urgent', 'must have', 'essential', 'required'],
            'high': ['important', 'high priority', 'needed', 'should have'],
            'medium': ['would like', 'nice to have', 'preferred', 'medium'],
            'low': ['optional', 'if possible', 'low priority', 'future']
        }

    def extract_entities(self, text: str) -> List[str]:
        """Extract named entities and important nouns from text."""
        # Simple entity extraction - in production, use spaCy or similar
        words = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        
        # Extract technical terms and domain-specific entities
        technical_entities = []
        text_lower = text.lower()
        
        for keyword in self.technical_keywords | self.ui_keywords | self.functional_keywords:
            if keyword in text_lower:
                technical_entities.append(keyword)
        
        return list(set(words + technical_entities))

    def extract_keywords(self, text: str) -> List[str]:
        """Extract relevant keywords from text."""
        # Remove common stop words and extract meaningful terms
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'}
        
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Count frequency and return most common
        word_freq = Counter(keywords)
        return [word for word, _ in word_freq.most_common(10)]

    def detect_priority(self, text: str) -> str:
        """Detect priority level from text indicators."""
        text_lower = text.lower()
        
        for priority, indicators in self.priority_indicators.items():
            if any(indicator in text_lower for indicator in indicators):
                return priority
        
        return 'medium'  # default

    def categorize_requirement(self, text: str, entities: List[str], keywords: List[str]) -> str:
        """Categorize requirement based on content analysis."""
        text_lower = text.lower()
        
        # Count matches for each category
        technical_score = sum(1 for word in keywords + entities if word.lower() in self.technical_keywords)
        ui_score = sum(1 for word in keywords + entities if word.lower() in self.ui_keywords)
        functional_score = sum(1 for word in keywords + entities if word.lower() in self.functional_keywords)
        
        # Determine category based on highest score
        scores = {
            'technical': technical_score,
            'ui_ux': ui_score,
            'functional': functional_score
        }
        
        return max(scores, key=scores.get) if max(scores.values()) > 0 else 'general'

    def calculate_confidence(self, text: str, entities: List[str], keywords: List[str]) -> float:
        """Calculate confidence score for the extracted information."""
        # Simple confidence calculation based on entity and keyword density
        word_count = len(text.split())
        entity_density = len(entities) / max(word_count, 1)
        keyword_density = len(keywords) / max(word_count, 1)
        
        # Normalize to 0-1 range
        confidence = min((entity_density + keyword_density) * 2, 1.0)
        return round(confidence, 2)