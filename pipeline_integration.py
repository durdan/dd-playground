from slack_notifier import SlackNotifier, EventType, PipelineStep, ApprovalRequest
from config import SlackConfig

class PipelineNotificationService:
    def __init__(self):
        config = SlackConfig()
        self.notifier = SlackNotifier(config.bot_token, config.default_channel)
        self.config = config
    
    def notify_step_success(self, step_name: str, duration: float = None):
        """Notify successful step completion"""
        step = PipelineStep(
            name=step_name,
            status="success",
            duration=duration
        )
        
        self.notifier.send_notification(EventType.STEP_SUCCESS, step)
    
    def notify_step_failure(self, step_name: str, error_message: str, logs_url: str = None):
        """Notify step failure"""
        step = PipelineStep(
            name=step_name,
            status="failed",
            error_message=error_message,
            logs_url=logs_url
        )
        
        channel = self.config.get_channel_for_event("step_failure")
        self.notifier.send_notification(EventType.STEP_FAILURE, step, channel)
    
    def notify_pipeline_failure(self, pipeline_name: str, failed_steps: list):
        """Notify complete pipeline failure"""
        data = {
            "pipeline_name": pipeline_name,
            "failed_steps": failed_steps
        }
        
        channel = self.config.get_channel_for_event("pipeline_failure")
        self.notifier.send_notification(EventType.PIPELINE_FAILURE, data, channel)
    
    def request_approval(self, pipeline_name: str, environment: str, 
                        requester: str, approval_url: str, changes_summary: str = None):
        """Send approval request"""
        approval = ApprovalRequest(
            pipeline_name=pipeline_name,
            environment=environment,
            requester=requester,
            approval_url=approval_url,
            changes_summary=changes_summary
        )
        
        channel = self.config.get_channel_for_event("approval_request")
        self.notifier.send_notification(EventType.APPROVAL_REQUEST, approval, channel)

# Example usage
def example_pipeline():
    """Example of how to integrate notifications in a pipeline"""
    notification_service = PipelineNotificationService()
    
    try:
        # Step 1: Build
        print("Running build step...")
        # ... build logic ...
        notification_service.notify_step_success("Build", duration=45.2)
        
        # Step 2: Test
        print("Running tests...")
        # ... test logic ...
        notification_service.notify_step_success("Tests", duration=120.5)
        
        # Step 3: Request approval for production
        notification_service.request_approval(
            pipeline_name="web-app-deploy",
            environment="production",
            requester="john.doe",
            approval_url="https://ci.company.com/approvals/123",
            changes_summary="• Updated API endpoints\n• Fixed authentication bug\n• Added new feature X"
        )
        
    except Exception as e:
        notification_service.notify_step_failure(
            step_name="Build",
            error_message=str(e),
            logs_url="https://ci.company.com/logs/build/456"
        )
        
        notification_service.notify_pipeline_failure(
            pipeline_name="web-app-deploy",
            failed_steps=["Build"]
        )