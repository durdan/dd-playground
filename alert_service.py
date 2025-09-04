import logging
from decimal import Decimal

logger = logging.getLogger(__name__)

class AlertService:
    def send_budget_alert(self, team: str, current_cost: Decimal, budget_limit: Decimal) -> None:
        logger.warning(f"BUDGET ALERT: Team '{team}' has spent ${current_cost} of ${budget_limit} budget")
    
    def send_budget_exceeded(self, team: str, current_cost: Decimal, budget_limit: Decimal) -> None:
        logger.error(f"BUDGET EXCEEDED: Team '{team}' has spent ${current_cost}, exceeding budget of ${budget_limit}")