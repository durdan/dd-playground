import os
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class GitHubConfig:
    token: str
    base_url: str = "https://api.github.com"
    
    @classmethod
    def from_env(cls) -> 'GitHubConfig':
        token = os.getenv('GITHUB_TOKEN')
        if not token:
            raise ValueError("GITHUB_TOKEN environment variable is required")
        return cls(token=token)

@dataclass
class QualityGateConfig:
    min_code_quality_score: float = 7.0
    min_security_score: float = 8.0
    min_performance_score: float = 6.0
    min_documentation_score: float = 5.0
    min_overall_score: float = 7.0
    
    @classmethod
    def from_dict(cls, config: Dict[str, Any]) -> 'QualityGateConfig':
        return cls(**{k: v for k, v in config.items() if hasattr(cls, k)})

@dataclass
class CrewConfig:
    model: str = "gpt-4"
    temperature: float = 0.1
    max_tokens: int = 2000