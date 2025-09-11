import sqlite3
import json
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from contextlib import contextmanager

from ..models.conversation import ConversationThread, Message
from ..security.encryption import SecurityManager

class ConversationStorage:
    def __init__(self, db_path: str, security_manager: SecurityManager):
        self.db_path = db_path
        self.security = security_manager
        self._init_database()
    
    def _init_database(self):
        """Initialize database schema."""
        with self._get_connection() as conn:
            conn.executescript('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    parent_id TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    metadata TEXT,
                    FOREIGN KEY (parent_id) REFERENCES conversations (id)
                );
                
                CREATE TABLE IF NOT EXISTS messages (
                    id TEXT PRIMARY KEY,
                    conversation_id TEXT NOT NULL,
                    content TEXT NOT NULL,
                    role TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    metadata TEXT,
                    search_hash TEXT,
                    FOREIGN KEY (conversation_id) REFERENCES conversations (id)
                );
                
                CREATE INDEX IF NOT EXISTS idx_conversations_parent 
                ON conversations (parent_id);
                
                CREATE INDEX IF NOT EXISTS idx_messages_conversation 
                ON messages (conversation_id);
                
                CREATE INDEX IF NOT EXISTS idx_messages_search 
                ON messages (search_hash);
                
                CREATE INDEX IF NOT EXISTS idx_conversations_updated 
                ON conversations (updated_at DESC);
            ''')
    
    @contextmanager
    def _get_connection(self):
        """Get database connection with proper cleanup."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def save_conversation(self, conversation: ConversationThread) -> str:
        """Save conversation and return its ID."""
        if not conversation.id:
            conversation.id = str(uuid.uuid4())
        
        with self._get_connection() as conn:
            # Save conversation metadata
            conn.execute('''
                INSERT OR REPLACE INTO conversations 
                (id, title, parent_id, created_at, updated_at, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                conversation.id,
                conversation.title,
                conversation.parent_id,
                conversation.created_at.isoformat(),
                conversation.updated_at.isoformat(),
                json.dumps(conversation.metadata) if conversation.metadata else None
            ))
            
            # Save messages
            for message in conversation.messages:
                if not message.id:
                    message.id = str(uuid.uuid4())
                
                encrypted_content = self.security.encrypt(message.content)
                search_hash = self.security.hash_for_search(message.content)
                
                conn.execute('''
                    INSERT OR REPLACE INTO messages 
                    (id, conversation_id, content, role, timestamp, metadata, search_hash)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    message.id,
                    conversation.id,
                    encrypted_content,
                    message.role,
                    message.timestamp.isoformat(),
                    json.dumps(message.metadata) if message.metadata else None,
                    search_hash
                ))
        
        return conversation.id
    
    def get_conversation(self, conversation_id: str) -> Optional[ConversationThread]:
        """Retrieve conversation by ID."""
        with self._get_connection() as conn:
            # Get conversation metadata
            conv_row = conn.execute(
                'SELECT * FROM conversations WHERE id = ?', 
                (conversation_id,)
            ).fetchone()
            
            if not conv_row:
                return None
            
            # Get messages
            message_rows = conn.execute('''
                SELECT * FROM messages 
                WHERE conversation_id = ? 
                ORDER BY timestamp ASC
            ''', (conversation_id,)).fetchall()
            
            messages = []
            for row in message_rows:
                decrypted_content = self.security.decrypt(row['content'])
                message = Message(
                    id=row['id'],
                    content=decrypted_content,
                    role=row['role'],
                    timestamp=datetime.fromisoformat(row['timestamp']),
                    metadata=json.loads(row['metadata']) if row['metadata'] else None
                )
                messages.append(message)
            
            return ConversationThread(
                id=conv_row['id'],
                title=conv_row['title'],
                parent_id=conv_row['parent_id'],
                created_at=datetime.fromisoformat(conv_row['created_at']),
                updated_at=datetime.fromisoformat(conv_row['updated_at']),
                messages=messages,
                metadata=json.loads(conv_row['metadata']) if conv_row['metadata'] else None
            )
    
    def list_conversations(self, parent_id: Optional[str] = None, limit: int = 50) -> List[ConversationThread]:
        """List conversations, optionally filtered by parent_id."""
        with self._get_connection() as conn:
            if parent_id is None:
                query = '''
                    SELECT * FROM conversations 
                    WHERE parent_id IS NULL 
                    ORDER BY updated_at DESC 
                    LIMIT ?
                '''
                params = (limit,)
            else:
                query = '''
                    SELECT * FROM conversations 
                    WHERE parent_id = ? 
                    ORDER BY updated_at DESC 
                    LIMIT ?
                '''
                params = (parent_id, limit)
            
            rows = conn.execute(query, params).fetchall()
            
            conversations = []
            for row in rows:
                conv = self.get_conversation(row['id'])
                if conv:
                    conversations.append(conv)
            
            return conversations
    
    def delete_conversation(self, conversation_id: str) -> bool:
        """Delete conversation and all its messages."""
        with self._get_connection() as conn:
            # Delete messages first
            conn.execute('DELETE FROM messages WHERE conversation_id = ?', (conversation_id,))
            
            # Delete conversation
            cursor = conn.execute('DELETE FROM conversations WHERE id = ?', (conversation_id,))
            
            return cursor.rowcount > 0