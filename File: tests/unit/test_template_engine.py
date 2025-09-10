import pytest
from unittest.mock import Mock, patch, mock_open
from src.spec.templates import TemplateEngine
from src.exceptions import TemplateError

class TestTemplateEngine:
    
    @pytest.fixture
    def template_engine(self, temp_dir):
        return TemplateEngine(template_dir=temp_dir)
    
    def test_render_template_success(self, template_engine, temp_dir):
        """Test successful template rendering."""
        # Create a test template file
        template_content = "title: {{ title }}\nversion: {{ version }}"
        template_file = temp_dir / "test.yaml.j2"
        template_file.write_text(template_content)
        
        data = {"title": "Test API", "version": "1.0.0"}
        result = template_engine.render("test.yaml", data)
        
        assert "title: Test API" in result
        assert "version: 1.0.0" in result
    
    def test_render_template_not_found(self, template_engine):
        """Test rendering non-existent template."""
        with pytest.raises(TemplateError, match="Template not found"):
            template_engine.render("nonexistent.yaml", {})
    
    def test_render_template_syntax_error(self, template_engine, temp_dir):
        """Test rendering template with syntax error."""
        # Create template with invalid Jinja2 syntax
        template_content = "title: {{ title }\nversion: {{ version }}"
        template_file = temp_dir / "invalid.yaml.j2"
        template_file.write_text(template_content)
        
        with pytest.raises(TemplateError, match="Template syntax error"):
            template_engine.render("invalid.yaml", {"title": "Test"})
    
    def test_list_available_templates(self, template_engine, temp_dir):
        """Test listing available templates."""
        # Create test template files
        (temp_dir / "openapi.yaml.j2").write_text("openapi template")
        (temp_dir / "asyncapi.yaml.j2").write_text("asyncapi template")
        
        templates = template_engine.list_templates()
        
        assert "openapi.yaml" in templates
        assert "asyncapi.yaml" in templates
    
    def test_validate_template_data(self, template_engine):
        """Test template data validation."""
        valid_data = {"title": "Test", "version": "1.0.0"}
        
        # Should not raise any exception
        template_engine.validate_data(valid_data)
    
    def test_validate_template_data_invalid(self, template_engine):
        """Test validation with invalid data types."""
        invalid_data = {"title": 123, "version": None}
        
        with pytest.raises(TemplateError, match="Invalid template data"):
            template_engine.validate_data(invalid_data)