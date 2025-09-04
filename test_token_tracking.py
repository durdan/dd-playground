import unittest
from decimal import Decimal
from token_tracking_service import TokenTrackingService

class TestTokenTracking(unittest.TestCase):
    def setUp(self):
        self.service = TokenTrackingService()
    
    def test_track_usage_success(self):
        self.service.track_usage("repo1", "team1", "gpt-4", 1000, Decimal('0.02'))
        
        repo_summary = self.service.get_repo_usage("repo1")
        self.assertEqual(repo_summary.repo_name, "repo1")
        self.assertEqual(repo_summary.team, "team1")
        self.assertEqual(repo_summary.total_tokens, 1000)
        self.assertEqual(repo_summary.total_cost, Decimal('0.02'))
    
    def test_track_usage_invalid_input(self):
        with self.assertRaises(ValueError):
            self.service.track_usage("", "team1", "gpt-4", 1000, Decimal('0.02'))
        
        with self.assertRaises(ValueError):
            self.service.track_usage("repo1", "team1", "gpt-4", -1, Decimal('0.02'))
    
    def test_budget_alerts(self):
        # Setup team budget
        self.service.setup_team_budget("team1", Decimal('1.00'), Decimal('0.5'))
        
        # Track usage that exceeds alert threshold
        with self.assertLogs(level='WARNING') as log:
            self.service.track_usage("repo1", "team1", "gpt-4", 1000, Decimal('0.60'))
            self.assertIn("BUDGET ALERT", log.output[0])
    
    def test_budget_exceeded(self):
        # Setup team budget
        self.service.setup_team_budget("team1", Decimal('1.00'))
        
        # Track usage that exceeds budget
        with self.assertLogs(level='ERROR') as log:
            self.service.track_usage("repo1", "team1", "gpt-4", 1000, Decimal('1.50'))
            self.assertIn("BUDGET EXCEEDED", log.output[0])
    
    def test_multiple_repos_same_team(self):
        self.service.track_usage("repo1", "team1", "gpt-4", 1000, Decimal('0.02'))
        self.service.track_usage("repo2", "team1", "gpt-3.5", 500, Decimal('0.01'))
        
        team_summary = self.service.get_team_usage("team1")
        self.assertEqual(team_summary.total_tokens, 1500)
        self.assertEqual(team_summary.total_cost, Decimal('0.03'))
        self.assertEqual(len(team_summary.model_breakdown), 2)
    
    def test_repo_not_found(self):
        with self.assertRaises(ValueError):
            self.service.get_repo_usage("nonexistent")

if __name__ == '__main__':
    unittest.main()