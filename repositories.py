from typing import Dict, List, Optional
from models import User, Organization, UserOrganization
from datetime import datetime

class UserRepository:
    def __init__(self):
        self._users: Dict[int, User] = {}
        self._next_id = 1
    
    def create(self, name: str, email: str) -> User:
        if self.find_by_email(email):
            raise ValueError(f"User with email {email} already exists")
        
        user = User(
            id=self._next_id,
            name=name,
            email=email,
            created_at=datetime.now()
        )
        self._users[self._next_id] = user
        self._next_id += 1
        return user
    
    def find_by_id(self, user_id: int) -> Optional[User]:
        return self._users.get(user_id)
    
    def find_by_email(self, email: str) -> Optional[User]:
        for user in self._users.values():
            if user.email == email:
                return user
        return None
    
    def get_all(self) -> List[User]:
        return list(self._users.values())
    
    def update(self, user_id: int, name: str = None, email: str = None) -> Optional[User]:
        user = self.find_by_id(user_id)
        if not user:
            return None
        
        if email and email != user.email and self.find_by_email(email):
            raise ValueError(f"User with email {email} already exists")
        
        if name:
            user.name = name
        if email:
            user.email = email
        
        return user
    
    def delete(self, user_id: int) -> bool:
        return self._users.pop(user_id, None) is not None

class OrganizationRepository:
    def __init__(self):
        self._organizations: Dict[int, Organization] = {}
        self._next_id = 1
    
    def create(self, name: str, description: str = "") -> Organization:
        if self.find_by_name(name):
            raise ValueError(f"Organization with name {name} already exists")
        
        org = Organization(
            id=self._next_id,
            name=name,
            description=description,
            created_at=datetime.now()
        )
        self._organizations[self._next_id] = org
        self._next_id += 1
        return org
    
    def find_by_id(self, org_id: int) -> Optional[Organization]:
        return self._organizations.get(org_id)
    
    def find_by_name(self, name: str) -> Optional[Organization]:
        for org in self._organizations.values():
            if org.name == name:
                return org
        return None
    
    def get_all(self) -> List[Organization]:
        return list(self._organizations.values())
    
    def update(self, org_id: int, name: str = None, description: str = None) -> Optional[Organization]:
        org = self.find_by_id(org_id)
        if not org:
            return None
        
        if name and name != org.name and self.find_by_name(name):
            raise ValueError(f"Organization with name {name} already exists")
        
        if name:
            org.name = name
        if description is not None:
            org.description = description
        
        return org
    
    def delete(self, org_id: int) -> bool:
        return self._organizations.pop(org_id, None) is not None

class UserOrganizationRepository:
    def __init__(self):
        self._memberships: List[UserOrganization] = []
    
    def add_membership(self, user_id: int, org_id: int) -> UserOrganization:
        if self.is_member(user_id, org_id):
            raise ValueError("User is already a member of this organization")
        
        membership = UserOrganization(
            user_id=user_id,
            organization_id=org_id,
            joined_at=datetime.now()
        )
        self._memberships.append(membership)
        return membership
    
    def remove_membership(self, user_id: int, org_id: int) -> bool:
        for i, membership in enumerate(self._memberships):
            if membership.user_id == user_id and membership.organization_id == org_id:
                del self._memberships[i]
                return True
        return False
    
    def is_member(self, user_id: int, org_id: int) -> bool:
        return any(
            m.user_id == user_id and m.organization_id == org_id 
            for m in self._memberships
        )
    
    def get_user_organizations(self, user_id: int) -> List[int]:
        return [m.organization_id for m in self._memberships if m.user_id == user_id]
    
    def get_organization_users(self, org_id: int) -> List[int]:
        return [m.user_id for m in self._memberships if m.organization_id == org_id]