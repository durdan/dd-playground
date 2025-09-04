import os
from typing import List, Dict, Set

class FileAnalyzer:
    """Utility to analyze code files and determine review scope"""
    
    SUPPORTED_EXTENSIONS = {'.py', '.js', '.ts', '.java', '.cpp', '.c', '.cs', '.go', '.rb', '.php'}
    
    @classmethod
    def read_files(cls, file_paths: List[str]) -> str:
        """Read and combine content from multiple files"""
        if not file_paths:
            raise ValueError("No file paths provided")
        
        combined_content = []
        
        for file_path in file_paths:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            if not cls._is_supported_file(file_path):
                raise ValueError(f"Unsupported file type: {file_path}")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    combined_content.append(f"=== {file_path} ===\n{content}\n")
            except UnicodeDecodeError:
                raise ValueError(f"Unable to read file (encoding issue): {file_path}")
        
        return '\n'.join(combined_content)
    
    @classmethod
    def _is_supported_file(cls, file_path: str) -> bool:
        """Check if file extension is supported"""
        _, ext = os.path.splitext(file_path)
        return ext.lower() in cls.SUPPORTED_EXTENSIONS
    
    @classmethod
    def get_file_stats(cls, file_paths: List[str]) -> Dict[str, int]:
        """Get basic statistics about the files"""
        stats = {
            'total_files': len(file_paths),
            'total_lines': 0,
            'total_chars': 0
        }
        
        for file_path in file_paths:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    stats['total_lines'] += len(content.splitlines())
                    stats['total_chars'] += len(content)
        
        return stats