import logging
import traceback
from typing import Optional, Dict, Any, Callable
from enum import Enum
import time
import json
from pathlib import Path

class ErrorType(Enum):
    VALIDATION = "validation"
    API_ERROR = "api_error"
    FILE_ERROR = "file_error"
    NETWORK_ERROR = "network_error"
    PARSING_ERROR = "parsing_error"
    GENERATION_ERROR = "generation_error"
    UNKNOWN = "unknown"

class AppError(Exception):
    """Base application error with user-friendly messaging"""
    def __init__(self, message: str, error_type: ErrorType = ErrorType.UNKNOWN, 
                 details: Optional[Dict[str, Any]] = None, original_error: Optional[Exception] = None):
        self.message = message
        self.error_type = error_type
        self.details = details or {}
        self.original_error = original_error
        super().__init__(message)

class ValidationError(AppError):
    def __init__(self, message: str, field: Optional[str] = None, details: Optional[Dict] = None):
        super().__init__(message, ErrorType.VALIDATION, details)
        self.field = field

class APIError(AppError):
    def __init__(self, message: str, status_code: Optional[int] = None, details: Optional[Dict] = None):
        super().__init__(message, ErrorType.API_ERROR, details)
        self.status_code = status_code

class FileError(AppError):
    def __init__(self, message: str, file_path: Optional[str] = None, details: Optional[Dict] = None):
        super().__init__(message, ErrorType.FILE_ERROR, details)
        self.file_path = file_path

class NetworkError(AppError):
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, ErrorType.NETWORK_ERROR, details)

class ParsingError(AppError):
    def __init__(self, message: str, content: Optional[str] = None, details: Optional[Dict] = None):
        super().__init__(message, ErrorType.PARSING_ERROR, details)
        self.content = content

class GenerationError(AppError):
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, ErrorType.GENERATION_ERROR, details)

class ErrorHandler:
    """Centralized error handling with logging and user-friendly messages"""
    
    def __init__(self, log_file: str = "app.log"):
        self.logger = self._setup_logging(log_file)
        self.error_messages = self._load_error_messages()
    
    def _setup_logging(self, log_file: str) -> logging.Logger:
        """Configure structured logging"""
        logger = logging.getLogger("app_error_handler")
        logger.setLevel(logging.INFO)
        
        # Remove existing handlers
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def _load_error_messages(self) -> Dict[str, str]:
        """Load user-friendly error messages"""
        return {
            ErrorType.VALIDATION.value: "Please check your input and try again.",
            ErrorType.API_ERROR.value: "There was an issue connecting to the service. Please try again later.",
            ErrorType.FILE_ERROR.value: "There was a problem accessing the file. Please check the file path and permissions.",
            ErrorType.NETWORK_ERROR.value: "Network connection failed. Please check your internet connection.",
            ErrorType.PARSING_ERROR.value: "The content could not be processed. Please check the format.",
            ErrorType.GENERATION_ERROR.value: "Failed to generate the specification. Trying alternative approach.",
            ErrorType.UNKNOWN.value: "An unexpected error occurred. Please try again."
        }
    
    def handle_error(self, error: Exception, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Handle any error and return user-friendly response"""
        context = context or {}
        
        if isinstance(error, AppError):
            return self._handle_app_error(error, context)
        else:
            return self._handle_unknown_error(error, context)
    
    def _handle_app_error(self, error: AppError, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle known application errors"""
        error_id = self._generate_error_id()
        
        # Log the error
        self.logger.error(
            f"Error ID: {error_id} | Type: {error.error_type.value} | Message: {error.message}",
            extra={
                "error_id": error_id,
                "error_type": error.error_type.value,
                "details": error.details,
                "context": context,
                "original_error": str(error.original_error) if error.original_error else None
            }
        )
        
        return {
            "success": False,
            "error_id": error_id,
            "error_type": error.error_type.value,
            "message": error.message,
            "user_message": self.error_messages.get(error.error_type.value, error.message),
            "details": error.details
        }
    
    def _handle_unknown_error(self, error: Exception, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle unexpected errors"""
        error_id = self._generate_error_id()
        
        # Log the full traceback
        self.logger.error(
            f"Error ID: {error_id} | Unexpected error: {str(error)}",
            extra={
                "error_id": error_id,
                "error_type": ErrorType.UNKNOWN.value,
                "context": context,
                "traceback": traceback.format_exc()
            }
        )
        
        return {
            "success": False,
            "error_id": error_id,
            "error_type": ErrorType.UNKNOWN.value,
            "message": str(error),
            "user_message": self.error_messages[ErrorType.UNKNOWN.value]
        }
    
    def _generate_error_id(self) -> str:
        """Generate unique error ID for tracking"""
        return f"ERR_{int(time.time() * 1000)}"
    
    def with_fallback(self, primary_func: Callable, fallback_func: Callable, 
                     context: Optional[Dict] = None) -> Any:
        """Execute function with fallback on failure"""
        context = context or {}
        
        try:
            return primary_func()
        except Exception as e:
            self.logger.warning(f"Primary function failed, trying fallback: {str(e)}")
            try:
                return fallback_func()
            except Exception as fallback_error:
                # Both failed, raise the original error with context
                raise GenerationError(
                    "Both primary and fallback methods failed",
                    details={
                        "primary_error": str(e),
                        "fallback_error": str(fallback_error),
                        "context": context
                    }
                )
    
    def retry_with_backoff(self, func: Callable, max_retries: int = 3, 
                          base_delay: float = 1.0, context: Optional[Dict] = None) -> Any:
        """Retry function with exponential backoff"""
        context = context or {}
        
        for attempt in range(max_retries + 1):
            try:
                return func()
            except Exception as e:
                if attempt == max_retries:
                    # Final attempt failed
                    raise NetworkError(
                        f"Operation failed after {max_retries} retries",
                        details={
                            "last_error": str(e),
                            "attempts": attempt + 1,
                            "context": context
                        }
                    )
                
                delay = base_delay * (2 ** attempt)
                self.logger.warning(
                    f"Attempt {attempt + 1} failed, retrying in {delay}s: {str(e)}"
                )
                time.sleep(delay)

# Global error handler instance
error_handler = ErrorHandler()