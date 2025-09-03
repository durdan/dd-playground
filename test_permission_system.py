import unittest
from permission_system import Role, Permission, User, PermissionChecker, RolePermissionMapper

class TestRolePermissionMapper(unittest.TestCase):
    
    def test_admin_permissions(self):
        permissions = RolePermissionMapper.get_permissions(Role.ADMIN)
        expected = {Permission.READ, Permission.WRITE, Permission.DELETE, Permission.MANAGE_USERS}
        self.assertEqual(permissions, expected)
    
    def test_user_permissions(self):
        permissions = RolePermissionMapper.get_permissions(Role.USER)
        expected = {Permission.READ, Permission.WRITE}
        self.assertEqual(permissions, expected)
    
    def test_none_role_raises_error(self):
        with self.assertRaises(ValueError) as context:
            RolePermissionMapper.get_permissions(None)
        self.assertIn("Role cannot be None", str(context.exception))

class TestUser(unittest.TestCase):
    
    def test_valid_user_creation(self):
        user = User("john", Role.USER)
        self.assertEqual(user.username, "john")
        self.assertEqual(user.role, Role.USER)
    
    def test_empty_username_raises_error(self):
        with self.assertRaises(ValueError) as context:
            User("", Role.USER)
        self.assertIn("Username cannot be empty", str(context.exception))
    
    def test_none_role_raises_error(self):
        with self.assertRaises(ValueError) as context:
            User("john", None)
        self.assertIn("Role cannot be None", str(context.exception))
    
    def test_whitespace_username_trimmed(self):
        user = User("  john  ", Role.USER)
        self.assertEqual(user.username, "john")

class TestPermissionChecker(unittest.TestCase):
    
    def setUp(self):
        self.checker = PermissionChecker()
        self.admin_user = User("admin", Role.ADMIN)
        self.regular_user = User("user", Role.USER)
    
    def test_admin_has_all_permissions(self):
        self.assertTrue(self.checker.has_permission(self.admin_user, Permission.READ))
        self.assertTrue(self.checker.has_permission(self.admin_user, Permission.WRITE))
        self.assertTrue(self.checker.has_permission(self.admin_user, Permission.DELETE))
        self.assertTrue(self.checker.has_permission(self.admin_user, Permission.MANAGE_USERS))
    
    def test_user_has_limited_permissions(self):
        self.assertTrue(self.checker.has_permission(self.regular_user, Permission.READ))
        self.assertTrue(self.checker.has_permission(self.regular_user, Permission.WRITE))
        self.assertFalse(self.checker.has_permission(self.regular_user, Permission.DELETE))
        self.assertFalse(self.checker.has_permission(self.regular_user, Permission.MANAGE_USERS))
    
    def test_check_permission_success(self):
        # Should not raise exception
        self.checker.check_permission(self.admin_user, Permission.DELETE)
    
    def test_check_permission_failure(self):
        with self.assertRaises(PermissionError) as context:
            self.checker.check_permission(self.regular_user, Permission.DELETE)
        self.assertIn("does not have 'delete' permission", str(context.exception))
    
    def test_none_user_raises_error(self):
        with self.assertRaises(ValueError) as context:
            self.checker.has_permission(None, Permission.READ)
        self.assertIn("User cannot be None", str(context.exception))
    
    def test_none_permission_raises_error(self):
        with self.assertRaises(ValueError) as context:
            self.checker.has_permission(self.regular_user, None)
        self.assertIn("Permission cannot be None", str(context.exception))

if __name__ == '__main__':
    unittest.main()