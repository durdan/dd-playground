from typing import List, Optional
from models import User, Organization, Role
from repositories import UserRepository, OrganizationRepository
from exceptions import ValidationError, PermissionError, NotFoundError

class UserService:
    def __init__(self, user_repo: UserRepository, org_repo: OrganizationRepository):
        self.user_repo = user_repo
        self.org_repo = org_repo

    def create_user(self, user_id: str, email: str, name: str, 
                   role: Role = Role.MEMBER, organization_id: Optional[str] = None) -> User:
        if organization_id:
            # Verify organization exists
            self.org_repo.get_by_id(organization_id)
        
        user = User(
            id=user_id,
            email=email,
            name=name,
            role=role,
            organization_id=organization_id
        )
        return self.user_repo.create(user)

    def get_user(self, user_id: str) -> User:
        return self.user_repo.get_by_id(user_id)

    def get_user_by_email(self, email: str) -> User:
        return self.user_repo.get_by_email(email)

    def update_user(self, user_id: str, email: Optional[str] = None, 
                   name: Optional[str] = None, role: Optional[Role] = None,
                   organization_id: Optional[str] = None, is_active: Optional[bool] = None) -> User:
        user = self.user_repo.get_by_id(user_id)
        
        if email is not None:
            user.email = email
        if name is not None:
            user.name = name
        if role is not None:
            user.role = role
        if organization_id is not None:
            if organization_id:
                self.org_repo.get_by_id(organization_id)
            user.organization_id = organization_id
        if is_active is not None:
            user.is_active = is_active
        
        # Re-validate after updates
        user._validate()
        return self.user_repo.update(user)

    def delete_user(self, user_id: str) -> None:
        self.user_repo.delete(user_id)

    def assign_to_organization(self, user_id: str, org_id: str, requesting_user_id: str) -> User:
        requesting_user = self.user_repo.get_by_id(requesting_user_id)
        
        # Check permissions: must be admin of target organization or system admin
        if requesting_user.organization_id != org_id or not requesting_user.has_permission(Role.ADMIN):
            if requesting_user.role != Role.ADMIN or requesting_user.organization_id is not None:
                raise PermissionError("Insufficient permissions to assign user to organization")
        
        # Verify organization exists
        self.org_repo.get_by_id(org_id)
        
        return self.update_user(user_id, organization_id=org_id)

    def get_organization_users(self, org_id: str) -> List[User]:
        # Verify organization exists
        self.org_repo.get_by_id(org_id)
        return self.user_repo.get_by_organization(org_id)

class OrganizationService:
    def __init__(self, org_repo: OrganizationRepository, user_repo: UserRepository):
        self.org_repo = org_repo
        self.user_repo = user_repo

    def create_organization(self, org_id: str, name: str, description: str = "") -> Organization:
        organization = Organization(
            id=org_id,
            name=name,
            description=description
        )
        return self.org_repo.create(organization)

    def get_organization(self, org_id: str) -> Organization:
        return self.org_repo.get_by_id(org_id)

    def update_organization(self, org_id: str, name: Optional[str] = None, 
                          description: Optional[str] = None, is_active: Optional[bool] = None) -> Organization:
        organization = self.org_repo.get_by_id(org_id)
        
        if name is not None:
            organization.name = name
        if description is not None:
            organization.description = description
        if is_active is not None:
            organization.is_active = is_active
        
        # Re-validate after updates
        organization._validate()
        return self.org_repo.update(organization)

    def delete_organization(self, org_id: str, requesting_user_id: str) -> None:
        requesting_user = self.user_repo.get_by_id(requesting_user_id)
        
        # Check permissions: must be admin of the organization
        if (requesting_user.organization_id != org_id or 
            not requesting_user.has_permission(Role.ADMIN)):
            raise PermissionError("Insufficient permissions to delete organization")
        
        # Remove users from organization before deleting
        org_users = self.user_repo.get_by_organization(org_id)
        for user in org_users:
            user.organization_id = None
            self.user_repo.update(user)
        
        self.org_repo.delete(org_id)

    def get_all_organizations(self) -> List[Organization]:
        return self.org_repo.get_all()