from typing import Dict, List
from models import QualityGate, QualityGateType

class QualityGateFactory:
    """Factory for creating standard quality gates"""
    
    @staticmethod
    def create_code_review_gate() -> QualityGate:
        return QualityGate(
            name="Code Review",
            gate_type=QualityGateType.CODE_REVIEW,
            crew_agent="code_reviewer",
            criteria={
                "min_score": 7.0,
                "check_patterns": True,
                "check_complexity": True,
                "check_maintainability": True
            }
        )
    
    @staticmethod
    def create_testing_gate() -> QualityGate:
        return QualityGate(
            name="Testing Validation",
            gate_type=QualityGateType.TESTING,
            crew_agent="test_validator",
            criteria={
                "min_coverage": 80.0,
                "require_unit_tests": True,
                "require_integration_tests": False
            }
        )
    
    @staticmethod
    def create_documentation_gate() -> QualityGate:
        return QualityGate(
            name="Documentation Check",
            gate_type=QualityGateType.DOCUMENTATION,
            crew_agent="doc_reviewer",
            required=False,
            criteria={
                "check_docstrings": True,
                "check_readme": True,
                "min_completeness": 70.0
            }
        )
    
    @staticmethod
    def create_security_gate() -> QualityGate:
        return QualityGate(
            name="Security Scan",
            gate_type=QualityGateType.SECURITY,
            crew_agent="security_scanner",
            criteria={
                "scan_vulnerabilities": True,
                "check_dependencies": True,
                "max_severity": "medium"
            }
        )

def get_default_gates() -> List[QualityGate]:
    """Get standard set of quality gates"""
    factory = QualityGateFactory()
    return [
        factory.create_code_review_gate(),
        factory.create_testing_gate(),
        factory.create_documentation_gate(),
        factory.create_security_gate()
    ]