import unittest
from unittest.mock import Mock, patch, MagicMock
import requests
from jira_client import JiraClient, JiraConfig, plan_to_jira_format


class TestJiraConfig(unittest.TestCase):
    def test_validate_success(self):
        config = JiraConfig("http://test.com", "user", "token", "PROJ")
        config.validate()  # Should not raise
    
    def test_validate_missing_fields(self):
        config = JiraConfig("", "user", "token", "PROJ")
        with self.assertRaises(ValueError):
            config.validate()
    
    @patch.dict('os.environ', {
        'JIRA_URL': 'http://test.com',
        'JIRA_USERNAME': 'user',
        'JIRA_TOKEN': 'token',
        'JIRA_PROJECT_KEY': 'PROJ'
    })
    def test_from_env(self):
        config = JiraConfig.from_env()
        self.assertEqual(config.url, 'http://test.com')
        self.assertEqual(config.project_key, 'PROJ')


class TestJiraClient(unittest.TestCase):
    def setUp(self):
        self.config = JiraConfig("http://test.com", "user", "token", "PROJ")
        self.client = JiraClient(self.config)
    
    @patch('requests.Session.request')
    def test_create_ticket_success(self, mock_request):
        mock_response = Mock()
        mock_response.json.return_value = {"key": "PROJ-123"}
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response
        
        ticket_key = self.client.create_ticket("Test Summary", "Test Description")
        
        self.assertEqual(ticket_key, "PROJ-123")
        mock_request.assert_called_once()
    
    @patch('requests.Session.request')
    def test_create_ticket_api_error(self, mock_request):
        mock_request.side_effect = requests.exceptions.RequestException("API Error")
        
        with self.assertRaises(Exception) as context:
            self.client.create_ticket("Test", "Test")
        
        self.assertIn("Jira API error", str(context.exception))


class TestPlanToJiraFormat(unittest.TestCase):
    def test_basic_conversion(self):
        plan = "# Main Title\n## Section\n- Task 1\n- Task 2"
        title, description = plan_to_jira_format(plan)
        
        self.assertEqual(title, "Main Title")
        self.assertIn("h2. Section", description)
        self.assertIn("* Task 1", description)
    
    def test_no_title_provided(self):
        plan = "## Section\n- Task 1"
        title, description = plan_to_jira_format(plan, "Custom Title")
        
        self.assertEqual(title, "Custom Title")
        self.assertIn("h2. Section", description)
    
    def test_empty_plan(self):
        title, description = plan_to_jira_format("", "Test")
        self.assertEqual(title, "Test")
        self.assertEqual(description, "")


if __name__ == '__main__':
    unittest.main()