from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from models import (
    HumanApprovalRequest, OperationResult, ApprovalStatus, RiskLevel
)
from safety_validator import SafetyValidator
from approval_store import ApprovalStore

class HumanController:
    def __init__(self):
        self.validator = SafetyValidator()
        self.store = ApprovalStore()
    
    def request_operation(self, operation_type: str, description: str, 
                         operation_data: Dict[str, Any]) -> OperationResult:
        """Request to perform an operation with safety checks"""
        if not operation_type or not description:
            return OperationResult(
                success=False,
                operation_id="",
                message="Operation type and description are required"
            )
        
        # Validate against safety rules
        violations, risk_level = self.validator.validate_operation(operation_data)
        
        # Check if human approval is required
        requires_approval = self.validator.requires_human_approval(risk_level, violations)
        
        if not requires_approval and not violations:
            # Safe to proceed automatically
            return OperationResult(
                success=True,
                operation_id=f"auto_{datetime.now().timestamp()}",
                message="Operation approved automatically",
                requires_approval=False
            )
        
        # Create approval request
        approval_request = HumanApprovalRequest(
            operation_type=operation_type,
            description=description,
            risk_level=risk_level,
            context={
                "operation_data": operation_data,
                "violations": violations
            }
        )
        
        # Set expiration based on risk level
        if risk_level == RiskLevel.CRITICAL:
            approval_request.expires_at = datetime.now() + timedelta(hours=1)
        elif risk_level == RiskLevel.HIGH:
            approval_request.expires_at = datetime.now() + timedelta(hours=4)
        
        self.store.save_request(approval_request)
        
        return OperationResult(
            success=False,
            operation_id="",
            message=f"Human approval required. Risk level: {risk_level.value}",
            requires_approval=True,
            approval_request_id=approval_request.id,
            safety_violations=violations
        )
    
    def approve_request(self, request_id: str, approver: str, 
                       override_safety: bool = False) -> OperationResult:
        """Approve a pending request"""
        if not request_id or not approver:
            return OperationResult(
                success=False,
                operation_id="",
                message="Request ID and approver are required"
            )
        
        request = self.store.get_request(request_id)
        if not request:
            return OperationResult(
                success=False,
                operation_id="",
                message=f"Request {request_id} not found"
            )
        
        if request.status != ApprovalStatus.PENDING:
            return OperationResult(
                success=False,
                operation_id="",
                message=f"Request is {request.status.value}, cannot approve"
            )
        
        # Check if request has expired
        if request.expires_at <= datetime.now():
            self.store.update_request_status(request_id, ApprovalStatus.EXPIRED)
            return OperationResult(
                success=False,
                operation_id="",
                message="Request has expired"
            )
        
        # For critical operations, require explicit safety override
        violations = request.context.get("violations", [])
        if violations and request.risk_level == RiskLevel.CRITICAL and not override_safety:
            return OperationResult(
                success=False,
                operation_id="",
                message="Critical safety violations require explicit override"
            )
        
        self.store.update_request_status(request_id, ApprovalStatus.APPROVED, approver)
        
        return OperationResult(
            success=True,
            operation_id=f"approved_{request_id}",
            message=f"Operation approved by {approver}"
        )
    
    def reject_request(self, request_id: str, approver: str, reason: str) -> OperationResult:
        """Reject a pending request"""
        if not request_id or not approver or not reason:
            return OperationResult(
                success=False,
                operation_id="",
                message="Request ID, approver, and reason are required"
            )
        
        request = self.store.get_request(request_id)
        if not request:
            return OperationResult(
                success=False,
                operation_id="",
                message=f"Request {request_id} not found"
            )
        
        if request.status != ApprovalStatus.PENDING:
            return OperationResult(
                success=False,
                operation_id="",
                message=f"Request is {request.status.value}, cannot reject"
            )
        
        self.store.update_request_status(request_id, ApprovalStatus.REJECTED, approver, reason)
        
        return OperationResult(
            success=True,
            operation_id="",
            message=f"Operation rejected by {approver}: {reason}"
        )
    
    def get_pending_approvals(self):
        """Get all pending approval requests"""
        return self.store.get_pending_requests()
    
    def add_safety_rule(self, rule):
        """Add a custom safety rule"""
        self.validator.add_rule(rule)