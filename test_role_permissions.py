import unittest
from role_permissions import Role, Permission, RolePermissions, User, PermissionChecker


class TestRolePermissions(unittest.TestCase):
    
    def test_admin_has_all_permissions(self):
        permissions = RolePermissions.get_permissions(Role.ADMIN)
        expected = {Permission.READ, Permission.WRITE, Permission.DELETE, Permission.MANAGE_USERS}
        self.assertEqual(permissions, expected)
    
    def test_user_has_limited_permissions(self):
        permissions = RolePermissions.get_permissions(Role.USER)
        expected = {Permission.READ, Permission.WRITE}
        self.assertEqual(permissions, expected)
    
    def test_invalid_role_raises_error(self):
        with self.assertRaises(ValueError):
            RolePermissions.get_permissions("invalid_role")


class TestUser(unittest.TestCase):
    
    def test_valid_user_creation(self):
        user = User("john_doe", Role.USER)
        self.assertEqual(user.username, "john_doe")
        self.assertEqual(user.role, Role.USER)
    
    def test_empty_username_raises_error(self):
        with self.assertRaises(ValueError):
            User("", Role.USER)
        with self.assertRaises(ValueError):
            User("   ", Role.USER)
    
    def test_invalid_role_raises_error(self):
        with self.assertRaises(ValueError):
            User("john", "invalid_role")


class TestPermissionChecker(unittest.TestCase):
    
    def setUp(self):
        self.checker = PermissionChecker()
        self.admin = User("admin_user", Role.ADMIN)
        self.user = User("regular_user", Role.USER)
    
    def test_admin_has_all_permissions(self):
        self.assertTrue(self.checker.has_permission(self.admin, Permission.READ))
        self.assertTrue(self.checker.has_permission(self.admin, Permission.WRITE))
        self.assertTrue(self.checker.has_permission(self.admin, Permission.DELETE))
        self.assertTrue(self.checker.has_permission(self.admin, Permission.MANAGE_USERS))
    
    def test_user_has_limited_permissions(self):
        self.assertTrue(self.checker.has_permission(self.user, Permission.READ))
        self.assertTrue(self.checker.has_permission(self.user, Permission.WRITE))
        self.assertFalse(self.checker.has_permission(self.user, Permission.DELETE))
        self.assertFalse(self.checker.has_permission(self.user, Permission.MANAGE_USERS))
    
    def test_require_permission_success(self):
        # Should not raise exception
        self.checker.require_permission(self.admin, Permission.DELETE)
        self.checker.require_permission(self.user, Permission.READ)
    
    def test_require_permission_failure(self):
        with self.assertRaises(PermissionError) as context:
            self.checker.require_permission(self.user, Permission.DELETE)
        self.assertIn("lacks permission", str(context.exception))
    
    def test_get_user_permissions(self):
        admin_perms = self.checker.get_user_permissions(self.admin)
        user_perms = self.checker.get_user_permissions(self.user)
        
        self.assertEqual(len(admin_perms), 4)
        self.assertEqual(len(user_perms), 2)
        self.assertIn(Permission.MANAGE_USERS, admin_perms)
        self.assertNotIn(Permission.MANAGE_USERS, user_perms)
    
    def test_invalid_inputs_raise_errors(self):
        with self.assertRaises(ValueError):
            self.checker.has_permission("not_a_user", Permission.READ)
        with self.assertRaises(ValueError):
            self.checker.has_permission(self.user, "not_a_permission")


if __name__ == '__main__':
    unittest.main()