from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from enum import Enum

class Severity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

@dataclass
class ValidationIssue:
    severity: Severity
    category: str
    message: str
    location: Optional[str] = None

@dataclass
class ValidationResult:
    issues: List[ValidationIssue]
    score: float  # 0-100
    
    def is_valid(self) -> bool:
        return not any(issue.severity == Severity.ERROR for issue in self.issues)

class SpecValidator:
    def __init__(self):
        self.completeness_checker = CompletenessChecker()
        self.consistency_checker = ConsistencyChecker()
        self.quality_checker = QualityChecker()
        self.code_reviewer = CodeReviewerAgent()
    
    def validate(self, specification: Dict[str, Any]) -> ValidationResult:
        """Validate specification completeness, consistency, and quality."""
        all_issues = []
        
        # Run all validation checks
        all_issues.extend(self.completeness_checker.check(specification))
        all_issues.extend(self.consistency_checker.check(specification))
        all_issues.extend(self.quality_checker.check(specification))
        
        # Calculate score based on issues
        score = self._calculate_score(all_issues)
        
        return ValidationResult(issues=all_issues, score=score)
    
    def get_rule_improvements(self) -> List[str]:
        """Get suggestions from code reviewer for improving validation rules."""
        current_rules = self._extract_current_rules()
        return self.code_reviewer.suggest_improvements(current_rules)
    
    def _calculate_score(self, issues: List[ValidationIssue]) -> float:
        """Calculate quality score from 0-100 based on issues."""
        if not issues:
            return 100.0
        
        error_penalty = sum(10 for issue in issues if issue.severity == Severity.ERROR)
        warning_penalty = sum(3 for issue in issues if issue.severity == Severity.WARNING)
        info_penalty = sum(1 for issue in issues if issue.severity == Severity.INFO)
        
        total_penalty = error_penalty + warning_penalty + info_penalty
        return max(0.0, 100.0 - total_penalty)
    
    def _extract_current_rules(self) -> Dict[str, List[str]]:
        """Extract current validation rules for review."""
        return {
            "completeness": self.completeness_checker.get_rules(),
            "consistency": self.consistency_checker.get_rules(),
            "quality": self.quality_checker.get_rules()
        }

class CompletenessChecker:
    def __init__(self):
        self.required_sections = ["title", "requirements", "architecture"]
        self.required_fields = {
            "requirements": ["functional", "non_functional"],
            "architecture": ["components", "data_flow"]
        }
    
    def check(self, spec: Dict[str, Any]) -> List[ValidationIssue]:
        """Check specification completeness."""
        issues = []
        
        # Check required sections
        for section in self.required_sections:
            if section not in spec:
                issues.append(ValidationIssue(
                    severity=Severity.ERROR,
                    category="completeness",
                    message=f"Missing required section: {section}",
                    location=f"root.{section}"
                ))
        
        # Check required fields within sections
        for section, fields in self.required_fields.items():
            if section in spec:
                for field in fields:
                    if field not in spec[section]:
                        issues.append(ValidationIssue(
                            severity=Severity.WARNING,
                            category="completeness",
                            message=f"Missing recommended field: {field} in {section}",
                            location=f"{section}.{field}"
                        ))
        
        # Check for empty sections
        for key, value in spec.items():
            if not value or (isinstance(value, (list, dict)) and len(value) == 0):
                issues.append(ValidationIssue(
                    severity=Severity.WARNING,
                    category="completeness",
                    message=f"Empty section: {key}",
                    location=key
                ))
        
        return issues
    
    def get_rules(self) -> List[str]:
        return [
            "Required sections must be present",
            "Recommended fields should be included",
            "Sections should not be empty"
        ]

class ConsistencyChecker:
    def check(self, spec: Dict[str, Any]) -> List[ValidationIssue]:
        """Check specification consistency."""
        issues = []
        
        # Check naming consistency
        issues.extend(self._check_naming_consistency(spec))
        
        # Check reference consistency
        issues.extend(self._check_reference_consistency(spec))
        
        # Check data type consistency
        issues.extend(self._check_data_type_consistency(spec))
        
        return issues
    
    def _check_naming_consistency(self, spec: Dict[str, Any]) -> List[ValidationIssue]:
        """Check for consistent naming conventions."""
        issues = []
        
        # Collect all identifiers
        identifiers = set()
        if "data_models" in spec:
            for model in spec["data_models"]:
                if isinstance(model, dict) and "name" in model:
                    identifiers.add(model["name"])
        
        if "api_endpoints" in spec:
            for endpoint in spec["api_endpoints"]:
                if isinstance(endpoint, dict) and "path" in endpoint:
                    # Extract resource names from paths
                    path_parts = endpoint["path"].strip("/").split("/")
                    identifiers.update(part for part in path_parts if part and not part.startswith("{"))
        
        # Check for inconsistent casing
        lowercase_map = {}
        for identifier in identifiers:
            lower = identifier.lower()
            if lower in lowercase_map and lowercase_map[lower] != identifier:
                issues.append(ValidationIssue(
                    severity=Severity.WARNING,
                    category="consistency",
                    message=f"Inconsistent naming: '{identifier}' vs '{lowercase_map[lower]}'",
                    location="naming"
                ))
            lowercase_map[lower] = identifier
        
        return issues
    
    def _check_reference_consistency(self, spec: Dict[str, Any]) -> List[ValidationIssue]:
        """Check that all references point to existing entities."""
        issues = []
        
        # Collect defined models
        defined_models = set()
        if "data_models" in spec:
            for model in spec["data_models"]:
                if isinstance(model, dict) and "name" in model:
                    defined_models.add(model["name"])
        
        # Check references in API endpoints
        if "api_endpoints" in spec:
            for endpoint in spec["api_endpoints"]:
                if isinstance(endpoint, dict) and "response_model" in endpoint:
                    model_name = endpoint["response_model"]
                    if model_name not in defined_models:
                        issues.append(ValidationIssue(
                            severity=Severity.ERROR,
                            category="consistency",
                            message=f"Reference to undefined model: {model_name}",
                            location=f"api_endpoints.response_model"
                        ))
        
        return issues
    
    def _check_data_type_consistency(self, spec: Dict[str, Any]) -> List[ValidationIssue]:
        """Check for consistent data type usage."""
        issues = []
        
        if "data_models" in spec:
            for model in spec["data_models"]:
                if isinstance(model, dict) and "fields" in model:
                    for field_name, field_info in model["fields"].items():
                        if isinstance(field_info, dict) and "type" in field_info:
                            field_type = field_info["type"]
                            # Check for common type inconsistencies
                            if field_type.lower() in ["int", "integer"] and field_type != "integer":
                                issues.append(ValidationIssue(
                                    severity=Severity.INFO,
                                    category="consistency",
                                    message=f"Consider using 'integer' instead of '{field_type}' for consistency",
                                    location=f"data_models.{model.get('name', 'unknown')}.{field_name}"
                                ))
        
        return issues
    
    def get_rules(self) -> List[str]:
        return [
            "Naming conventions should be consistent",
            "All references must point to existing entities",
            "Data types should be consistently named"
        ]

class QualityChecker:
    def check(self, spec: Dict[str, Any]) -> List[ValidationIssue]:
        """Check specification quality."""
        issues = []
        
        # Check description quality
        issues.extend(self._check_description_quality(spec))
        
        # Check requirement specificity
        issues.extend(self._check_requirement_specificity(spec))
        
        # Check API design quality
        issues.extend(self._check_api_design_quality(spec))
        
        return issues
    
    def _check_description_quality(self, spec: Dict[str, Any]) -> List[ValidationIssue]:
        """Check quality of descriptions and documentation."""
        issues = []
        
        # Check title length and clarity
        if "title" in spec:
            title = spec["title"]
            if len(title) < 5:
                issues.append(ValidationIssue(
                    severity=Severity.WARNING,
                    category="quality",
                    message="Title is too short, consider adding more descriptive information",
                    location="title"
                ))
            elif len(title) > 100:
                issues.append(ValidationIssue(
                    severity=Severity.INFO,
                    category="quality",
                    message="Title is very long, consider making it more concise",
                    location="title"
                ))
        
        # Check for vague language
        vague_terms = ["some", "various", "multiple", "several", "many"]
        for section_name, section_content in spec.items():
            if isinstance(section_content, str):
                for term in vague_terms:
                    if term in section_content.lower():
                        issues.append(ValidationIssue(
                            severity=Severity.INFO,
                            category="quality",
                            message=f"Consider being more specific than '{term}' in {section_name}",
                            location=section_name
                        ))
        
        return issues
    
    def _check_requirement_specificity(self, spec: Dict[str, Any]) -> List[ValidationIssue]:
        """Check that requirements are specific and measurable."""
        issues = []
        
        if "requirements" in spec:
            requirements = spec["requirements"]
            if isinstance(requirements, dict):
                # Check functional requirements
                if "functional" in requirements:
                    for req in requirements["functional"]:
                        if isinstance(req, str) and len(req.split()) < 5:
                            issues.append(ValidationIssue(
                                severity=Severity.WARNING,
                                category="quality",
                                message="Functional requirement seems too brief, add more detail",
                                location="requirements.functional"
                            ))
                
                # Check non-functional requirements for measurable criteria
                if "non_functional" in requirements:
                    measurable_keywords = ["response time", "throughput", "availability", "users", "requests"]
                    for req in requirements["non_functional"]:
                        if isinstance(req, str):
                            has_measurable = any(keyword in req.lower() for keyword in measurable_keywords)
                            if not has_measurable:
                                issues.append(ValidationIssue(
                                    severity=Severity.INFO,
                                    category="quality",
                                    message="Consider adding measurable criteria to non-functional requirement",
                                    location="requirements.non_functional"
                                ))
        
        return issues
    
    def _check_api_design_quality(self, spec: Dict[str, Any]) -> List[ValidationIssue]:
        """Check API design best practices."""
        issues = []
        
        if "api_endpoints" in spec:
            for i, endpoint in enumerate(spec["api_endpoints"]):
                if isinstance(endpoint, dict):
                    # Check HTTP method appropriateness
                    if "method" in endpoint and "path" in endpoint:
                        method = endpoint["method"].upper()
                        path = endpoint["path"]
                        
                        if method == "GET" and any(word in path.lower() for word in ["create", "update", "delete"]):
                            issues.append(ValidationIssue(
                                severity=Severity.WARNING,
                                category="quality",
                                message=f"GET method with action-oriented path: {path}",
                                location=f"api_endpoints[{i}]"
                            ))
                    
                    # Check for missing status codes
                    if "responses" not in endpoint:
                        issues.append(ValidationIssue(
                            severity=Severity.WARNING,
                            category="quality",
                            message="API endpoint missing response specifications",
                            location=f"api_endpoints[{i}]"
                        ))
        
        return issues
    
    def get_rules(self) -> List[str]:
        return [
            "Descriptions should be clear and appropriately detailed",
            "Requirements should be specific and measurable",
            "API design should follow REST best practices"
        ]

class CodeReviewerAgent:
    def suggest_improvements(self, current_rules: Dict[str, List[str]]) -> List[str]:
        """Analyze current validation rules and suggest improvements."""
        suggestions = []
        
        # Analyze completeness rules
        completeness_rules = current_rules.get("completeness", [])
        if len(completeness_rules) < 5:
            suggestions.append("Consider adding validation for security requirements section")
            suggestions.append("Add check for performance benchmarks in specifications")
        
        # Analyze consistency rules
        consistency_rules = current_rules.get("consistency", [])
        suggestions.extend([
            "Add validation for consistent error response formats across API endpoints",
            "Check for consistent authentication patterns across endpoints",
            "Validate that database schema matches data model definitions"
        ])
        
        # Analyze quality rules
        quality_rules = current_rules.get("quality", [])
        suggestions.extend([
            "Add check for accessibility requirements compliance",
            "Validate that API versioning strategy is documented",
            "Check for proper error handling specifications",
            "Add validation for rate limiting and throttling specifications"
        ])
        
        # General improvements
        suggestions.extend([
            "Consider adding severity levels for different types of missing sections",
            "Implement configurable rule sets for different project types",
            "Add validation for compliance with industry standards (OpenAPI, etc.)",
            "Include checks for internationalization and localization requirements"
        ])
        
        return suggestions