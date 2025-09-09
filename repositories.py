from typing import Dict, List, Optional
from models import User, Organization
from exceptions import NotFoundError, DuplicateError

class UserRepository:
    def __init__(self):
        self._users: Dict[str, User] = {}
        self._email_index: Dict[str, str] = {}  # email -> user_id

    def create(self, user: User) -> User:
        if user.id in self._users:
            raise DuplicateError(f"User with ID {user.id} already exists")
        
        if user.email in self._email_index:
            raise DuplicateError(f"User with email {user.email} already exists")
        
        self._users[user.id] = user
        self._email_index[user.email] = user.id
        return user

    def get_by_id(self, user_id: str) -> User:
        if user_id not in self._users:
            raise NotFoundError(f"User with ID {user_id} not found")
        return self._users[user_id]

    def get_by_email(self, email: str) -> User:
        if email not in self._email_index:
            raise NotFoundError(f"User with email {email} not found")
        user_id = self._email_index[email]
        return self._users[user_id]

    def update(self, user: User) -> User:
        if user.id not in self._users:
            raise NotFoundError(f"User with ID {user.id} not found")
        
        old_user = self._users[user.id]
        if old_user.email != user.email:
            if user.email in self._email_index:
                raise DuplicateError(f"User with email {user.email} already exists")
            del self._email_index[old_user.email]
            self._email_index[user.email] = user.id
        
        self._users[user.id] = user
        return user

    def delete(self, user_id: str) -> None:
        if user_id not in self._users:
            raise NotFoundError(f"User with ID {user_id} not found")
        
        user = self._users[user_id]
        del self._email_index[user.email]
        del self._users[user_id]

    def get_by_organization(self, org_id: str) -> List[User]:
        return [user for user in self._users.values() 
                if user.organization_id == org_id and user.is_active]

    def get_all(self) -> List[User]:
        return list(self._users.values())

class OrganizationRepository:
    def __init__(self):
        self._organizations: Dict[str, Organization] = {}

    def create(self, organization: Organization) -> Organization:
        if organization.id in self._organizations:
            raise DuplicateError(f"Organization with ID {organization.id} already exists")
        
        self._organizations[organization.id] = organization
        return organization

    def get_by_id(self, org_id: str) -> Organization:
        if org_id not in self._organizations:
            raise NotFoundError(f"Organization with ID {org_id} not found")
        return self._organizations[org_id]

    def update(self, organization: Organization) -> Organization:
        if organization.id not in self._organizations:
            raise NotFoundError(f"Organization with ID {organization.id} not found")
        
        self._organizations[organization.id] = organization
        return organization

    def delete(self, org_id: str) -> None:
        if org_id not in self._organizations:
            raise NotFoundError(f"Organization with ID {org_id} not found")
        
        del self._organizations[org_id]

    def get_all(self) -> List[Organization]:
        return list(self._organizations.values())