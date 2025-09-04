from typing import List, Optional, Dict
from datetime import datetime, timedelta
from models import AgentUsage, CrewOperation, Budget
import json
import os

class CostRepository:
    """Persist cost tracking data"""
    
    def __init__(self, data_dir: str = "cost_data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
    
    def save_agent_usage(self, usage: AgentUsage) -> None:
        """Save agent usage record"""
        filename = f"{self.data_dir}/agent_usage.jsonl"
        with open(filename, "a") as f:
            data = {
                "agent_id": usage.agent_id,
                "agent_name": usage.agent_name,
                "operation_type": usage.operation_type.value,
                "model": usage.model,
                "input_tokens": usage.input_tokens,
                "output_tokens": usage.output_tokens,
                "cost": usage.cost,
                "timestamp": usage.timestamp.isoformat(),
                "crew_operation_id": usage.crew_operation_id,
                "metadata": usage.metadata
            }
            f.write(json.dumps(data) + "\n")
    
    def save_crew_operation(self, operation: CrewOperation) -> None:
        """Save crew operation record"""
        filename = f"{self.data_dir}/crew_operations.json"
        operations = self._load_json_file(filename, {})
        
        operations[operation.operation_id] = {
            "crew_name": operation.crew_name,
            "start_time": operation.start_time.isoformat(),
            "end_time": operation.end_time.isoformat() if operation.end_time else None,
            "total_cost": operation.total_cost,
            "status": operation.status,
            "agent_count": len(operation.agent_usages)
        }
        
        self._save_json_file(filename, operations)
    
    def save_budget(self, budget: Budget) -> None:
        """Save budget configuration"""
        filename = f"{self.data_dir}/budgets.json"
        budgets = self._load_json_file(filename, {})
        
        budgets[budget.budget_id] = {
            "name": budget.name,
            "limit": budget.limit,
            "spent": budget.spent,
            "period_start": budget.period_start.isoformat(),
            "period_end": budget.period_end.isoformat() if budget.period_end else None,
            "status": budget.status.value,
            "alert_threshold": budget.alert_threshold,
            "agents": budget.agents
        }
        
        self._save_json_file(filename, budgets)
    
    def get_usage_by_agent(self, agent_id: str, days: int = 30) -> List[AgentUsage]:
        """Get usage history for specific agent"""
        filename = f"{self.data_dir}/agent_usage.jsonl"
        if not os.path.exists(filename):
            return []
        
        cutoff_date = datetime.now() - timedelta(days=days)
        usages = []
        
        with open(filename, "r") as f:
            for line in f:
                data = json.loads(line.strip())
                timestamp = datetime.fromisoformat(data["timestamp"])
                
                if (data["agent_id"] == agent_id and timestamp >= cutoff_date):
                    usage = AgentUsage(
                        agent_id=data["agent_id"],
                        agent_name=data["agent_name"],
                        operation_type=OperationType(data["operation_type"]),
                        model=data["model"],
                        input_tokens=data["input_tokens"],
                        output_tokens=data["output_tokens"],
                        cost=data["cost"],
                        timestamp=timestamp,
                        crew_operation_id=data.get("crew_operation_id"),
                        metadata=data.get("metadata", {})
                    )
                    usages.append(usage)
        
        return usages
    
    def get_budget(self, budget_id: str) -> Optional[Budget]:
        """Get budget by ID"""
        filename = f"{self.data_dir}/budgets.json"
        budgets = self._load_json_file(filename, {})
        
        if budget_id not in budgets:
            return None
        
        data = budgets[budget_id]
        return Budget(
            budget_id=budget_id,
            name=data["name"],
            limit=data["limit"],
            spent=data["spent"],
            period_start=datetime.fromisoformat(data["period_start"]),
            period_end=datetime.fromisoformat(data["period_end"]) if data["period_end"] else None,
            status=BudgetStatus(data["status"]),
            alert_threshold=data["alert_threshold"],
            agents=data["agents"]
        )
    
    def _load_json_file(self, filename: str, default: dict) -> dict:
        """Load JSON file with default fallback"""
        if not os.path.exists(filename):
            return default
        with open(filename, "r") as f:
            return json.load(f)
    
    def _save_json_file(self, filename: str, data: dict) -> None:
        """Save data to JSON file"""
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)