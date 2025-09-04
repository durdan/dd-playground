from decimal import Decimal
from typing import Dict
from models import Team

class BudgetManager:
    def __init__(self):
        self._teams: Dict[str, Team] = {}
    
    def set_team_budget(self, team_name: str, budget_limit: Decimal, alert_threshold: Decimal = Decimal('0.8')) -> None:
        if not team_name:
            raise ValueError("team_name cannot be empty")
        if budget_limit <= 0:
            raise ValueError("budget_limit must be positive")
        if not (0 < alert_threshold <= 1):
            raise ValueError("alert_threshold must be between 0 and 1")
        
        self._teams[team_name] = Team(team_name, budget_limit, alert_threshold)
    
    def get_team_budget(self, team_name: str) -> Team:
        if team_name not in self._teams:
            raise ValueError(f"No budget set for team: {team_name}")
        return self._teams[team_name]
    
    def check_budget_status(self, team_name: str, current_cost: Decimal) -> tuple[bool, bool]:
        """Returns (exceeded_budget, exceeded_alert_threshold)"""
        team = self.get_team_budget(team_name)
        
        exceeded_budget = current_cost >= team.budget_limit
        alert_cost = team.budget_limit * team.alert_threshold
        exceeded_alert = current_cost >= alert_cost
        
        return exceeded_budget, exceeded_alert