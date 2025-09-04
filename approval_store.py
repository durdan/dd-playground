from typing import Dict, List, Optional
from datetime import datetime
from models import HumanApprovalRequest, ApprovalStatus

class ApprovalStore:
    def __init__(self):
        self.requests: Dict[str, HumanApprovalRequest] = {}
    
    def save_request(self, request: HumanApprovalRequest):
        """Save approval request"""
        if not request.id:
            raise ValueError("Request ID is required")
        self.requests[request.id] = request
    
    def get_request(self, request_id: str) -> Optional[HumanApprovalRequest]:
        """Get approval request by ID"""
        return self.requests.get(request_id)
    
    def get_pending_requests(self) -> List[HumanApprovalRequest]:
        """Get all pending approval requests"""
        now = datetime.now()
        pending = []
        
        for request in self.requests.values():
            if request.status == ApprovalStatus.PENDING:
                if request.expires_at <= now:
                    request.status = ApprovalStatus.EXPIRED
                else:
                    pending.append(request)
        
        return pending
    
    def update_request_status(self, request_id: str, status: ApprovalStatus, 
                            approved_by: Optional[str] = None, 
                            rejection_reason: Optional[str] = None):
        """Update request status"""
        request = self.get_request(request_id)
        if not request:
            raise ValueError(f"Request {request_id} not found")
        
        if request.status != ApprovalStatus.PENDING:
            raise ValueError(f"Cannot update request with status {request.status.value}")
        
        request.status = status
        request.approved_by = approved_by
        request.rejection_reason = rejection_reason