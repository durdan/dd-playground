from datetime import datetime
from decimal import Decimal
from typing import Dict, List
from models import TokenUsage, UsageSummary

class TokenUsageTracker:
    def __init__(self):
        self._usage_records: List[TokenUsage] = []
    
    def record_usage(self, repo_name: str, team: str, model: str, tokens: int, cost: Decimal) -> None:
        if not repo_name or not team or not model:
            raise ValueError("repo_name, team, and model cannot be empty")
        if tokens <= 0:
            raise ValueError("tokens must be positive")
        if cost < 0:
            raise ValueError("cost cannot be negative")
        
        usage = TokenUsage(
            repo_name=repo_name,
            team=team,
            model=model,
            tokens=tokens,
            cost=cost,
            timestamp=datetime.now()
        )
        self._usage_records.append(usage)
    
    def get_repo_summary(self, repo_name: str) -> UsageSummary:
        if not repo_name:
            raise ValueError("repo_name cannot be empty")
        
        repo_records = [r for r in self._usage_records if r.repo_name == repo_name]
        if not repo_records:
            raise ValueError(f"No usage found for repo: {repo_name}")
        
        team = repo_records[0].team
        total_tokens = sum(r.tokens for r in repo_records)
        total_cost = sum(r.cost for r in repo_records)
        
        model_breakdown = {}
        for record in repo_records:
            if record.model not in model_breakdown:
                model_breakdown[record.model] = (0, Decimal('0'))
            tokens, cost = model_breakdown[record.model]
            model_breakdown[record.model] = (tokens + record.tokens, cost + record.cost)
        
        return UsageSummary(repo_name, team, total_tokens, total_cost, model_breakdown)
    
    def get_team_summary(self, team: str) -> UsageSummary:
        if not team:
            raise ValueError("team cannot be empty")
        
        team_records = [r for r in self._usage_records if r.team == team]
        if not team_records:
            raise ValueError(f"No usage found for team: {team}")
        
        total_tokens = sum(r.tokens for r in team_records)
        total_cost = sum(r.cost for r in team_records)
        
        model_breakdown = {}
        for record in team_records:
            if record.model not in model_breakdown:
                model_breakdown[record.model] = (0, Decimal('0'))
            tokens, cost = model_breakdown[record.model]
            model_breakdown[record.model] = (tokens + record.tokens, cost + record.cost)
        
        return UsageSummary("", team, total_tokens, total_cost, model_breakdown)