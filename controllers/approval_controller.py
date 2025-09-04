from typing import Dict, Any, List
from services.approval_service import ApprovalService
from services.merge_deploy_service import MergeDeployService
from models.approval import OperationType

class ApprovalController:
    def __init__(self, approval_service: ApprovalService, merge_deploy_service: MergeDeployService):
        self.approval_service = approval_service
        self.merge_deploy_service = merge_deploy_service

    def request_merge_approval(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """API endpoint for requesting merge approval"""
        try:
            approval_id = self.merge_deploy_service.request_merge(
                branch=data['branch'],
                requester=data['requester'],
                description=data['description']
            )
            return {"success": True, "approval_id": approval_id}
        except (KeyError, ValueError) as e:
            return {"success": False, "error": str(e)}

    def request_deploy_approval(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """API endpoint for requesting deploy approval"""
        try:
            approval_id = self.merge_deploy_service.request_deploy(
                environment=data['environment'],
                requester=data['requester'],
                description=data['description'],
                metadata=data.get('metadata')
            )
            return {"success": True, "approval_id": approval_id}
        except (KeyError, ValueError) as e:
            return {"success": False, "error": str(e)}

    def review_approval(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """API endpoint for reviewing approval"""
        try:
            request = self.approval_service.review_request(
                request_id=data['approval_id'],
                reviewer=data['reviewer'],
                approved=data['approved'],
                comment=data.get('comment')
            )
            return {"success": True, "status": request.status.value}
        except (KeyError, ValueError) as e:
            return {"success": False, "error": str(e)}

    def execute_operation(self, approval_id: str) -> Dict[str, Any]:
        """API endpoint for executing approved operation"""
        try:
            request = self.approval_service.get_request(approval_id)
            if not request:
                return {"success": False, "error": "Approval request not found"}

            if request.operation_type == OperationType.MERGE:
                self.merge_deploy_service.execute_merge(approval_id)
            else:
                self.merge_deploy_service.execute_deploy(approval_id)
            
            return {"success": True, "message": f"{request.operation_type.value} completed"}
        except ValueError as e:
            return {"success": False, "error": str(e)}

    def get_pending_approvals(self) -> List[Dict[str, Any]]:
        """API endpoint for getting pending approvals"""
        requests = self.approval_service.get_pending_requests()
        return [
            {
                "id": req.id,
                "operation_type": req.operation_type.value,
                "target": req.target,
                "requester": req.requester,
                "description": req.description,
                "created_at": req.created_at.isoformat()
            }
            for req in requests
        ]