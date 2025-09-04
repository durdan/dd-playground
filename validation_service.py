from typing import List
from models import Repository, Phase, RepositoryTier

class ValidationService:
    @staticmethod
    def validate_phases(phases: List[Phase]) -> List[str]:
        errors = []
        
        if not phases:
            errors.append("At least one phase is required")
            return errors
        
        total_percentage = sum(p.target_percentage for p in phases)
        if total_percentage > 100:
            errors.append(f"Total percentage ({total_percentage}%) exceeds 100%")
        
        for i, phase in enumerate(phases):
            if phase.wait_time_hours < 0:
                errors.append(f"Phase {i}: wait_time_hours cannot be negative")
            
            if phase.max_failures < 0:
                errors.append(f"Phase {i}: max_failures cannot be negative")
        
        return errors
    
    @staticmethod
    def validate_repositories(repos: List[Repository]) -> List[str]:
        errors = []
        
        if not repos:
            errors.append("At least one repository is required")
            return errors
        
        repo_names = [r.name for r in repos]
        if len(repo_names) != len(set(repo_names)):
            errors.append("Repository names must be unique")
        
        pilot_repos = [r for r in repos if r.tier == RepositoryTier.PILOT]
        if not pilot_repos:
            errors.append("At least one pilot repository is required")
        
        return errors