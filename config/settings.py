import os
from typing import Optional
from pydantic import BaseSettings, Field
from dotenv import load_dotenv


class Settings(BaseSettings):
    """Application settings with environment-based configuration."""
    
    environment: str = Field(default="dev", env="ENVIRONMENT")
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    database_url: str = Field(default="sqlite:///./crew_app.db", env="DATABASE_URL")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


def load_config() -> Settings:
    """Load configuration based on environment."""
    env = os.getenv("ENVIRONMENT", "dev")
    
    # Load environment-specific .env file
    env_file = f".env.{env}"
    if os.path.exists(env_file):
        load_dotenv(env_file, override=True)
    else:
        # Fallback to default .env
        load_dotenv(".env")
    
    return Settings()


# Global config instance
config = load_config()