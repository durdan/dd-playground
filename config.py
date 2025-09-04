import os
from typing import Optional

class SlackConfig:
    def __init__(self):
        self.bot_token = self._get_required_env("SLACK_BOT_TOKEN")
        self.default_channel = self._get_required_env("SLACK_DEFAULT_CHANNEL")
        self.failure_channel = os.getenv("SLACK_FAILURE_CHANNEL")
        self.approval_channel = os.getenv("SLACK_APPROVAL_CHANNEL")
    
    def _get_required_env(self, key: str) -> str:
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Required environment variable {key} is not set")
        return value
    
    def get_channel_for_event(self, event_type: str) -> Optional[str]:
        """Get specific channel for event type, fallback to default"""
        if event_type in ["step_failure", "pipeline_failure"] and self.failure_channel:
            return self.failure_channel
        elif event_type == "approval_request" and self.approval_channel:
            return self.approval_channel
        return self.default_channel