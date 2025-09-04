import os
import pytest
from unittest.mock import patch
from config.settings import Settings, load_config


class TestSettings:
    
    def test_default_settings(self):
        """Test default settings values."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"}, clear=True):
            settings = Settings()
            assert settings.environment == "dev"
            assert settings.openai_api_key == "test_key"
            assert settings.log_level == "INFO"
    
    def test_environment_override(self):
        """Test environment variable override."""
        with patch.dict(os.environ, {
            "ENVIRONMENT": "prod",
            "OPENAI_API_KEY": "prod_key",
            "LOG_LEVEL": "ERROR"
        }, clear=True):
            settings = Settings()
            assert settings.environment == "prod"
            assert settings.openai_api_key == "prod_key"
            assert settings.log_level == "ERROR"
    
    def test_missing_required_field(self):
        """Test validation of required fields."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(Exception):  # Pydantic validation error
                Settings()


class TestLoadConfig:
    
    @patch('config.settings.load_dotenv')
    @patch('os.path.exists')
    def test_load_env_specific_file(self, mock_exists, mock_load_dotenv):
        """Test loading environment-specific config file."""
        mock_exists.return_value = True
        
        with patch.dict(os.environ, {"ENVIRONMENT": "staging"}, clear=True):
            with patch.object(Settings, '__init__', return_value=None):
                load_config()
                mock_load_dotenv.assert_called_with(".env.staging", override=True)
    
    @patch('config.settings.load_dotenv')
    @patch('os.path.exists')
    def test_fallback_to_default_env(self, mock_exists, mock_load_dotenv):
        """Test fallback to default .env file."""
        mock_exists.return_value = False
        
        with patch.dict(os.environ, {"ENVIRONMENT": "nonexistent"}, clear=True):
            with patch.object(Settings, '__init__', return_value=None):
                load_config()
                mock_load_dotenv.assert_called_with(".env")