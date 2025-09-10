import uuid
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

@dataclass
class SpecVersion:
    id: str
    content: str
    section: str
    author: str
    timestamp: str
    changes_summary: str

class SpecificationManager:
    def __init__(self):
        self.current_spec: Dict[str, str] = {'main': ''}
        self.versions: List[SpecVersion] = []
        self._create_initial_version()
    
    def _create_initial_version(self):
        """Create initial empty version"""
        version = SpecVersion(
            id=str(uuid.uuid4()),
            content='',
            section='main',
            author='system',
            timestamp=datetime.now().isoformat(),
            changes_summary='Initial version'
        )
        self.versions.append(version)
    
    def update_specification(self, content: str, section: str = 'main', author: str = 'anonymous') -> str:
        """Update specification content and create new version"""
        if not content.strip():
            raise ValueError("Content cannot be empty")
        
        old_content = self.current_spec.get(section, '')
        self.current_spec[section] = content
        
        # Create version entry
        changes_summary = self._generate_changes_summary(old_content, content)
        version = SpecVersion(
            id=str(uuid.uuid4()),
            content=content,
            section=section,
            author=author,
            timestamp=datetime.now().isoformat(),
            changes_summary=changes_summary
        )
        
        self.versions.append(version)
        return version.id
    
    def _generate_changes_summary(self, old_content: str, new_content: str) -> str:
        """Generate simple summary of changes"""
        old_lines = old_content.split('\n')
        new_lines = new_content.split('\n')
        
        if len(new_lines) > len(old_lines):
            return f"Added {len(new_lines) - len(old_lines)} lines"
        elif len(new_lines) < len(old_lines):
            return f"Removed {len(old_lines) - len(new_lines)} lines"
        else:
            return "Modified content"
    
    def get_current_spec(self) -> Dict[str, str]:
        """Get current specification content"""
        return self.current_spec.copy()
    
    def get_version_history(self) -> List[Dict]:
        """Get version history"""
        return [asdict(version) for version in self.versions[-10:]]  # Last 10 versions
    
    def get_version(self, version_id: str) -> Optional[Dict]:
        """Get specific version by ID"""
        for version in self.versions:
            if version.id == version_id:
                return asdict(version)
        return None
    
    def revert_to_version(self, version_id: str, author: str = 'anonymous') -> bool:
        """Revert to a specific version"""
        version = self.get_version(version_id)
        if not version:
            return False
        
        self.update_specification(
            version['content'], 
            version['section'], 
            f"{author} (reverted to {version_id[:8]})"
        )
        return True