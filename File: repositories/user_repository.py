from typing import List, Optional
import sqlite3
from datetime import datetime
from models.user import User, UserStatus
from repositories.base_repository import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self, db_path: str = "app.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
    
    def create(self, user: User) -> User:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                INSERT INTO users (email, password_hash, first_name, last_name, status)
                VALUES (?, ?, ?, ?, ?)
            """, (user.email, user.password_hash, user.first_name, user.last_name, user.status.value))
            
            user.id = cursor.lastrowid
            user.created_at = datetime.now()
            user.updated_at = datetime.now()
            return user
    
    def get_by_id(self, id: int) -> Optional[User]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM users WHERE id = ?", (id,))
            row = cursor.fetchone()
            
            if row:
                return User(
                    id=row['id'],
                    email=row['email'],
                    password_hash=row['password_hash'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    status=UserStatus(row['status']),
                    created_at=datetime.fromisoformat(row['created_at']),
                    updated_at=datetime.fromisoformat(row['updated_at'])
                )
            return None
    
    def get_by_email(self, email: str) -> Optional[User]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM users WHERE email = ?", (email,))
            row = cursor.fetchone()
            
            if row:
                return User(
                    id=row['id'],
                    email=row['email'],
                    password_hash=row['password_hash'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    status=UserStatus(row['status']),
                    created_at=datetime.fromisoformat(row['created_at']),
                    updated_at=datetime.fromisoformat(row['updated_at'])
                )
            return None
    
    def update(self, user: User) -> User:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE users 
                SET email=?, first_name=?, last_name=?, status=?, updated_at=CURRENT_TIMESTAMP
                WHERE id=?
            """, (user.email, user.first_name, user.last_name, user.status.value, user.id))
            user.updated_at = datetime.now()
            return user
    
    def delete(self, id: int) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("DELETE FROM users WHERE id = ?", (id,))
            return cursor.rowcount > 0
    
    def list_all(self) -> List[User]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM users ORDER BY created_at DESC")
            rows = cursor.fetchall()
            
            return [User(
                id=row['id'],
                email=row['email'],
                password_hash=row['password_hash'],
                first_name=row['first_name'],
                last_name=row['last_name'],
                status=UserStatus(row['status']),
                created_at=datetime.fromisoformat(row['created_at']),
                updated_at=datetime.fromisoformat(row['updated_at'])
            ) for row in rows]