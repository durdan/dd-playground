import re
from typing import Dict, Any, List
from abc import ABC, abstractmethod

class ValidationError(Exception):
    """Custom exception for template validation issues."""
    pass

class DataProvider(ABC):
    """Abstract base class for data providers."""
    
    @abstractmethod
    def get_data(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Get data based on context."""
        pass

class UserDataProvider(DataProvider):
    """Provides user-specific data."""
    
    def __init__(self, user_data: Dict[str, Any]):
        self.user_data = user_data
    
    def get_data(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Return user data, optionally filtered by context."""
        if 'fields' in context:
            return {k: v for k, v in self.user_data.items() 
                   if k in context['fields']}
        return self.user_data.copy()

class AIContentProvider(DataProvider):
    """Generates AI content based on context."""
    
    def get_data(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI content based on context."""
        content_type = context.get('type', 'general')
        user_info = context.get('user_info', {})
        
        # Simulate AI content generation
        ai_content = {
            'summary': self._generate_summary(user_info),
            'recommendations': self._generate_recommendations(content_type, user_info),
            'analysis': self._generate_analysis(user_info)
        }
        
        return ai_content
    
    def _generate_summary(self, user_info: Dict[str, Any]) -> str:
        """Generate a summary based on user information."""
        name = user_info.get('name', 'User')
        role = user_info.get('role', 'professional')
        return f"This specification is tailored for {name}, a {role} with specific requirements."
    
    def _generate_recommendations(self, content_type: str, user_info: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on content type and user info."""
        base_recommendations = [
            "Follow industry best practices",
            "Ensure compliance with relevant standards",
            "Implement proper testing procedures"
        ]
        
        if content_type == 'technical':
            base_recommendations.extend([
                "Use version control for all deliverables",
                "Document all technical decisions"
            ])
        
        return base_recommendations
    
    def _generate_analysis(self, user_info: Dict[str, Any]) -> str:
        """Generate analysis based on user information."""
        experience = user_info.get('experience_level', 'intermediate')
        return f"Based on {experience} experience level, this specification includes appropriate detail and complexity."

class SpecificationTemplate:
    """Represents a specification template."""
    
    def __init__(self, name: str, content: str, metadata: Dict[str, Any] = None):
        self.name = name
        self.content = content
        self.metadata = metadata or {}
        self.variables = self._extract_variables()
    
    def _extract_variables(self) -> List[str]:
        """Extract variable names from template content."""
        pattern = r'\{\{(\w+)\}\}'
        return list(set(re.findall(pattern, self.content)))

class TemplateEngine:
    """Core template processing engine."""
    
    def __init__(self):
        self.variable_pattern = re.compile(r'\{\{(\w+)\}\}')
    
    def process_template(self, template: SpecificationTemplate, 
                        data: Dict[str, Any]) -> str:
        """Process template with provided data."""
        self._validate_data(template, data)
        
        processed_content = template.content
        for variable in template.variables:
            if variable in data:
                value = self._format_value(data[variable])
                processed_content = processed_content.replace(
                    f'{{{{{variable}}}}}', str(value)
                )
        
        return self._apply_formatting(processed_content)
    
    def _validate_data(self, template: SpecificationTemplate, 
                      data: Dict[str, Any]) -> None:
        """Validate that all required variables have data."""
        missing_vars = [var for var in template.variables if var not in data]
        if missing_vars:
            raise ValidationError(f"Missing data for variables: {missing_vars}")
    
    def _format_value(self, value: Any) -> str:
        """Format a value for template insertion."""
        if isinstance(value, list):
            return '\n'.join(f"• {item}" for item in value)
        return str(value)
    
    def _apply_formatting(self, content: str) -> str:
        """Apply professional formatting to the content."""
        # Remove extra whitespace and normalize line breaks
        lines = [line.strip() for line in content.split('\n')]
        formatted_lines = []
        
        for line in lines:
            if line:
                formatted_lines.append(line)
            elif formatted_lines and formatted_lines[-1]:  # Preserve single empty lines
                formatted_lines.append('')
        
        return '\n'.join(formatted_lines)

class TemplateProcessor:
    """Orchestrates the template processing pipeline."""
    
    def __init__(self):
        self.engine = TemplateEngine()
        self.data_providers: List[DataProvider] = []
    
    def add_data_provider(self, provider: DataProvider) -> None:
        """Add a data provider to the processing pipeline."""
        self.data_providers.append(provider)
    
    def process(self, template: SpecificationTemplate, 
               context: Dict[str, Any] = None) -> str:
        """Process a template with all registered data providers."""
        context = context or {}
        combined_data = {}
        
        # Collect data from all providers
        for provider in self.data_providers:
            provider_data = provider.get_data(context)
            combined_data.update(provider_data)
        
        # Process the template
        return self.engine.process_template(template, combined_data)