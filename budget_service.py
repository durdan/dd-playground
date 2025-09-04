from typing import List, Optional
from datetime import datetime
from models import Budget, BudgetStatus, AgentUsage
from cost_repository import CostRepository

class BudgetService:
    """Business logic for budget management"""
    
    def __init__(self, repository: CostRepository):
        self.repository = repository
    
    def create_budget(self, name: str, limit: float, agents: List[str] = None) -> Budget:
        """Create new budget"""
        if limit <= 0:
            raise ValueError("Budget limit must be positive")
        
        budget_id = f"budget_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        budget = Budget(
            budget_id=budget_id,
            name=name,
            limit=limit,
            agents=agents or []
        )
        
        self.repository.save_budget(budget)
        return budget
    
    def update_budget_spending(self, budget_id: str, usage: AgentUsage) -> Budget:
        """Update budget with new spending"""
        budget = self.repository.get_budget(budget_id)
        if not budget:
            raise ValueError(f"Budget not found: {budget_id}")
        
        # Check if usage applies to this budget
        if budget.agents and usage.agent_id not in budget.agents:
            return budget
        
        budget.spent += usage.cost
        budget.status = self._calculate_budget_status(budget)
        
        self.repository.save_budget(budget)
        return budget
    
    def check_budget_limits(self, budget_id: str, planned_cost: float) -> bool:
        """Check if planned cost would exceed budget"""
        budget = self.repository.get_budget(budget_id)
        if not budget:
            return True  # No budget = no limits
        
        return (budget.spent + planned_cost) <= budget.limit
    
    def get_budget_alerts(self, budget_id: str) -> List[str]:
        """Get budget alert messages"""
        budget = self.repository.get_budget(budget_id)
        if not budget:
            return []
        
        alerts = []
        usage_percent = budget.spent / budget.limit
        
        if budget.status == BudgetStatus.EXCEEDED:
            alerts.append(f"Budget '{budget.name}' exceeded! Spent: ${budget.spent:.2f} / ${budget.limit:.2f}")
        elif usage_percent >= budget.alert_threshold:
            alerts.append(f"Budget '{budget.name}' at {usage_percent:.1%} of limit")
        
        return alerts
    
    def _calculate_budget_status(self, budget: Budget) -> BudgetStatus:
        """Calculate budget status based on spending"""
        usage_percent = budget.spent / budget.limit
        
        if usage_percent >= 1.0:
            return BudgetStatus.EXCEEDED
        elif usage_percent >= budget.alert_threshold:
            return BudgetStatus.WARNING
        else:
            return BudgetStatus.ACTIVE