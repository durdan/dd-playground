import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, MagicMock

@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path)

@pytest.fixture
def sample_chat_input():
    """Sample chat input for testing."""
    return {
        "message": "Create a REST API for user management with CRUD operations",
        "context": "Building a web application",
        "requirements": ["authentication", "validation", "error handling"]
    }

@pytest.fixture
def expected_spec_structure():
    """Expected structure of generated spec."""
    return {
        "title": str,
        "version": str,
        "description": str,
        "endpoints": list,
        "models": dict,
        "authentication": dict
    }

@pytest.fixture
def mock_llm_client():
    """Mock LLM client for testing."""
    mock = Mock()
    mock.generate_response.return_value = {
        "content": "Generated API specification content",
        "metadata": {"tokens_used": 150, "model": "test-model"}
    }
    return mock

@pytest.fixture
def mock_file_system(temp_dir):
    """Mock file system operations."""
    mock = Mock()
    mock.write_file = Mock()
    mock.read_file = Mock(return_value="file content")
    mock.ensure_directory = Mock()
    mock.base_path = temp_dir
    return mock