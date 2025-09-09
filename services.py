from typing import List, Optional
from models import User, Organization
from repositories import UserRepository, OrganizationRepository, UserOrganizationRepository

class UserService:
    def __init__(self, user_repo: UserRepository, user_org_repo: UserOrganizationRepository):
        self.user_repo = user_repo
        self.user_org_repo = user_org_repo
    
    def create_user(self, name: str, email: str) -> User:
        return self.user_repo.create(name, email)
    
    def get_user(self, user_id: int) -> Optional[User]:
        return self.user_repo.find_by_id(user_id)
    
    def get_all_users(self) -> List[User]:
        return self.user_repo.get_all()
    
    def update_user(self, user_id: int, name: str = None, email: str = None) -> Optional[User]:
        return self.user_repo.update(user_id, name, email)
    
    def delete_user(self, user_id: int) -> bool:
        # Remove from all organizations first
        org_ids = self.user_org_repo.get_user_organizations(user_id)
        for org_id in org_ids:
            self.user_org_repo.remove_membership(user_id, org_id)
        
        return self.user_repo.delete(user_id)
    
    def join_organization(self, user_id: int, org_id: int) -> bool:
        if not self.user_repo.find_by_id(user_id):
            raise ValueError("User not found")
        
        self.user_org_repo.add_membership(user_id, org_id)
        return True
    
    def leave_organization(self, user_id: int, org_id: int) -> bool:
        return self.user_org_repo.remove_membership(user_id, org_id)
    
    def get_user_organizations(self, user_id: int) -> List[int]:
        return self.user_org_repo.get_user_organizations(user_id)

class OrganizationService:
    def __init__(self, org_repo: OrganizationRepository, user_org_repo: UserOrganizationRepository):
        self.org_repo = org_repo
        self.user_org_repo = user_org_repo
    
    def create_organization(self, name: str, description: str = "") -> Organization:
        return self.org_repo.create(name, description)
    
    def get_organization(self, org_id: int) -> Optional[Organization]:
        return self.org_repo.find_by_id(org_id)
    
    def get_all_organizations(self) -> List[Organization]:
        return self.org_repo.get_all()
    
    def update_organization(self, org_id: int, name: str = None, description: str = None) -> Optional[Organization]:
        return self.org_repo.update(org_id, name, description)
    
    def delete_organization(self, org_id: int) -> bool:
        # Remove all memberships first
        user_ids = self.user_org_repo.get_organization_users(org_id)
        for user_id in user_ids:
            self.user_org_repo.remove_membership(user_id, org_id)
        
        return self.org_repo.delete(org_id)
    
    def get_organization_members(self, org_id: int) -> List[int]:
        return self.user_org_repo.get_organization_users(org_id)