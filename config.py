import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class Config:
    github_token: str
    github_webhook_secret: str
    openai_api_key: str
    port: int = 5000
    
    @classmethod
    def from_env(cls) -> 'Config':
        github_token = os.getenv('GITHUB_TOKEN')
        webhook_secret = os.getenv('GITHUB_WEBHOOK_SECRET')
        openai_key = os.getenv('OPENAI_API_KEY')
        
        if not all([github_token, webhook_secret, openai_key]):
            raise ValueError("Missing required environment variables: GITHUB_TOKEN, GITHUB_WEBHOOK_SECRET, OPENAI_API_KEY")
        
        return cls(
            github_token=github_token,
            github_webhook_secret=webhook_secret,
            openai_api_key=openai_key,
            port=int(os.getenv('PORT', '5000'))
        )