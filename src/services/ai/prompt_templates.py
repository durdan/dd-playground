from typing import Dict, Any
from enum import Enum

class SpecType(Enum):
    API = "api"
    DATABASE = "database"
    COMPONENT = "component"
    SYSTEM = "system"

class PromptTemplates:
    """Centralized prompt engineering for different spec types"""
    
    SYSTEM_PROMPTS = {
        SpecType.API: """You are an expert API architect. Generate comprehensive API specifications that are:
- RESTful and follow OpenAPI 3.0 standards
- Include proper HTTP methods, status codes, and error handling
- Define clear request/response schemas
- Consider security, validation, and performance
- Output valid JSON that can be parsed programmatically""",
        
        SpecType.DATABASE: """You are a database architect. Generate database specifications that are:
- Normalized and follow best practices
- Include proper relationships, constraints, and indexes
- Consider data types, performance, and scalability
- Include migration strategies
- Output valid JSON schema format""",
        
        SpecType.COMPONENT: """You are a software architect. Generate component specifications that are:
- Modular and follow SOLID principles
- Include clear interfaces and dependencies
- Consider testability and maintainability
- Define proper abstractions and contracts
- Output structured JSON specification""",
        
        SpecType.SYSTEM: """You are a system architect. Generate system specifications that are:
- Scalable and resilient
- Include proper service boundaries and communication patterns
- Consider deployment, monitoring, and operations
- Define clear architectural decisions and trade-offs
- Output comprehensive system design document"""
    }
    
    USER_PROMPTS = {
        SpecType.API: """Generate an API specification for: {description}

Requirements:
- Include all necessary endpoints
- Define request/response schemas
- Specify authentication and authorization
- Include error handling and status codes
- Consider rate limiting and caching

Context: {context}

Output the specification as valid JSON in this format:
{{
    "openapi": "3.0.0",
    "info": {{"title": "...", "version": "1.0.0"}},
    "paths": {{}},
    "components": {{"schemas": {{}}}}
}}""",
        
        SpecType.DATABASE: """Generate a database specification for: {description}

Requirements:
- Define all necessary tables and relationships
- Include proper data types and constraints
- Specify indexes for performance
- Consider data integrity and normalization
- Include sample queries

Context: {context}

Output the specification as valid JSON in this format:
{{
    "database": {{"name": "...", "type": "..."}},
    "tables": [{{}}],
    "relationships": [{{}}],
    "indexes": [{{}}]
}}""",
        
        SpecType.COMPONENT: """Generate a component specification for: {description}

Requirements:
- Define clear interfaces and contracts
- Specify dependencies and interactions
- Include configuration and lifecycle
- Consider error handling and logging
- Define testing strategies

Context: {context}

Output the specification as valid JSON in this format:
{{
    "component": {{"name": "...", "type": "..."}},
    "interfaces": [{{}}],
    "dependencies": [{{}}],
    "configuration": {{}},
    "lifecycle": {{}}
}}""",
        
        SpecType.SYSTEM: """Generate a system specification for: {description}

Requirements:
- Define system architecture and components
- Specify communication patterns and protocols
- Include deployment and scaling strategies
- Consider monitoring and observability
- Define security and compliance requirements

Context: {context}

Output the specification as valid JSON in this format:
{{
    "system": {{"name": "...", "type": "..."}},
    "components": [{{}}],
    "communication": [{{}}],
    "deployment": {{}},
    "monitoring": {{}}
}}"""
    }
    
    @classmethod
    def get_system_prompt(cls, spec_type: SpecType) -> str:
        """Get system prompt for spec type"""
        return cls.SYSTEM_PROMPTS.get(spec_type, "")
    
    @classmethod
    def get_user_prompt(cls, spec_type: SpecType, description: str, context: str = "") -> str:
        """Get formatted user prompt for spec type"""
        template = cls.USER_PROMPTS.get(spec_type, "")
        return template.format(description=description, context=context)
    
    @classmethod
    def create_refinement_prompt(cls, spec_type: SpecType, current_spec: str, feedback: str) -> str:
        """Create prompt for refining existing specification"""
        return f"""Refine the following {spec_type.value} specification based on the feedback:

Current Specification:
{current_spec}

Feedback:
{feedback}

Please update the specification to address the feedback while maintaining the same JSON format.
Focus on the specific issues mentioned and improve the overall quality."""