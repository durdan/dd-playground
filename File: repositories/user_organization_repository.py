from typing import List, Optional
import sqlite3
from datetime import datetime
from models.user_organization import UserOrganization, Role

class UserOrganizationRepository:
    def __init__(self, db_path: str = "app.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS user_organizations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    organization_id INTEGER NOT NULL,
                    role TEXT NOT NULL,
                    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                    FOREIGN KEY (organization_id) REFERENCES organizations (id) ON DELETE CASCADE,
                    UNIQUE(user_id, organization_id)
                )
            """)
    
    def add_user_to_organization(self, user_org: UserOrganization) -> UserOrganization:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                INSERT INTO user_organizations (user_id, organization_id, role)
                VALUES (?, ?, ?)
            """, (user_org.user_id, user_org.organization_id, user_org.role.value))
            
            user_org.id = cursor.lastrowid
            user_org.joined_at = datetime.now()
            return user_org
    
    def get_user_organizations(self, user_id: int) -> List[UserOrganization]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM user_organizations WHERE user_id = ?
            """, (user_id,))
            rows = cursor.fetchall()
            
            return [UserOrganization(
                id=row['id'],
                user_id=row['user_id'],
                organization_id=row['organization_id'],
                role=Role(row['role']),
                joined_at=datetime.fromisoformat(row['joined_at'])
            ) for row in rows]
    
    def get_organization_users(self, organization_id: int) -> List[UserOrganization]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM user_organizations WHERE organization_id = ?
            """, (organization_id,))
            rows = cursor.fetchall()
            
            return [UserOrganization(
                id=row['id'],
                user_id=row['user_id'],
                organization_id=row['organization_id'],
                role=Role(row['role']),
                joined_at=datetime.fromisoformat(row['joined_at'])
            ) for row in rows]
    
    def update_user_role(self, user_id: int, organization_id: int, new_role: Role) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                UPDATE user_organizations 
                SET role = ? 
                WHERE user_id = ? AND organization_id = ?
            """, (new_role.value, user_id, organization_id))
            return cursor.rowcount > 0
    
    def remove_user_from_organization(self, user_id: int, organization_id: int) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                DELETE FROM user_organizations 
                WHERE user_id = ? AND organization_id = ?
            """, (user_id, organization_id))
            return cursor.rowcount > 0