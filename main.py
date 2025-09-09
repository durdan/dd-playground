from models import User, Organization, Role
from repositories import UserRepository, OrganizationRepository
from services import UserService, OrganizationService
from exceptions import UserManagementError

def main():
    # Initialize repositories and services
    user_repo = UserRepository()
    org_repo = OrganizationRepository()
    user_service = UserService(user_repo, org_repo)
    org_service = OrganizationService(org_repo, user_repo)
    
    try:
        # Create organizations
        org1 = org_service.create_organization("org1", "Tech Corp", "Technology company")
        org2 = org_service.create_organization("org2", "Design Studio", "Creative agency")
        
        # Create users
        admin = user_service.create_user("admin1", "admin@techcorp.com", "Admin User", Role.ADMIN, "org1")
        member = user_service.create_user("member1", "member@techcorp.com", "Member User", Role.MEMBER, "org1")
        viewer = user_service.create_user("viewer1", "viewer@design.com", "Viewer User", Role.VIEWER, "org2")
        
        # Demonstrate functionality
        print(f"Created organization: {org1.name}")
        print(f"Created user: {admin.name} ({admin.role.value})")
        
        # Get organization users
        org1_users = user_service.get_organization_users("org1")
        print(f"Organization 1 has {len(org1_users)} users")
        
        # Update user
        updated_member = user_service.update_user("member1", name="Updated Member")
        print(f"Updated user name to: {updated_member.name}")
        
    except UserManagementError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()