from typing import Optional
from models.approval import OperationType, ApprovalStatus
from services.approval_service import ApprovalService

class MergeDeployService:
    def __init__(self, approval_service: ApprovalService):
        self.approval_service = approval_service

    def request_merge(self, branch: str, requester: str, description: str) -> str:
        """Request approval for merge operation"""
        request = self.approval_service.create_approval_request(
            operation_type=OperationType.MERGE,
            target=branch,
            requester=requester,
            description=description
        )
        return request.id

    def execute_merge(self, approval_id: str) -> bool:
        """Execute merge if approved"""
        request = self.approval_service.get_request(approval_id)
        if not request:
            raise ValueError(f"Approval request {approval_id} not found")

        if request.status != ApprovalStatus.APPROVED:
            raise ValueError(f"Cannot merge: approval status is {request.status.value}")

        # Simulate merge operation
        print(f"Executing merge for {request.target}")
        
        # Mark as completed
        self.approval_service.mark_completed(approval_id)
        return True

    def request_deploy(self, environment: str, requester: str, description: str, metadata: Optional[dict] = None) -> str:
        """Request approval for deploy operation"""
        request = self.approval_service.create_approval_request(
            operation_type=OperationType.DEPLOY,
            target=environment,
            requester=requester,
            description=description,
            metadata=metadata
        )
        return request.id

    def execute_deploy(self, approval_id: str) -> bool:
        """Execute deploy if approved"""
        request = self.approval_service.get_request(approval_id)
        if not request:
            raise ValueError(f"Approval request {approval_id} not found")

        if request.status != ApprovalStatus.APPROVED:
            raise ValueError(f"Cannot deploy: approval status is {request.status.value}")

        # Simulate deploy operation
        print(f"Executing deploy to {request.target}")
        
        # Mark as completed
        self.approval_service.mark_completed(approval_id)
        return True