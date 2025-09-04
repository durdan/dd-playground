from models.approval import ApprovalRequest

class NotificationService:
    def notify_approval_needed(self, request: ApprovalRequest) -> None:
        """Notify that approval is needed"""
        print(f"📧 Approval needed: {request.operation_type.value} for {request.target}")
        print(f"   Requested by: {request.requester}")
        print(f"   Description: {request.description}")
        print(f"   Request ID: {request.id}")

    def notify_approval_decision(self, request: ApprovalRequest) -> None:
        """Notify about approval decision"""
        status = "✅ APPROVED" if request.status.value == "approved" else "❌ REJECTED"
        print(f"📧 {status}: {request.operation_type.value} for {request.target}")
        print(f"   Reviewed by: {request.reviewer}")
        if request.review_comment:
            print(f"   Comment: {request.review_comment}")