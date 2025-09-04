from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any
from enum import Enum

class Severity(Enum):
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

@dataclass
class RuleViolation:
    rule_name: str
    severity: Severity
    message: str
    details: Dict[str, Any] = None

class StopRule(ABC):
    def __init__(self, name: str, severity: Severity = Severity.ERROR):
        self.name = name
        self.severity = severity
    
    @abstractmethod
    def evaluate(self, change_data: Dict[str, Any]) -> List[RuleViolation]:
        """Evaluate the rule against change data."""
        pass

class FilesChangedRule(StopRule):
    def __init__(self, max_files: int, severity: Severity = Severity.ERROR):
        super().__init__("files_changed_limit", severity)
        self.max_files = max_files
    
    def evaluate(self, change_data: Dict[str, Any]) -> List[RuleViolation]:
        files_changed = change_data.get('files_changed', 0)
        if files_changed > self.max_files:
            return [RuleViolation(
                rule_name=self.name,
                severity=self.severity,
                message=f"Too many files changed: {files_changed} > {self.max_files}",
                details={'files_changed': files_changed, 'limit': self.max_files}
            )]
        return []

class LinesChangedRule(StopRule):
    def __init__(self, max_added: int, max_deleted: int, max_modified: int, 
                 severity: Severity = Severity.ERROR):
        super().__init__("lines_changed_limit", severity)
        self.max_added = max_added
        self.max_deleted = max_deleted
        self.max_modified = max_modified
    
    def evaluate(self, change_data: Dict[str, Any]) -> List[RuleViolation]:
        violations = []
        
        lines_added = change_data.get('lines_added', 0)
        lines_deleted = change_data.get('lines_deleted', 0)
        lines_modified = change_data.get('lines_modified', 0)
        
        if lines_added > self.max_added:
            violations.append(RuleViolation(
                rule_name=f"{self.name}_added",
                severity=self.severity,
                message=f"Too many lines added: {lines_added} > {self.max_added}",
                details={'lines_added': lines_added, 'limit': self.max_added}
            ))
        
        if lines_deleted > self.max_deleted:
            violations.append(RuleViolation(
                rule_name=f"{self.name}_deleted",
                severity=self.severity,
                message=f"Too many lines deleted: {lines_deleted} > {self.max_deleted}",
                details={'lines_deleted': lines_deleted, 'limit': self.max_deleted}
            ))
        
        if lines_modified > self.max_modified:
            violations.append(RuleViolation(
                rule_name=f"{self.name}_modified",
                severity=self.severity,
                message=f"Too many lines modified: {lines_modified} > {self.max_modified}",
                details={'lines_modified': lines_modified, 'limit': self.max_modified}
            ))
        
        return violations

class ComplexityRule(StopRule):
    def __init__(self, max_increase: int, severity: Severity = Severity.WARNING):
        super().__init__("complexity_increase", severity)
        self.max_increase = max_increase
    
    def evaluate(self, change_data: Dict[str, Any]) -> List[RuleViolation]:
        complexity_increase = change_data.get('complexity_increase', 0)
        if complexity_increase > self.max_increase:
            return [RuleViolation(
                rule_name=self.name,
                severity=self.severity,
                message=f"Complexity increased too much: {complexity_increase} > {self.max_increase}",
                details={'complexity_increase': complexity_increase, 'limit': self.max_increase}
            )]
        return []