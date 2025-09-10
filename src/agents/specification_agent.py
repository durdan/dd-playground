from typing import Dict, Any
from .base_agent import AIAgent, AgentResponse, AgentStatus, AgentError
import re

class SpecificationAgent(AIAgent):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("SpecificationAgent", config)
        self.templates = {
            "functional": self._get_functional_template(),
            "technical": self._get_technical_template(),
            "api": self._get_api_template()
        }
    
    def process(self, input_data: str, context: Dict[str, Any] = None) -> AgentResponse:
        try:
            self.validate_input(input_data)
            self.status = AgentStatus.PROCESSING
            
            context = context or {}
            spec_type = context.get("type", "functional")
            
            if spec_type not in self.templates:
                raise AgentError(f"Unknown specification type: {spec_type}", self.name)
            
            # Extract requirements from input
            requirements = self._extract_requirements(input_data)
            
            # Generate specification
            specification = self._generate_specification(requirements, spec_type)
            
            # Validate generated content
            validation_errors = self._validate_specification(specification)
            
            if validation_errors:
                return self._create_response(
                    content=specification,
                    status=AgentStatus.ERROR,
                    errors=validation_errors
                )
            
            self.status = AgentStatus.COMPLETED
            return self._create_response(
                content=specification,
                status=AgentStatus.COMPLETED,
                metadata={
                    "spec_type": spec_type,
                    "requirements_count": len(requirements),
                    "generated_sections": self._count_sections(specification)
                }
            )
            
        except AgentError:
            raise
        except Exception as e:
            self.status = AgentStatus.ERROR
            raise AgentError(f"Failed to generate specification: {str(e)}", self.name)
    
    def _extract_requirements(self, input_data: str) -> list:
        """Extract requirements from user input"""
        # Simple requirement extraction - look for sentences with action words
        action_words = ["should", "must", "will", "need", "require", "implement", "create", "build"]
        sentences = input_data.split('.')
        
        requirements = []
        for sentence in sentences:
            sentence = sentence.strip()
            if any(word in sentence.lower() for word in action_words):
                requirements.append(sentence)
        
        return requirements if requirements else [input_data]
    
    def _generate_specification(self, requirements: list, spec_type: str) -> str:
        """Generate specification based on requirements and type"""
        template = self.templates[spec_type]
        
        # Format requirements into specification sections
        formatted_requirements = "\n".join([f"- {req}" for req in requirements])
        
        specification = template.format(
            requirements=formatted_requirements,
            timestamp=self._get_timestamp()
        )
        
        return specification
    
    def _validate_specification(self, specification: str) -> list:
        """Validate generated specification"""
        errors = []
        
        if len(specification) < 100:
            errors.append("Specification too short")
        
        required_sections = ["Requirements", "Overview"]
        for section in required_sections:
            if section not in specification:
                errors.append(f"Missing required section: {section}")
        
        return errors
    
    def _count_sections(self, specification: str) -> int:
        """Count sections in specification"""
        return len(re.findall(r'^##\s+', specification, re.MULTILINE))
    
    def _get_timestamp(self) -> str:
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def _get_functional_template(self) -> str:
        return """# Functional Specification

## Overview
This specification outlines the functional requirements for the requested system.

## Requirements
{requirements}

## Acceptance Criteria
- All requirements must be implemented
- System must handle error cases gracefully
- User interface must be intuitive

Generated on: {timestamp}
"""
    
    def _get_technical_template(self) -> str:
        return """# Technical Specification

## Overview
This specification defines the technical implementation details.

## Requirements
{requirements}

## Architecture
- Modular design with clear separation of concerns
- Error handling and validation
- Extensible structure

## Implementation Notes
- Use appropriate design patterns
- Include comprehensive testing
- Follow coding standards

Generated on: {timestamp}
"""
    
    def _get_api_template(self) -> str:
        return """# API Specification

## Overview
This specification defines the API endpoints and data structures.

## Requirements
{requirements}

## Endpoints
- RESTful design principles
- Proper HTTP status codes
- JSON request/response format

## Error Handling
- Consistent error response format
- Appropriate error codes
- Clear error messages

Generated on: {timestamp}
"""