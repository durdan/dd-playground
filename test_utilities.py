"""Test utilities and helpers."""
import json
import os
from typing import Any, Dict, List, Optional, Union
from unittest.mock import Mock, MagicMock
import tempfile

class TestDataBuilder:
    """Builder pattern for creating test data."""
    
    def __init__(self):
        self._data = {}
    
    def with_field(self, key: str, value: Any) -> 'TestDataBuilder':
        """Add a field to test data."""
        self._data[key] = value
        return self
    
    def with_fields(self, **kwargs) -> 'TestDataBuilder':
        """Add multiple fields to test data."""
        self._data.update(kwargs)
        return self
    
    def build(self) -> Dict[str, Any]:
        """Build the test data."""
        return self._data.copy()

class MockBuilder:
    """Builder for creating configured mocks."""
    
    def __init__(self, spec: Optional[type] = None):
        self._mock = Mock(spec=spec) if spec else Mock()
        self._return_values = {}
        self._side_effects = {}
    
    def returns(self, method_name: str, value: Any) -> 'MockBuilder':
        """Set return value for a method."""
        self._return_values[method_name] = value
        return self
    
    def raises(self, method_name: str, exception: Exception) -> 'MockBuilder':
        """Set method to raise an exception."""
        self._side_effects[method_name] = exception
        return self
    
    def calls(self, method_name: str, side_effect: callable) -> 'MockBuilder':
        """Set side effect for a method."""
        self._side_effects[method_name] = side_effect
        return self
    
    def build(self) -> Mock:
        """Build the configured mock."""
        for method_name, return_value in self._return_values.items():
            setattr(self._mock, method_name, Mock(return_value=return_value))
        
        for method_name, side_effect in self._side_effects.items():
            setattr(self._mock, method_name, Mock(side_effect=side_effect))
        
        return self._mock

class FileTestHelper:
    """Helper for file-based testing."""
    
    @staticmethod
    def create_test_file(content: str, suffix: str = ".txt") -> str:
        """Create a temporary test file."""
        fd, path = tempfile.mkstemp(suffix=suffix)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)
        except:
            os.close(fd)
            raise
        return path
    
    @staticmethod
    def create_test_json(data: Dict[str, Any]) -> str:
        """Create a temporary JSON test file."""
        content = json.dumps(data, indent=2)
        return FileTestHelper.create_test_file(content, ".json")

def assert_dict_subset(actual: Dict, expected_subset: Dict, message: str = ""):
    """Assert that actual dict contains all key-value pairs from expected_subset."""
    missing_keys = []
    wrong_values = []
    
    for key, expected_value in expected_subset.items():
        if key not in actual:
            missing_keys.append(key)
        elif actual[key] != expected_value:
            wrong_values.append(f"{key}: expected {expected_value}, got {actual[key]}")
    
    errors = []
    if missing_keys:
        errors.append(f"Missing keys: {missing_keys}")
    if wrong_values:
        errors.append(f"Wrong values: {wrong_values}")
    
    if errors:
        error_msg = "; ".join(errors)
        if message:
            error_msg = f"{message}: {error_msg}"
        raise AssertionError(error_msg)