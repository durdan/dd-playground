from typing import Dict, List, Optional
from models.approval import ApprovalRequest, ApprovalStatus

class ApprovalRepository:
    def __init__(self):
        self._storage: Dict[str, ApprovalRequest] = {}

    def save(self, request: ApprovalRequest) -> None:
        """Save approval request"""
        self._storage[request.id] = request

    def get_by_id(self, request_id: str) -> Optional[ApprovalRequest]:
        """Get approval request by ID"""
        return self._storage.get(request_id)

    def get_by_status(self, status: ApprovalStatus) -> List[ApprovalRequest]:
        """Get all requests with given status"""
        return [req for req in self._storage.values() if req.status == status]

    def get_all(self) -> List[ApprovalRequest]:
        """Get all approval requests"""
        return list(self._storage.values())