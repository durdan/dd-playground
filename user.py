from .role import Role

class User:
    """Represents a user with a role"""
    
    def __init__(self, username: str, role: Role):
        if not username or not username.strip():
            raise ValueError("Username cannot be empty")
        if role is None:
            raise ValueError("Role cannot be None")
            
        self.username = username.strip()
        self.role = role
    
    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.username == other.username and self.role == other.role
    
    def __repr__(self):
        return f"User(username='{self.username}', role={self.role})"