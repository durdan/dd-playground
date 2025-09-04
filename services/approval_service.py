import uuid
from datetime import datetime
from typing import List, Optional
from models.approval import ApprovalRequest, ApprovalStatus, OperationType
from repositories.approval_repository import ApprovalRepository
from services.notification_service import NotificationService

class ApprovalService:
    def __init__(self, repository: ApprovalRepository, notification_service: NotificationService):
        self.repository = repository
        self.notification_service = notification_service

    def create_approval_request(
        self, 
        operation_type: OperationType, 
        target: str, 
        requester: str, 
        description: str,
        metadata: Optional[dict] = None
    ) -> ApprovalRequest:
        """Create a new approval request"""
        if not target.strip():
            raise ValueError("Target cannot be empty")
        if not requester.strip():
            raise ValueError("Requester cannot be empty")
        if not description.strip():
            raise ValueError("Description cannot be empty")

        request = ApprovalRequest(
            id=str(uuid.uuid4()),
            operation_type=operation_type,
            target=target,
            requester=requester,
            description=description,
            status=ApprovalStatus.PENDING,
            created_at=datetime.now(),
            metadata=metadata or {}
        )
        
        self.repository.save(request)
        self.notification_service.notify_approval_needed(request)
        return request

    def review_request(
        self, 
        request_id: str, 
        reviewer: str, 
        approved: bool, 
        comment: Optional[str] = None
    ) -> ApprovalRequest:
        """Review an approval request"""
        if not reviewer.strip():
            raise ValueError("Reviewer cannot be empty")

        request = self.repository.get_by_id(request_id)
        if not request:
            raise ValueError(f"Approval request {request_id} not found")

        new_status = ApprovalStatus.APPROVED if approved else ApprovalStatus.REJECTED
        
        if not request.can_transition_to(new_status):
            raise ValueError(f"Cannot transition from {request.status.value} to {new_status.value}")

        request.status = new_status
        request.reviewer = reviewer
        request.review_comment = comment
        request.reviewed_at = datetime.now()

        self.repository.save(request)
        self.notification_service.notify_approval_decision(request)
        return request

    def mark_completed(self, request_id: str) -> ApprovalRequest:
        """Mark an approved request as completed"""
        request = self.repository.get_by_id(request_id)
        if not request:
            raise ValueError(f"Approval request {request_id} not found")

        if not request.can_transition_to(ApprovalStatus.COMPLETED):
            raise ValueError(f"Cannot mark request as completed from status {request.status.value}")

        request.status = ApprovalStatus.COMPLETED
        self.repository.save(request)
        return request

    def get_pending_requests(self) -> List[ApprovalRequest]:
        """Get all pending approval requests"""
        return self.repository.get_by_status(ApprovalStatus.PENDING)

    def get_request(self, request_id: str) -> Optional[ApprovalRequest]:
        """Get approval request by ID"""
        return self.repository.get_by_id(request_id)