import os
from typing import Optional
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application configuration settings."""
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # CrewAI Configuration
    openai_api_key: Optional[str] = None
    crew_max_execution_time: int = 3600  # 1 hour
    crew_max_iterations: int = 10
    
    # CI/CD Configuration
    environment: str = "development"
    log_level: str = "INFO"
    
    # Storage Configuration
    results_storage_path: str = "/app/results"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()