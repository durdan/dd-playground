from decimal import Decimal
from token_tracker import TokenUsageTracker
from budget_manager import BudgetManager
from alert_service import AlertService

class TokenTrackingService:
    def __init__(self):
        self.tracker = TokenUsageTracker()
        self.budget_manager = BudgetManager()
        self.alert_service = AlertService()
        self._alerted_teams = set()  # Track teams already alerted to avoid spam
    
    def setup_team_budget(self, team_name: str, budget_limit: Decimal, alert_threshold: Decimal = Decimal('0.8')) -> None:
        self.budget_manager.set_team_budget(team_name, budget_limit, alert_threshold)
    
    def track_usage(self, repo_name: str, team: str, model: str, tokens: int, cost: Decimal) -> None:
        # Record the usage
        self.tracker.record_usage(repo_name, team, model, tokens, cost)
        
        # Check budget if team has one set
        try:
            team_summary = self.tracker.get_team_summary(team)
            exceeded_budget, exceeded_alert = self.budget_manager.check_budget_status(team, team_summary.total_cost)
            
            if exceeded_budget:
                team_budget = self.budget_manager.get_team_budget(team)
                self.alert_service.send_budget_exceeded(team, team_summary.total_cost, team_budget.budget_limit)
            elif exceeded_alert and team not in self._alerted_teams:
                team_budget = self.budget_manager.get_team_budget(team)
                self.alert_service.send_budget_alert(team, team_summary.total_cost, team_budget.budget_limit)
                self._alerted_teams.add(team)
                
        except ValueError:
            # Team doesn't have budget set, skip budget checks
            pass
    
    def get_repo_usage(self, repo_name: str):
        return self.tracker.get_repo_summary(repo_name)
    
    def get_team_usage(self, team: str):
        return self.tracker.get_team_summary(team)