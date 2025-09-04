"""Base test classes and utilities."""
import unittest
from unittest.mock import Mock, patch, MagicMock
from typing import Any, Dict, List, Optional, Callable
import tempfile
import shutil
from contextlib import contextmanager

class BaseTestCase(unittest.TestCase):
    """Base test case with common utilities."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dirs = []
        self.mocks = []
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Clean up temporary directories
        for temp_dir in self.temp_dirs:
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)
        
        # Stop all mocks
        for mock in self.mocks:
            if hasattr(mock, 'stop'):
                mock.stop()
    
    def create_temp_dir(self) -> str:
        """Create a temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        self.temp_dirs.append(temp_dir)
        return temp_dir
    
    def create_mock(self, target: str, **kwargs) -> Mock:
        """Create and register a mock for cleanup."""
        mock_patch = patch(target, **kwargs)
        mock_obj = mock_patch.start()
        self.mocks.append(mock_patch)
        return mock_obj
    
    def assert_called_with_subset(self, mock_obj: Mock, **expected_kwargs):
        """Assert mock was called with at least the expected kwargs."""
        self.assertTrue(mock_obj.called, "Mock was not called")
        call_args = mock_obj.call_args
        if call_args is None:
            self.fail("Mock was not called with any arguments")
        
        actual_kwargs = call_args.kwargs
        for key, expected_value in expected_kwargs.items():
            self.assertIn(key, actual_kwargs, f"Expected key '{key}' not found in call")
            self.assertEqual(actual_kwargs[key], expected_value, 
                           f"Expected {key}={expected_value}, got {actual_kwargs[key]}")

class UnitTestCase(BaseTestCase):
    """Base class for unit tests - isolated, fast tests."""
    
    def setUp(self):
        super().setUp()
        # Unit tests should be isolated - mock external dependencies by default
        self.mock_external_deps()
    
    def mock_external_deps(self):
        """Override to mock external dependencies."""
        pass

class IntegrationTestCase(BaseTestCase):
    """Base class for integration tests - test component interactions."""
    
    @classmethod
    def setUpClass(cls):
        """Set up integration test environment."""
        super().setUpClass()
        cls.setup_test_environment()
    
    @classmethod
    def tearDownClass(cls):
        """Clean up integration test environment."""
        cls.cleanup_test_environment()
        super().tearDownClass()
    
    @classmethod
    def setup_test_environment(cls):
        """Override to set up test environment."""
        pass
    
    @classmethod
    def cleanup_test_environment(cls):
        """Override to clean up test environment."""
        pass

class PerformanceTestCase(BaseTestCase):
    """Base class for performance tests."""
    
    def assert_execution_time(self, func: Callable, max_seconds: float, *args, **kwargs):
        """Assert function executes within time limit."""
        import time
        start_time = time.time()
        result = func(*args, **kwargs)
        execution_time = time.time() - start_time
        
        self.assertLessEqual(execution_time, max_seconds,
                           f"Function took {execution_time:.3f}s, expected <= {max_seconds}s")
        return result