import unittest
from role_permissions import Role, Permission, User, PermissionChecker, RolePermissions


class TestRolePermissions(unittest.TestCase):
    
    def setUp(self):
        self.checker = PermissionChecker()
        self.admin_user = User("admin", Role.ADMIN)
        self.regular_user = User("john", Role.USER)
    
    def test_admin_has_all_permissions(self):
        """Admin should have all permissions"""
        for permission in Permission:
            self.assertTrue(self.checker.has_permission(self.admin_user, permission))
    
    def test_user_has_limited_permissions(self):
        """Regular user should have limited permissions"""
        self.assertTrue(self.checker.has_permission(self.regular_user, Permission.READ))
        self.assertTrue(self.checker.has_permission(self.regular_user, Permission.WRITE))
        self.assertFalse(self.checker.has_permission(self.regular_user, Permission.DELETE))
        self.assertFalse(self.checker.has_permission(self.regular_user, Permission.MANAGE_USERS))
    
    def test_check_permission_success(self):
        """check_permission should not raise for valid permissions"""
        self.checker.check_permission(self.admin_user, Permission.DELETE)
        self.checker.check_permission(self.regular_user, Permission.READ)
    
    def test_check_permission_failure(self):
        """check_permission should raise PermissionError for invalid permissions"""
        with self.assertRaises(PermissionError) as cm:
            self.checker.check_permission(self.regular_user, Permission.DELETE)
        
        self.assertIn("john", str(cm.exception))
        self.assertIn("user", str(cm.exception))
        self.assertIn("delete", str(cm.exception))
    
    def test_get_user_permissions(self):
        """Should return correct permission sets"""
        admin_perms = self.checker.get_user_permissions(self.admin_user)
        user_perms = self.checker.get_user_permissions(self.regular_user)
        
        self.assertEqual(len(admin_perms), 4)
        self.assertEqual(len(user_perms), 2)
        self.assertIn(Permission.MANAGE_USERS, admin_perms)
        self.assertNotIn(Permission.MANAGE_USERS, user_perms)
    
    def test_invalid_user_creation(self):
        """Should reject invalid user data"""
        with self.assertRaises(ValueError):
            User("", Role.USER)
        
        with self.assertRaises(ValueError):
            User("   ", Role.USER)
        
        with self.assertRaises(ValueError):
            User("john", "invalid_role")
    
    def test_invalid_permission_check(self):
        """Should reject invalid inputs to permission methods"""
        with self.assertRaises(ValueError):
            self.checker.has_permission("not_a_user", Permission.READ)
        
        with self.assertRaises(ValueError):
            self.checker.has_permission(self.regular_user, "invalid_permission")
    
    def test_role_permissions_immutable(self):
        """Returned permission sets should be copies"""
        perms1 = RolePermissions.get_permissions(Role.USER)
        perms2 = RolePermissions.get_permissions(Role.USER)
        
        perms1.add(Permission.DELETE)  # Modify copy
        self.assertNotEqual(perms1, perms2)  # Should not affect original


if __name__ == '__main__':
    unittest.main()