from typing import Dict, Optional, List
from models.user import User
from exceptions.user_exceptions import UserNotFoundError, UserAlreadyExistsError

class UserRepository:
    def __init__(self):
        self._users: Dict[str, User] = {}
        self._email_index: Dict[str, str] = {}  # email -> user_id mapping
        self._username_index: Dict[str, str] = {}  # username -> user_id mapping
    
    def save(self, user: User) -> User:
        if user.id in self._users:
            # Update existing user
            old_user = self._users[user.id]
            self._remove_from_indexes(old_user)
        else:
            # Check for duplicates
            if user.email in self._email_index:
                raise UserAlreadyExistsError(f"User with email {user.email} already exists")
            if user.username in self._username_index:
                raise UserAlreadyExistsError(f"User with username {user.username} already exists")
        
        self._users[user.id] = user
        self._add_to_indexes(user)
        return user
    
    def find_by_id(self, user_id: str) -> Optional[User]:
        return self._users.get(user_id)
    
    def find_by_email(self, email: str) -> Optional[User]:
        user_id = self._email_index.get(email)
        return self._users.get(user_id) if user_id else None
    
    def find_by_username(self, username: str) -> Optional[User]:
        user_id = self._username_index.get(username)
        return self._users.get(user_id) if user_id else None
    
    def find_all(self) -> List[User]:
        return list(self._users.values())
    
    def delete(self, user_id: str) -> bool:
        user = self._users.get(user_id)
        if not user:
            return False
        
        del self._users[user_id]
        self._remove_from_indexes(user)
        return True
    
    def _add_to_indexes(self, user: User):
        self._email_index[user.email] = user.id
        self._username_index[user.username] = user.id
    
    def _remove_from_indexes(self, user: User):
        self._email_index.pop(user.email, None)
        self._username_index.pop(user.username, None)