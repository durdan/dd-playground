from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from decimal import Decimal

@dataclass
class Repo:
    name: str
    team: str

@dataclass
class Team:
    name: str
    budget_limit: Decimal
    alert_threshold: Decimal  # percentage (0.8 = 80%)

@dataclass
class TokenUsage:
    repo_name: str
    team: str
    model: str
    tokens: int
    cost: Decimal
    timestamp: datetime

@dataclass
class UsageSummary:
    repo_name: str
    team: str
    total_tokens: int
    total_cost: Decimal
    model_breakdown: dict  # model -> (tokens, cost)