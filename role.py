from enum import Enum

class Role(Enum):
    USER = "user"
    ADMIN = "admin"

class Permission(Enum):
    READ = "read"
    WRITE = "write" 
    DELETE = "delete"
    MANAGE_USERS = "manage_users"