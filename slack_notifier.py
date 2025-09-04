import json
import requests
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

class EventType(Enum):
    STEP_SUCCESS = "step_success"
    STEP_FAILURE = "step_failure"
    PIPELINE_FAILURE = "pipeline_failure"
    APPROVAL_REQUEST = "approval_request"

@dataclass
class PipelineStep:
    name: str
    status: str
    duration: Optional[float] = None
    error_message: Optional[str] = None
    logs_url: Optional[str] = None

@dataclass
class ApprovalRequest:
    pipeline_name: str
    environment: str
    requester: str
    approval_url: str
    changes_summary: Optional[str] = None

class SlackNotifier:
    def __init__(self, bot_token: str, default_channel: str):
        if not bot_token:
            raise ValueError("Slack bot token is required")
        if not default_channel:
            raise ValueError("Default channel is required")
            
        self.bot_token = bot_token
        self.default_channel = default_channel
        self.base_url = "https://slack.com/api"
        
    def send_notification(self, event_type: EventType, data: Any, 
                         channel: Optional[str] = None) -> bool:
        """Send notification to Slack channel"""
        try:
            channel = channel or self.default_channel
            message = self._format_message(event_type, data)
            
            payload = {
                "channel": channel,
                "blocks": message["blocks"]
            }
            
            if message.get("text"):
                payload["text"] = message["text"]
                
            return self._post_message(payload)
            
        except Exception as e:
            print(f"Failed to send Slack notification: {e}")
            return False
    
    def _format_message(self, event_type: EventType, data: Any) -> Dict:
        """Format message based on event type"""
        formatter = NotificationFormatter()
        
        if event_type == EventType.STEP_SUCCESS:
            return formatter.format_step_success(data)
        elif event_type == EventType.STEP_FAILURE:
            return formatter.format_step_failure(data)
        elif event_type == EventType.PIPELINE_FAILURE:
            return formatter.format_pipeline_failure(data)
        elif event_type == EventType.APPROVAL_REQUEST:
            return formatter.format_approval_request(data)
        else:
            raise ValueError(f"Unknown event type: {event_type}")
    
    def _post_message(self, payload: Dict) -> bool:
        """Post message to Slack API"""
        headers = {
            "Authorization": f"Bearer {self.bot_token}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            f"{self.base_url}/chat.postMessage",
            headers=headers,
            json=payload,
            timeout=10
        )
        
        if response.status_code != 200:
            raise Exception(f"Slack API error: {response.status_code}")
            
        result = response.json()
        if not result.get("ok"):
            raise Exception(f"Slack API error: {result.get('error')}")
            
        return True

class NotificationFormatter:
    def format_step_success(self, step: PipelineStep) -> Dict:
        """Format successful step notification"""
        duration_text = f" in {step.duration:.1f}s" if step.duration else ""
        
        return {
            "text": f"✅ Step '{step.name}' completed successfully{duration_text}",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"✅ *Step Completed Successfully*\n*Step:* {step.name}{duration_text}"
                    }
                }
            ]
        }
    
    def format_step_failure(self, step: PipelineStep) -> Dict:
        """Format failed step notification"""
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"❌ *Step Failed*\n*Step:* {step.name}\n*Status:* {step.status}"
                }
            }
        ]
        
        if step.error_message:
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Error:*\n