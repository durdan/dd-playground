import unittest
from template_engine import (
    TemplateEngine, TemplateProcessor, SpecificationTemplate,
    UserDataProvider, AIContentProvider, ValidationError
)

class TestTemplateEngine(unittest.TestCase):
    
    def setUp(self):
        self.engine = TemplateEngine()
        self.template = SpecificationTemplate(
            "test_spec",
            "Project: {{project_name}}\nOwner: {{name}}\nSummary: {{summary}}"
        )
    
    def test_successful_processing(self):
        data = {
            'project_name': 'Test Project',
            'name': 'John Doe',
            'summary': 'A test project specification'
        }
        result = self.engine.process_template(self.template, data)
        
        self.assertIn('Project: Test Project', result)
        self.assertIn('Owner: John Doe', result)
        self.assertIn('Summary: A test project specification', result)
    
    def test_missing_variable_validation(self):
        data = {'project_name': 'Test Project'}  # Missing 'name' and 'summary'
        
        with self.assertRaises(ValidationError) as context:
            self.engine.process_template(self.template, data)
        
        self.assertIn('Missing data for variables', str(context.exception))
    
    def test_list_formatting(self):
        template = SpecificationTemplate(
            "list_test",
            "Requirements:\n{{requirements}}"
        )
        data = {
            'requirements': ['Requirement 1', 'Requirement 2', 'Requirement 3']
        }
        
        result = self.engine.process_template(template, data)
        self.assertIn('• Requirement 1', result)
        self.assertIn('• Requirement 2', result)

class TestDataProviders(unittest.TestCase):
    
    def test_user_data_provider(self):
        user_data = {'name': 'Alice', 'role': 'developer', 'email': 'alice@example.com'}
        provider = UserDataProvider(user_data)
        
        result = provider.get_data({})
        self.assertEqual(result, user_data)
        
        # Test filtered data
        filtered_result = provider.get_data({'fields': ['name', 'role']})
        expected = {'name': 'Alice', 'role': 'developer'}
        self.assertEqual(filtered_result, expected)
    
    def test_ai_content_provider(self):
        provider = AIContentProvider()
        context = {
            'type': 'technical',
            'user_info': {'name': 'Bob', 'experience_level': 'senior'}
        }
        
        result = provider.get_data(context)
        
        self.assertIn('summary', result)
        self.assertIn('recommendations', result)
        self.assertIn('analysis', result)
        self.assertIn('Bob', result['summary'])
        self.assertIn('senior', result['analysis'])

class TestTemplateProcessor(unittest.TestCase):
    
    def test_full_processing_pipeline(self):
        processor = TemplateProcessor()
        
        # Add data providers
        user_data = {'name': 'Charlie', 'role': 'manager', 'experience_level': 'senior'}
        processor.add_data_provider(UserDataProvider(user_data))
        processor.add_data_provider(AIContentProvider())
        
        # Create template
        template = SpecificationTemplate(
            "full_spec",
            "Name: {{name}}\nRole: {{role}}\n\n{{summary}}\n\nAnalysis: {{analysis}}"
        )
        
        context = {'type': 'technical', 'user_info': user_data}
        result = processor.process(template, context)
        
        self.assertIn('Name: Charlie', result)
        self.assertIn('Role: manager', result)
        self.assertIn('This specification is tailored for Charlie', result)
        self.assertIn('senior experience level', result)
    
    def test_empty_context(self):
        processor = TemplateProcessor()
        user_data = {'name': 'Dave'}
        processor.add_data_provider(UserDataProvider(user_data))
        
        template = SpecificationTemplate("simple", "Hello {{name}}")
        result = processor.process(template)  # No context provided
        
        self.assertEqual(result, "Hello Dave")

class TestSpecificationTemplate(unittest.TestCase):
    
    def test_variable_extraction(self):
        template = SpecificationTemplate(
            "test",
            "{{var1}} and {{var2}} and {{var1}} again"
        )
        
        # Should extract unique variables
        self.assertEqual(set(template.variables), {'var1', 'var2'})
    
    def test_no_variables(self):
        template = SpecificationTemplate("test", "No variables here")
        self.assertEqual(template.variables, [])

if __name__ == '__main__':
    unittest.main()