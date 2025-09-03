import sqlite3
from typing import Optional, List
from contextlib import contextmanager
from models.user import User, UserValidationError

class UserRepository:
    def __init__(self, db_path: str = "users.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize the database with users table"""
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
    
    @contextmanager
    def _get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    def create(self, user: User) -> User:
        """Create a new user in the database"""
        try:
            with self._get_connection() as conn:
                cursor = conn.execute(
                    "INSERT INTO users (email, password_hash, created_at) VALUES (?, ?, ?)",
                    (user.email, user.password_hash, user.created_at)
                )
                conn.commit()
                user.id = cursor.lastrowid
                return user
        except sqlite3.IntegrityError:
            raise UserValidationError("Email already exists")
    
    def find_by_email(self, email: str) -> Optional[User]:
        """Find user by email"""
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM users WHERE email = ?", (email,)
            ).fetchone()
            
            if row:
                return User(
                    id=row['id'],
                    email=row['email'],
                    password_hash=row['password_hash'],
                    created_at=row['created_at']
                )
            return None
    
    def find_by_id(self, user_id: int) -> Optional[User]:
        """Find user by ID"""
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM users WHERE id = ?", (user_id,)
            ).fetchone()
            
            if row:
                return User(
                    id=row['id'],
                    email=row['email'],
                    password_hash=row['password_hash'],
                    created_at=row['created_at']
                )
            return None
    
    def update_password(self, user_id: int, new_password_hash: str) -> bool:
        """Update user's password hash"""
        with self._get_connection() as conn:
            cursor = conn.execute(
                "UPDATE users SET password_hash = ? WHERE id = ?",
                (new_password_hash, user_id)
            )
            conn.commit()
            return cursor.rowcount > 0