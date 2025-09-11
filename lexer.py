import re
from enum import Enum
from dataclasses import dataclass
from typing import List, Iterator, Optional

class TokenType(Enum):
    GRAPH = "graph"
    FLOWCHART = "flowchart"
    DIRECTION = "direction"
    NODE = "node"
    EDGE = "edge"
    IDENTIFIER = "identifier"
    STRING = "string"
    ARROW = "arrow"
    BRACKET_OPEN = "bracket_open"
    BRACKET_CLOSE = "bracket_close"
    NEWLINE = "newline"
    EOF = "eof"
    INVALID = "invalid"

@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int

class MermaidLexer:
    """Tokenizes mermaid diagram syntax."""
    
    KEYWORDS = {
        'graph', 'flowchart', 'TD', 'TB', 'BT', 'RL', 'LR'
    }
    
    ARROWS = {
        '-->': 'solid',
        '-.->': 'dotted',
        '==>': 'thick',
        '--': 'line',
        '-.': 'dotted_line'
    }
    
    def __init__(self, text: str):
        if not isinstance(text, str):
            raise ValueError("Input must be a string")
        self.text = text
        self.position = 0
        self.line = 1
        self.column = 1
        
    def tokenize(self) -> List[Token]:
        """Tokenize the input text into a list of tokens."""
        tokens = []
        
        while self.position < len(self.text):
            token = self._next_token()
            if token:
                tokens.append(token)
                
        tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return tokens
    
    def _next_token(self) -> Optional[Token]:
        """Get the next token from the input."""
        self._skip_whitespace()
        
        if self.position >= len(self.text):
            return None
            
        start_line, start_col = self.line, self.column
        
        # Handle newlines
        if self._current_char() == '\n':
            self._advance()
            return Token(TokenType.NEWLINE, '\n', start_line, start_col)
        
        # Handle comments
        if self._current_char() == '%' and self._peek() == '%':
            self._skip_comment()
            return self._next_token()
        
        # Handle arrows
        arrow_token = self._try_arrow()
        if arrow_token:
            return arrow_token
            
        # Handle brackets
        if self._current_char() in '()[]{}':
            char = self._current_char()
            self._advance()
            token_type = TokenType.BRACKET_OPEN if char in '([{' else TokenType.BRACKET_CLOSE
            return Token(token_type, char, start_line, start_col)
        
        # Handle strings (quoted)
        if self._current_char() in '"\'':
            return self._read_string()
        
        # Handle identifiers and keywords
        if self._current_char().isalnum() or self._current_char() in '_-':
            return self._read_identifier()
        
        # Invalid character
        char = self._current_char()
        self._advance()
        return Token(TokenType.INVALID, char, start_line, start_col)
    
    def _current_char(self) -> str:
        """Get current character or empty string if at end."""
        return self.text[self.position] if self.position < len(self.text) else ''
    
    def _peek(self, offset: int = 1) -> str:
        """Peek at character ahead."""
        pos = self.position + offset
        return self.text[pos] if pos < len(self.text) else ''
    
    def _advance(self):
        """Move to next character."""
        if self.position < len(self.text):
            if self.text[self.position] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.position += 1
    
    def _skip_whitespace(self):
        """Skip whitespace except newlines."""
        while self._current_char() in ' \t\r':
            self._advance()
    
    def _skip_comment(self):
        """Skip comment line."""
        while self._current_char() and self._current_char() != '\n':
            self._advance()
    
    def _try_arrow(self) -> Optional[Token]:
        """Try to match arrow patterns."""
        start_line, start_col = self.line, self.column
        
        for arrow, arrow_type in self.ARROWS.items():
            if self.text[self.position:].startswith(arrow):
                for _ in range(len(arrow)):
                    self._advance()
                return Token(TokenType.ARROW, arrow, start_line, start_col)
        return None
    
    def _read_string(self) -> Token:
        """Read quoted string."""
        start_line, start_col = self.line, self.column
        quote_char = self._current_char()
        self._advance()  # Skip opening quote
        
        value = ""
        while self._current_char() and self._current_char() != quote_char:
            if self._current_char() == '\\':
                self._advance()
                if self._current_char():
                    value += self._current_char()
                    self._advance()
            else:
                value += self._current_char()
                self._advance()
        
        if self._current_char() == quote_char:
            self._advance()  # Skip closing quote
            
        return Token(TokenType.STRING, value, start_line, start_col)
    
    def _read_identifier(self) -> Token:
        """Read identifier or keyword."""
        start_line, start_col = self.line, self.column
        value = ""
        
        while (self._current_char().isalnum() or 
               self._current_char() in '_-'):
            value += self._current_char()
            self._advance()
        
        # Determine token type
        if value in self.KEYWORDS:
            if value in ('graph', 'flowchart'):
                token_type = TokenType.GRAPH
            elif value in ('TD', 'TB', 'BT', 'RL', 'LR'):
                token_type = TokenType.DIRECTION
            else:
                token_type = TokenType.IDENTIFIER
        else:
            token_type = TokenType.IDENTIFIER
            
        return Token(token_type, value, start_line, start_col)