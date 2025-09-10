import pytest
from unittest.mock import Mock, patch
from src.chat.handler import ChatHandler
from src.exceptions import ValidationError, ProcessingError

class TestChatHandler:
    
    @pytest.fixture
    def chat_handler(self, mock_llm_client):
        return ChatHandler(llm_client=mock_llm_client)
    
    def test_process_message_success(self, chat_handler, sample_chat_input):
        """Test successful message processing."""
        result = chat_handler.process_message(sample_chat_input["message"])
        
        assert result is not None
        assert "content" in result
        assert "metadata" in result
        chat_handler.llm_client.generate_response.assert_called_once()
    
    def test_process_message_with_context(self, chat_handler, sample_chat_input):
        """Test message processing with context."""
        result = chat_handler.process_message(
            sample_chat_input["message"],
            context=sample_chat_input["context"]
        )
        
        assert result is not None
        call_args = chat_handler.llm_client.generate_response.call_args[0][0]
        assert sample_chat_input["context"] in call_args
    
    def test_process_empty_message(self, chat_handler):
        """Test processing empty message raises validation error."""
        with pytest.raises(ValidationError, match="Message cannot be empty"):
            chat_handler.process_message("")
    
    def test_process_message_llm_failure(self, chat_handler, mock_llm_client):
        """Test handling LLM client failures."""
        mock_llm_client.generate_response.side_effect = Exception("LLM Error")
        
        with pytest.raises(ProcessingError, match="Failed to process message"):
            chat_handler.process_message("test message")
    
    def test_extract_requirements(self, chat_handler):
        """Test requirement extraction from message."""
        message = "Create API with authentication, validation, and logging"
        requirements = chat_handler.extract_requirements(message)
        
        assert isinstance(requirements, list)
        assert len(requirements) > 0
        assert any("authentication" in req.lower() for req in requirements)
    
    def test_validate_input_success(self, chat_handler):
        """Test successful input validation."""
        valid_input = {
            "message": "Valid message",
            "context": "Valid context"
        }
        
        # Should not raise any exception
        chat_handler.validate_input(valid_input)
    
    def test_validate_input_missing_message(self, chat_handler):
        """Test validation with missing message."""
        invalid_input = {"context": "Valid context"}
        
        with pytest.raises(ValidationError, match="Message is required"):
            chat_handler.validate_input(invalid_input)