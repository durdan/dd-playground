import unittest
from message_processor import MessageProcessor
from spec_types import SpecType

class TestMessageProcessor(unittest.TestCase):
    
    def setUp(self):
        self.processor = MessageProcessor()
    
    def test_process_api_message(self):
        message = "I need to create a REST API endpoint for user authentication"
        result = self.processor.process_message(message)
        
        self.assertEqual(result.spec_type, SpecType.API)
        self.assertIn("authentication", ' '.join(result.extracted_requirements))
        self.assertIn("# Api Specification", result.formatted_response)
        self.assertIn("