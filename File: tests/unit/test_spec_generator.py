import pytest
from unittest.mock import Mock, patch
from src.spec.generator import SpecGenerator
from src.spec.templates import TemplateEngine
from src.exceptions import GenerationError, ValidationError

class TestSpecGenerator:
    
    @pytest.fixture
    def template_engine(self):
        mock = Mock(spec=TemplateEngine)
        mock.render.return_value = "rendered spec content"
        return mock
    
    @pytest.fixture
    def spec_generator(self, template_engine, mock_file_system):
        return SpecGenerator(
            template_engine=template_engine,
            file_system=mock_file_system
        )
    
    def test_generate_spec_success(self, spec_generator, sample_chat_input):
        """Test successful spec generation."""
        spec_data = {
            "title": "User Management API",
            "endpoints": ["/users", "/users/{id}"],
            "methods": ["GET", "POST", "PUT", "DELETE"]
        }
        
        result = spec_generator.generate_spec(spec_data)
        
        assert result is not None
        assert "content" in result
        assert "metadata" in result
        spec_generator.template_engine.render.assert_called_once()
    
    def test_generate_spec_with_template(self, spec_generator):
        """Test spec generation with specific template."""
        spec_data = {"title": "Test API"}
        template_name = "openapi"
        
        result = spec_generator.generate_spec(spec_data, template=template_name)
        
        spec_generator.template_engine.render.assert_called_with(
            template_name, spec_data
        )
    
    def test_generate_spec_invalid_data(self, spec_generator):
        """Test spec generation with invalid data."""
        invalid_data = {}  # Missing required fields
        
        with pytest.raises(ValidationError, match="Invalid spec data"):
            spec_generator.generate_spec(invalid_data)
    
    def test_generate_spec_template_error(self, spec_generator, template_engine):
        """Test handling template rendering errors."""
        template_engine.render.side_effect = Exception("Template error")
        spec_data = {"title": "Test API"}
        
        with pytest.raises(GenerationError, match="Failed to generate spec"):
            spec_generator.generate_spec(spec_data)
    
    def test_save_spec_success(self, spec_generator, temp_dir):
        """Test successful spec saving."""
        spec_content = "openapi: 3.0.0\ninfo:\n  title: Test API"
        filename = "test-api.yaml"
        
        result = spec_generator.save_spec(spec_content, filename)
        
        assert result["success"] is True
        assert result["path"] is not None
        spec_generator.file_system.write_file.assert_called_once()
    
    def test_validate_spec_data_success(self, spec_generator):
        """Test successful spec data validation."""
        valid_data = {
            "title": "Test API",
            "version": "1.0.0",
            "endpoints": ["/test"]
        }
        
        # Should not raise any exception
        spec_generator.validate_spec_data(valid_data)
    
    def test_validate_spec_data_missing_title(self, spec_generator):
        """Test validation with missing title."""
        invalid_data = {"version": "1.0.0"}
        
        with pytest.raises(ValidationError, match="Title is required"):
            spec_generator.validate_spec_data(invalid_data)