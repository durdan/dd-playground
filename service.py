from crew import CodeReviewCrew
from models import CodeReviewRequest, ReviewResult, Issue, ReviewType
from typing import List
import re

class CodeReviewService:
    def __init__(self):
        self.crew_manager = CodeReviewCrew()
    
    def review_code(self, request: CodeReviewRequest) -> ReviewResult:
        if not request.code_content.strip():
            raise ValueError("Code content cannot be empty")
        
        if not request.file_path:
            raise ValueError("File path is required")
        
        crew = self.crew_manager.create_crew(request)
        result = crew.kickoff()
        
        return self._parse_crew_result(result, request.file_path)
    
    def _parse_crew_result(self, crew_result: str, file_path: str) -> ReviewResult:
        """Parse the crew result and extract structured issues"""
        issues = self._extract_issues(crew_result)
        overall_score = self._calculate_score(issues)
        summary = self._generate_summary(issues)
        
        return ReviewResult(
            file_path=file_path,
            issues=issues,
            overall_score=overall_score,
            summary=summary
        )
    
    def _extract_issues(self, result: str) -> List[Issue]:
        """Extract issues from crew result text"""
        issues = []
        
        # Simple pattern matching - in production, use more sophisticated parsing
        security_pattern = r"SECURITY.*?(?=QUALITY|PERFORMANCE|$)"
        quality_pattern = r"QUALITY.*?(?=SECURITY|PERFORMANCE|$)"
        performance_pattern = r"PERFORMANCE.*?(?=SECURITY|QUALITY|$)"
        
        patterns = [
            (security_pattern, ReviewType.SECURITY),
            (quality_pattern, ReviewType.QUALITY),
            (performance_pattern, ReviewType.PERFORMANCE)
        ]
        
        for pattern, review_type in patterns:
            matches = re.findall(pattern, result, re.DOTALL | re.IGNORECASE)
            for match in matches:
                parsed_issues = self._parse_section_issues(match, review_type)
                issues.extend(parsed_issues)
        
        return issues
    
    def _parse_section_issues(self, section: str, review_type: ReviewType) -> List[Issue]:
        """Parse issues from a specific section"""
        issues = []
        
        # Extract line numbers, severity, and descriptions
        # This is a simplified parser - enhance based on actual crew output format
        lines = section.split('\n')
        current_issue = {}
        
        for line in lines:
            line = line.strip()
            if 'line' in line.lower() and any(char.isdigit() for char in line):
                line_num = re.search(r'\d+', line)
                current_issue['line_number'] = int(line_num.group()) if line_num else None
            elif any(severity in line.lower() for severity in ['critical', 'high', 'medium', 'low']):
                for severity in ['critical', 'high', 'medium', 'low']:
                    if severity in line.lower():
                        current_issue['severity'] = severity
                        break
            elif line and 'suggestion' not in line.lower():
                current_issue['description'] = line
            elif 'suggestion' in line.lower():
                current_issue['suggestion'] = line
                
                if all(key in current_issue for key in ['severity', 'description', 'suggestion']):
                    issues.append(Issue(
                        type=review_type,
                        severity=current_issue['severity'],
                        line_number=current_issue.get('line_number'),
                        description=current_issue['description'],
                        suggestion=current_issue['suggestion']
                    ))
                    current_issue = {}
        
        return issues
    
    def _calculate_score(self, issues: List[Issue]) -> int:
        """Calculate overall score based on issues"""
        if not issues:
            return 10
        
        severity_weights = {'critical': 4, 'high': 3, 'medium': 2, 'low': 1}
        total_weight = sum(severity_weights.get(issue.severity, 1) for issue in issues)
        
        # Score from 1-10, inversely related to issue weight
        score = max(1, 10 - min(9, total_weight // 2))
        return score
    
    def _generate_summary(self, issues: List[Issue]) -> str:
        """Generate summary of review results"""
        if not issues:
            return "Code review completed successfully with no issues found."
        
        issue_counts = {}
        for issue in issues:
            key = f"{issue.type.value}_{issue.severity}"
            issue_counts[key] = issue_counts.get(key, 0) + 1
        
        summary_parts = []
        for issue_type in [ReviewType.SECURITY, ReviewType.QUALITY, ReviewType.PERFORMANCE]:
            type_issues = [i for i in issues if i.type == issue_type]
            if type_issues:
                summary_parts.append(f"{len(type_issues)} {issue_type.value} issues")
        
        return f"Found {len(issues)} total issues: {', '.join(summary_parts)}"