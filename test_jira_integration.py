import unittest
from unittest.mock import patch, Mock
import tempfile
import os
from cli import handle_jira_integration


class TestJiraIntegration(unittest.TestCase):
    def setUp(self):
        self.mock_args = Mock()
        self.mock_args.jira = False
        self.mock_args.jira_update = None
        self.plan_content = "# Test Plan\n## Tasks\n- Task 1\n- Task 2"
    
    def test_no_jira_flags(self):
        # Should return early without doing anything
        handle_jira_integration(self.plan_content, self.mock_args)
        # No assertions needed - just shouldn't crash
    
    @patch('cli.JiraClient')
    @patch('cli.JiraConfig.from_env')
    def test_create_ticket(self, mock_config, mock_client_class):
        self.mock_args.jira = True
        mock_client = Mock()
        mock_client.create_ticket.return_value = "PROJ-123"
        mock_client_class.return_value = mock_client
        mock_config.return_value = Mock(url="http://test.com")
        
        with patch('builtins.print') as mock_print:
            handle_jira_integration(self.plan_content, self.mock_args)
        
        mock_client.create_ticket.assert_called_once()
        mock_print.assert_called()
    
    @patch('cli.JiraClient')
    @patch('cli.JiraConfig.from_env')
    def test_update_ticket(self, mock_config, mock_client_class):
        self.mock_args.jira_update = "PROJ-456"
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        mock_config.return_value = Mock(url="http://test.com")
        
        with patch('builtins.print') as mock_print:
            handle_jira_integration(self.plan_content, self.mock_args)
        
        mock_client.update_ticket.assert_called_once_with("PROJ-456", "Test Plan", unittest.mock.ANY)
        mock_print.assert_called()
    
    @patch('cli.JiraConfig.from_env')
    def test_jira_error_handling(self, mock_config):
        self.mock_args.jira = True
        mock_config.side_effect = ValueError("Missing config")
        
        with patch('builtins.print') as mock_print:
            handle_jira_integration(self.plan_content, self.mock_args)
        
        # Should print error message
        mock_print.assert_called()
        printed_text = str(mock_print.call_args)
        self.assertIn("Jira integration failed", printed_text)


if __name__ == '__main__':
    unittest.main()