from abc import ABC, abstractmethod
from typing import List, Set
import random
from models import Repository, RepositoryTier

class RolloutStrategy(ABC):
    @abstractmethod
    def select_repositories(self, repos: List[Repository], 
                          target_count: int, 
                          excluded: Set[str]) -> List[Repository]:
        pass

class PilotFirstStrategy(RolloutStrategy):
    def select_repositories(self, repos: List[Repository], 
                          target_count: int, 
                          excluded: Set[str]) -> List[Repository]:
        available = [r for r in repos if r.name not in excluded and r.is_healthy()]
        
        # Sort by tier priority: pilot -> canary -> production
        tier_priority = {
            RepositoryTier.PILOT: 0,
            RepositoryTier.CANARY: 1, 
            RepositoryTier.PRODUCTION: 2
        }
        
        available.sort(key=lambda r: (tier_priority[r.tier], r.name))
        return available[:target_count]

class RandomStrategy(RolloutStrategy):
    def select_repositories(self, repos: List[Repository], 
                          target_count: int, 
                          excluded: Set[str]) -> List[Repository]:
        available = [r for r in repos if r.name not in excluded and r.is_healthy()]
        return random.sample(available, min(target_count, len(available)))

class HealthBasedStrategy(RolloutStrategy):
    def select_repositories(self, repos: List[Repository], 
                          target_count: int, 
                          excluded: Set[str]) -> List[Repository]:
        available = [r for r in repos if r.name not in excluded and r.is_healthy()]
        # Select healthiest repositories first
        available.sort(key=lambda r: r.health_score, reverse=True)
        return available[:target_count]