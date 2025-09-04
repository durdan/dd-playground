from datetime import datetime
from typing import Dict, List, Optional
from models import CostEntry
from storage import TimeSeriesStorage

class CostTracker:
    def __init__(self, storage: TimeSeriesStorage):
        self._storage = storage
        self._rate_cards: Dict[str, float] = {
            "compute_hour": 0.10,
            "storage_gb": 0.023,
            "network_gb": 0.09,
            "database_hour": 0.25
        }
    
    def set_rate(self, resource_type: str, rate_per_unit: float):
        if rate_per_unit < 0:
            raise ValueError("Rate cannot be negative")
        self._rate_cards[resource_type] = rate_per_unit
    
    def track_usage(self, resource_id: str, resource_type: str, 
                   service: str, usage_amount: float, usage_unit: str,
                   labels: Optional[Dict[str, str]] = None):
        
        rate = self._rate_cards.get(resource_type, 0.0)
        cost = usage_amount * rate
        
        cost_entry = CostEntry(
            resource_id=resource_id,
            resource_type=resource_type,
            service=service,
            cost=cost,
            usage_amount=usage_amount,
            usage_unit=usage_unit,
            timestamp=datetime.now(),
            labels=labels or {}
        )
        
        self._storage.store_cost(cost_entry)
        return cost_entry
    
    def get_service_costs(self, service: str, 
                         start_time: Optional[datetime] = None,
                         end_time: Optional[datetime] = None) -> List[CostEntry]:
        return self._storage.get_costs(start_time, end_time, service)
    
    def calculate_total_cost(self, service: Optional[str] = None,
                           start_time: Optional[datetime] = None,
                           end_time: Optional[datetime] = None) -> float:
        costs = self._storage.get_costs(start_time, end_time, service)
        return sum(cost.cost for cost in costs)