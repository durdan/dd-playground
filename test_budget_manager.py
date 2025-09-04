import unittest
from decimal import Decimal
from budget_manager import BudgetManager

class TestBudgetManager(unittest.TestCase):
    def setUp(self):
        self.manager = BudgetManager()
    
    def test_set_team_budget_success(self):
        self.manager.set_team_budget("team1", Decimal('100.00'), Decimal('0.8'))
        team = self.manager.get_team_budget("team1")
        self.assertEqual(team.budget_limit, Decimal('100.00'))
        self.assertEqual(team.alert_threshold, Decimal('0.8'))
    
    def test_set_team_budget_invalid(self):
        with self.assertRaises(ValueError):
            self.manager.set_team_budget("", Decimal('100.00'))
        
        with self.assertRaises(ValueError):
            self.manager.set_team_budget("team1", Decimal('-10.00'))
        
        with self.assertRaises(ValueError):
            self.manager.set_team_budget("team1", Decimal('100.00'), Decimal('1.5'))
    
    def test_check_budget_status(self):
        self.manager.set_team_budget("team1", Decimal('100.00'), Decimal('0.8'))
        
        # Under alert threshold
        exceeded_budget, exceeded_alert = self.manager.check_budget_status("team1", Decimal('50.00'))
        self.assertFalse(exceeded_budget)
        self.assertFalse(exceeded_alert)
        
        # Over alert threshold, under budget
        exceeded_budget, exceeded_alert = self.manager.check_budget_status("team1", Decimal('85.00'))
        self.assertFalse(exceeded_budget)
        self.assertTrue(exceeded_alert)
        
        # Over budget
        exceeded_budget, exceeded_alert = self.manager.check_budget_status("team1", Decimal('150.00'))
        self.assertTrue(exceeded_budget)
        self.assertTrue(exceeded_alert)

if __name__ == '__main__':
    unittest.main()