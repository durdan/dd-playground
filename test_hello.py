#!/usr/bin/env python3
import unittest
import os
import tempfile
from unittest.mock import patch, mock_open
from test import read_and_print_hello

class TestHello(unittest.TestCase):
    
    def test_read_and_print_existing_file(self):
        """Test reading and printing from an existing file."""
        with patch('builtins.open', mock_open(read_data='Hello from Claude CLI with native tools!')):
            with patch('builtins.print') as mock_print:
                read_and_print_hello()
                mock_print.assert_called_once_with('Hello from Claude CLI with native tools!')
    
    def test_file_not_found(self):
        """Test handling when hello.txt doesn't exist."""
        with patch('builtins.open', side_effect=FileNotFoundError):
            with patch('builtins.print') as mock_print:
                read_and_print_hello()
                mock_print.assert_called_once_with("Error: hello.txt file not found")
    
    def test_other_exception(self):
        """Test handling of other file reading errors."""
        with patch('builtins.open', side_effect=PermissionError("Permission denied")):
            with patch('builtins.print') as mock_print:
                read_and_print_hello()
                mock_print.assert_called_once_with("Error reading file: Permission denied")

if __name__ == "__main__":
    unittest.main()