from repositories import UserRepository, OrganizationRepository, UserOrganizationRepository
from services import UserService, OrganizationService

def main():
    # Initialize repositories
    user_repo = UserRepository()
    org_repo = OrganizationRepository()
    user_org_repo = UserOrganizationRepository()
    
    # Initialize services
    user_service = UserService(user_repo, user_org_repo)
    org_service = OrganizationService(org_repo, user_org_repo)
    
    # Demo usage
    try:
        # Create users
        user1 = user_service.create_user("John Doe", "john@example.com")
        user2 = user_service.create_user("Jane Smith", "jane@example.com")
        print(f"Created users: {user1.name}, {user2.name}")
        
        # Create organizations
        org1 = org_service.create_organization("Tech Corp", "A technology company")
        org2 = org_service.create_organization("Design Studio", "Creative design agency")
        print(f"Created organizations: {org1.name}, {org2.name}")
        
        # Add users to organizations
        user_service.join_organization(user1.id, org1.id)
        user_service.join_organization(user2.id, org1.id)
        user_service.join_organization(user1.id, org2.id)
        print("Added users to organizations")
        
        # Display memberships
        user1_orgs = user_service.get_user_organizations(user1.id)
        org1_members = org_service.get_organization_members(org1.id)
        print(f"User {user1.name} is in organizations: {user1_orgs}")
        print(f"Organization {org1.name} has members: {org1_members}")
        
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()