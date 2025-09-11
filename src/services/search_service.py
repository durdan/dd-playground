import sqlite3
from typing import List, Dict, Any
from contextlib import contextmanager

from ..security.encryption import SecurityManager

class SearchService:
    def __init__(self, db_path: str, security_manager: SecurityManager):
        self.db_path = db_path
        self.security = security_manager
    
    @contextmanager
    def _get_connection(self):
        """Get database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    def search_conversations(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Search conversations by content."""
        if not query.strip():
            return []
        
        # Create search hash for the query
        search_terms = query.lower().split()
        search_hashes = [self.security.hash_for_search(term) for term in search_terms]
        
        with self._get_connection() as conn:
            # Search by hash matches (approximate search)
            placeholders = ','.join(['?' for _ in search_hashes])
            results = conn.execute(f'''
                SELECT DISTINCT c.id, c.title, c.updated_at, 
                       COUNT(m.id) as message_count
                FROM conversations c
                JOIN messages m ON c.id = m.conversation_id
                WHERE m.search_hash IN ({placeholders})
                GROUP BY c.id, c.title, c.updated_at
                ORDER BY c.updated_at DESC
                LIMIT ?
            ''', search_hashes + [limit]).fetchall()
            
            return [
                {
                    'id': row['id'],
                    'title': row['title'],
                    'updated_at': row['updated_at'],
                    'message_count': row['message_count']
                }
                for row in results
            ]
    
    def search_messages(self, query: str, conversation_id: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Search messages within conversations."""
        if not query.strip():
            return []
        
        search_terms = query.lower().split()
        search_hashes = [self.security.hash_for_search(term) for term in search_terms]
        
        with self._get_connection() as conn:
            if conversation_id:
                placeholders = ','.join(['?' for _ in search_hashes])
                results = conn.execute(f'''
                    SELECT m.id, m.conversation_id, m.role, m.timestamp,
                           c.title as conversation_title
                    FROM messages m
                    JOIN conversations c ON m.conversation_id = c.id
                    WHERE m.conversation_id = ? AND m.search_hash IN ({placeholders})
                    ORDER BY m.timestamp DESC
                    LIMIT ?
                ''', [conversation_id] + search_hashes + [limit]).fetchall()
            else:
                placeholders = ','.join(['?' for _ in search_hashes])
                results = conn.execute(f'''
                    SELECT m.id, m.conversation_id, m.role, m.timestamp,
                           c.title as conversation_title
                    FROM messages m
                    JOIN conversations c ON m.conversation_id = c.id
                    WHERE m.search_hash IN ({placeholders})
                    ORDER BY m.timestamp DESC
                    LIMIT ?
                ''', search_hashes + [limit]).fetchall()
            
            return [
                {
                    'id': row['id'],
                    'conversation_id': row['conversation_id'],
                    'conversation_title': row['conversation_title'],
                    'role': row['role'],
                    'timestamp': row['timestamp']
                }
                for row in results
            ]