from typing import List, Optional, Dict
from models.user import User

class UserRepository:
    def __init__(self):
        self._users: Dict[int, User] = {}
        self._next_id = 1
        self._username_index: Dict[str, int] = {}
        self._email_index: Dict[str, int] = {}
    
    def save(self, user: User) -> User:
        if user.id is None:
            user.id = self._next_id
            self._next_id += 1
        
        # Check for duplicates
        if user.username in self._username_index:
            existing_id = self._username_index[user.username]
            if existing_id != user.id:
                raise ValueError(f"Username '{user.username}' already exists")
        
        if user.email in self._email_index:
            existing_id = self._email_index[user.email]
            if existing_id != user.id:
                raise ValueError(f"Email '{user.email}' already exists")
        
        self._users[user.id] = user
        self._username_index[user.username] = user.id
        self._email_index[user.email] = user.id
        
        return user
    
    def find_by_id(self, user_id: int) -> Optional[User]:
        return self._users.get(user_id)
    
    def find_by_username(self, username: str) -> Optional[User]:
        user_id = self._username_index.get(username)
        return self._users.get(user_id) if user_id else None
    
    def find_by_email(self, email: str) -> Optional[User]:
        user_id = self._email_index.get(email)
        return self._users.get(user_id) if user_id else None
    
    def find_all(self) -> List[User]:
        return list(self._users.values())
    
    def delete(self, user_id: int) -> bool:
        user = self._users.get(user_id)
        if not user:
            return False
        
        del self._users[user_id]
        del self._username_index[user.username]
        del self._email_index[user.email]
        return True
    
    def count(self) -> int:
        return len(self._users)