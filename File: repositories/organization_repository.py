from typing import List, Optional
import sqlite3
from datetime import datetime
from models.organization import Organization, OrganizationStatus
from repositories.base_repository import BaseRepository

class OrganizationRepository(BaseRepository[Organization]):
    def __init__(self, db_path: str = "app.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS organizations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    status TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
    
    def create(self, org: Organization) -> Organization:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                INSERT INTO organizations (name, description, status)
                VALUES (?, ?, ?)
            """, (org.name, org.description, org.status.value))
            
            org.id = cursor.lastrowid
            org.created_at = datetime.now()
            org.updated_at = datetime.now()
            return org
    
    def get_by_id(self, id: int) -> Optional[Organization]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM organizations WHERE id = ?", (id,))
            row = cursor.fetchone()
            
            if row:
                return Organization(
                    id=row['id'],
                    name=row['name'],
                    description=row['description'],
                    status=OrganizationStatus(row['status']),
                    created_at=datetime.fromisoformat(row['created_at']),
                    updated_at=datetime.fromisoformat(row['updated_at'])
                )
            return None
    
    def update(self, org: Organization) -> Organization:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE organizations 
                SET name=?, description=?, status=?, updated_at=CURRENT_TIMESTAMP
                WHERE id=?
            """, (org.name, org.description, org.status.value, org.id))
            org.updated_at = datetime.now()
            return org
    
    def delete(self, id: int) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("DELETE FROM organizations WHERE id = ?", (id,))
            return cursor.rowcount > 0
    
    def list_all(self) -> List[Organization]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM organizations ORDER BY created_at DESC")
            rows = cursor.fetchall()
            
            return [Organization(
                id=row['id'],
                name=row['name'],
                description=row['description'],
                status=OrganizationStatus(row['status']),
                created_at=datetime.fromisoformat(row['created_at']),
                updated_at=datetime.fromisoformat(row['updated_at'])
            ) for row in rows]