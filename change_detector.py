import os
import re
import subprocess
from typing import Dict, List, Set, Any
from pathlib import Path

class ChangeDetector:
    def __init__(self, excluded_patterns: List[str] = None):
        self.excluded_patterns = excluded_patterns or []
        self.excluded_regex = [re.compile(pattern) for pattern in self.excluded_patterns]
    
    def detect_changes(self, base_ref: str = "HEAD~1", target_ref: str = "HEAD") -> Dict[str, Any]:
        """Detect changes between two git references."""
        try:
            return {
                'files_changed': self._count_changed_files(base_ref, target_ref),
                'lines_added': self._count_lines_added(base_ref, target_ref),
                'lines_deleted': self._count_lines_deleted(base_ref, target_ref),
                'lines_modified': self._count_lines_modified(base_ref, target_ref),
                'complexity_increase': self._estimate_complexity_change(base_ref, target_ref),
                'changed_files': self._get_changed_files(base_ref, target_ref)
            }
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Git command failed: {e}")
    
    def _should_exclude_file(self, filepath: str) -> bool:
        """Check if file should be excluded based on patterns."""
        return any(regex.search(filepath) for regex in self.excluded_regex)
    
    def _get_changed_files(self, base_ref: str, target_ref: str) -> List[str]:
        """Get list of changed files."""
        result = subprocess.run(
            ['git', 'diff', '--name-only', f"{base_ref}..{target_ref}"],
            capture_output=True, text=True, check=True
        )
        files = result.stdout.strip().split('\n') if result.stdout.strip() else []
        return [f for f in files if not self._should_exclude_file(f)]
    
    def _count_changed_files(self, base_ref: str, target_ref: str) -> int:
        """Count number of changed files."""
        return len(self._get_changed_files(base_ref, target_ref))
    
    def _count_lines_added(self, base_ref: str, target_ref: str) -> int:
        """Count lines added."""
        result = subprocess.run(
            ['git', 'diff', '--numstat', f"{base_ref}..{target_ref}"],
            capture_output=True, text=True, check=True
        )
        
        total_added = 0
        for line in result.stdout.strip().split('\n'):
            if line:
                parts = line.split('\t')
                if len(parts) >= 3 and not self._should_exclude_file(parts[2]):
                    try:
                        added = int(parts[0]) if parts[0] != '-' else 0
                        total_added += added
                    except ValueError:
                        continue
        
        return total_added
    
    def _count_lines_deleted(self, base_ref: str, target_ref: str) -> int:
        """Count lines deleted."""
        result = subprocess.run(
            ['git', 'diff', '--numstat', f"{base_ref}..{target_ref}"],
            capture_output=True, text=True, check=True
        )
        
        total_deleted = 0
        for line in result.stdout.strip().split('\n'):
            if line:
                parts = line.split('\t')
                if len(parts) >= 3 and not self._should_exclude_file(parts[2]):
                    try:
                        deleted = int(parts[1]) if parts[1] != '-' else 0
                        total_deleted += deleted
                    except ValueError:
                        continue
        
        return total_deleted
    
    def _count_lines_modified(self, base_ref: str, target_ref: str) -> int:
        """Count total lines modified (added + deleted)."""
        return self._count_lines_added(base_ref, target_ref) + self._count_lines_deleted(base_ref, target_ref)
    
    def _estimate_complexity_change(self, base_ref: str, target_ref: str) -> int:
        """Estimate complexity change based on control flow keywords."""
        complexity_keywords = ['if', 'elif', 'else', 'for', 'while', 'try', 'except', 'with']
        
        result = subprocess.run(
            ['git', 'diff', f"{base_ref}..{target_ref}"],
            capture_output=True, text=True, check=True
        )
        
        added_complexity = 0
        for line in result.stdout.split('\n'):
            if line.startswith('+') and not line.startswith('+++'):
                line_content = line[1:].strip().lower()
                for keyword in complexity_keywords:
                    if f' {keyword} ' in f' {line_content} ' or line_content.startswith(f'{keyword} '):
                        added_complexity += 1
        
        return added_complexity