import uuid
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

@dataclass
class Comment:
    id: str
    text: str
    section: str
    line_number: int
    author_id: str
    author_name: str
    timestamp: str
    resolved: bool = False
    resolved_by: Optional[str] = None
    resolved_at: Optional[str] = None

class CommentManager:
    def __init__(self):
        self.comments: Dict[str, Comment] = {}
    
    def add_comment(self, text: str, section: str, line_number: int, 
                   author_id: str, author_name: str) -> Dict:
        """Add a new comment"""
        if not text.strip():
            raise ValueError("Comment text cannot be empty")
        
        comment = Comment(
            id=str(uuid.uuid4()),
            text=text.strip(),
            section=section,
            line_number=line_number,
            author_id=author_id,
            author_name=author_name,
            timestamp=datetime.now().isoformat()
        )
        
        self.comments[comment.id] = comment
        return asdict(comment)
    
    def resolve_comment(self, comment_id: str, resolver_id: str, resolver_name: str) -> bool:
        """Mark comment as resolved"""
        if comment_id not in self.comments:
            return False
        
        comment = self.comments[comment_id]
        if comment.resolved:
            return False
        
        comment.resolved = True
        comment.resolved_by = resolver_name
        comment.resolved_at = datetime.now().isoformat()
        return True
    
    def get_comment(self, comment_id: str) -> Optional[Dict]:
        """Get specific comment"""
        comment = self.comments.get(comment_id)
        return asdict(comment) if comment else None
    
    def get_all_comments(self) -> List[Dict]:
        """Get all comments"""
        return [asdict(comment) for comment in self.comments.values()]
    
    def get_comments_for_section(self, section: str) -> List[Dict]:
        """Get comments for specific section"""
        return [
            asdict(comment) for comment in self.comments.values() 
            if comment.section == section
        ]
    
    def get_unresolved_comments(self) -> List[Dict]:
        """Get all unresolved comments"""
        return [
            asdict(comment) for comment in self.comments.values() 
            if not comment.resolved
        ]