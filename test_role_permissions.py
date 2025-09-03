import unittest
from role_permissions import Role, Permission, RolePermissions, User, PermissionChecker


class TestRolePermissions(unittest.TestCase):
    
    def test_user_permissions(self):
        permissions = RolePermissions.get_permissions(Role.USER)
        expected = {Permission.READ, Permission.WRITE}
        self.assertEqual(permissions, expected)
    
    def test_admin_permissions(self):
        permissions = RolePermissions.get_permissions(Role.ADMIN)
        expected = {Permission.READ, Permission.WRITE, Permission.DELETE, Permission.MANAGE_USERS}
        self.assertEqual(permissions, expected)
    
    def test_invalid_role(self):
        with self.assertRaises(ValueError):
            RolePermissions.get_permissions("invalid_role")


class TestUser(unittest.TestCase):
    
    def test_valid_user_creation(self):
        user = User("john_doe", Role.USER)
        self.assertEqual(user.username, "john_doe")
        self.assertEqual(user.role, Role.USER)
    
    def test_empty_username(self):
        with self.assertRaises(ValueError):
            User("", Role.USER)
        with self.assertRaises(ValueError):
            User("   ", Role.USER)
    
    def test_invalid_role(self):
        with self.assertRaises(ValueError):
            User("john", "invalid_role")


class TestPermissionChecker(unittest.TestCase):
    
    def setUp(self):
        self.checker = PermissionChecker()
        self.user = User("john", Role.USER)
        self.admin = User("admin", Role.ADMIN)
    
    def test_user_has_read_permission(self):
        self.assertTrue(self.checker.has_permission(self.user, Permission.READ))
        self.assertTrue(self.checker.has_permission(self.user, Permission.WRITE))
    
    def test_user_lacks_admin_permissions(self):
        self.assertFalse(self.checker.has_permission(self.user, Permission.DELETE))
        self.assertFalse(self.checker.has_permission(self.user, Permission.MANAGE_USERS))
    
    def test_admin_has_all_permissions(self):
        for permission in Permission:
            self.assertTrue(self.checker.has_permission(self.admin, permission))
    
    def test_require_permission_success(self):
        # Should not raise
        self.checker.require_permission(self.user, Permission.READ)
        self.checker.require_permission(self.admin, Permission.DELETE)
    
    def test_require_permission_failure(self):
        with self.assertRaises(PermissionError) as cm:
            self.checker.require_permission(self.user, Permission.DELETE)
        self.assertIn("john", str(cm.exception))
        self.assertIn("delete", str(cm.exception))
    
    def test_get_user_permissions(self):
        user_perms = self.checker.get_user_permissions(self.user)
        expected = {Permission.READ, Permission.WRITE}
        self.assertEqual(user_perms, expected)
        
        admin_perms = self.checker.get_user_permissions(self.admin)
        self.assertEqual(len(admin_perms), 4)  # All permissions
    
    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            self.checker.has_permission("not_a_user", Permission.READ)
        with self.assertRaises(ValueError):
            self.checker.has_permission(self.user, "not_a_permission")


if __name__ == '__main__':
    unittest.main()