import unittest
from datetime import datetime, timedelta
from models import OverrideAuditEntry
from audit_repository import AuditRepository
from audit_logger import AuditLogger
from override_service import OverrideService
from audit_query_service import AuditQueryService

class TestAuditSystem(unittest.TestCase):
    
    def setUp(self):
        self.repository = AuditRepository()
        self.audit_logger = AuditLogger(self.repository)
        self.override_service = OverrideService(self.audit_logger)
        self.query_service = AuditQueryService(self.repository)
    
    def test_log_override_success(self):
        """Test successful override logging."""
        audit_id = self.audit_logger.log_override(
            user_id="user123",
            reason="Business requirement change",
            field_name="price",
            original_value=100.0,
            new_value=150.0,
            entity_type="product",
            entity_id="prod456"
        )
        
        self.assertIsNotNone(audit_id)
        entries = self.query_service.get_all_overrides()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].user_id, "user123")
        self.assertEqual(entries[0].new_value, 150.0)
    
    def test_override_service_integration(self):
        """Test override service with audit logging."""
        audit_id = self.override_service.override_field(
            user_id="admin",
            reason="Price correction",
            entity_type="product",
            entity_id="123",
            field_name="price",
            new_value=99.99,
            ip_address="192.168.1.1"
        )
        
        # Verify override was applied
        current_value = self.override_service.get_field_value("product", "123", "price")
        self.assertEqual(current_value, 99.99)
        
        # Verify audit log
        entries = self.query_service.get_entity_overrides("product", "123")
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].ip_address, "192.168.1.1")
    
    def test_invalid_input_validation(self):
        """Test validation of required fields."""
        with self.assertRaises(ValueError) as context:
            self.audit_logger.log_override(
                user_id="",  # Empty user ID
                reason="Valid reason",
                field_name="price",
                original_value=100,
                new_value=200,
                entity_type="product",
                entity_id="123"
            )
        self.assertIn("User ID is required", str(context.exception))
        
        with self.assertRaises(ValueError):
            self.audit_logger.log_override(
                user_id="user123",
                reason="",  # Empty reason
                field_name="price",
                original_value=100,
                new_value=200,
                entity_type="product",
                entity_id="123"
            )
    
    def test_query_by_user(self):
        """Test querying overrides by user."""
        # Create multiple overrides
        self.audit_logger.log_override("user1", "reason1", "field1", 1, 2, "type1", "id1")
        self.audit_logger.log_override("user2", "reason2", "field2", 3, 4, "type2", "id2")
        self.audit_logger.log_override("user1", "reason3", "field3", 5, 6, "type3", "id3")
        
        user1_overrides = self.query_service.get_user_overrides("user1")
        self.assertEqual(len(user1_overrides), 2)
        
        user2_overrides = self.query_service.get_user_overrides("user2")
        self.assertEqual(len(user2_overrides), 1)
    
    def test_query_by_date_range(self):
        """Test querying overrides by date range."""
        now = datetime.utcnow()
        yesterday = now - timedelta(days=1)
        tomorrow = now + timedelta(days=1)
        
        self.audit_logger.log_override("user1", "reason1", "field1", 1, 2, "type1", "id1")
        
        # Query should find the entry
        entries = self.query_service.get_overrides_by_date_range(yesterday, tomorrow)
        self.assertEqual(len(entries), 1)
        
        # Query outside range should find nothing
        entries = self.query_service.get_overrides_by_date_range(
            yesterday - timedelta(days=1), 
            yesterday
        )
        self.assertEqual(len(entries), 0)

if __name__ == '__main__':
    unittest.main()