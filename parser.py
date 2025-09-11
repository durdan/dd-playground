from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from lexer import Token, TokenType, MermaidLexer

@dataclass
class Node:
    id: str
    label: str
    shape: str = "rectangle"
    
@dataclass
class Edge:
    from_node: str
    to_node: str
    label: str = ""
    style: str = "solid"

@dataclass
class Diagram:
    type: str
    direction: str
    nodes: Dict[str, Node]
    edges: List[Edge]

class ParseError(Exception):
    """Custom exception for parsing errors."""
    def __init__(self, message: str, token: Optional[Token] = None):
        self.message = message
        self.token = token
        super().__init__(self._format_message())
    
    def _format_message(self) -> str:
        if self.token:
            return f"Parse error at line {self.token.line}, column {self.token.column}: {self.message}"
        return f"Parse error: {self.message}"

class MermaidParser:
    """Parses mermaid tokens into an AST."""
    
    def __init__(self, tokens: List[Token]):
        if not tokens:
            raise ValueError("Token list cannot be empty")
        self.tokens = tokens
        self.position = 0
        self.current_token = tokens[0] if tokens else None
    
    def parse(self) -> Diagram:
        """Parse tokens into a diagram AST."""
        try:
            return self._parse_diagram()
        except IndexError:
            raise ParseError("Unexpected end of input")
    
    def _parse_diagram(self) -> Diagram:
        """Parse the main diagram structure."""
        # Parse diagram type and direction
        diagram_type, direction = self._parse_header()
        
        nodes = {}
        edges = []
        
        # Parse diagram content
        while not self._is_at_end():
            if self._current_token_is(TokenType.NEWLINE):
                self._advance()
                continue
                
            if self._current_token_is(TokenType.IDENTIFIER):
                # Could be node definition or edge
                if self._is_edge_definition():
                    edge = self._parse_edge()
                    edges.append(edge)
                    # Ensure nodes exist
                    self._ensure_node_exists(edge.from_node, nodes)
                    self._ensure_node_exists(edge.to_node, nodes)
                else:
                    node = self._parse_node()
                    nodes[node.id] = node
            else:
                self._advance()
        
        return Diagram(diagram_type, direction, nodes, edges)
    
    def _parse_header(self) -> tuple[str, str]:
        """Parse diagram type and direction."""
        if not self._current_token_is(TokenType.GRAPH):
            raise ParseError("Expected 'graph' or 'flowchart'", self.current_token)
        
        diagram_type = self.current_token.value
        self._advance()
        
        direction = "TD"  # Default direction
        if self._current_token_is(TokenType.DIRECTION):
            direction = self.current_token.value
            self._advance()
        
        return diagram_type, direction
    
    def _parse_node(self) -> Node:
        """Parse a node definition."""
        if not self._current_token_is(TokenType.IDENTIFIER):
            raise ParseError("Expected node identifier", self.current_token)
        
        node_id = self.current_token.value
        self._advance()
        
        label = node_id
        shape = "rectangle"
        
        # Check for node label and shape
        if self._current_token_is(TokenType.BRACKET_OPEN):
            bracket = self.current_token.value
            self._advance()
            
            # Determine shape from bracket type
            shape_map = {
                '[': 'rectangle',
                '(': 'rounded',
                '{': 'rhombus'
            }
            shape = shape_map.get(bracket, 'rectangle')
            
            # Parse label
            if self._current_token_is(TokenType.STRING) or self._current_token_is(TokenType.IDENTIFIER):
                label = self.current_token.value
                self._advance()
            
            # Expect closing bracket
            if self._current_token_is(TokenType.BRACKET_CLOSE):
                self._advance()
        
        return Node(node_id, label, shape)
    
    def _parse_edge(self) -> Edge:
        """Parse an edge definition."""
        if not self._current_token_is(TokenType.IDENTIFIER):
            raise ParseError("Expected source node identifier", self.current_token)
        
        from_node = self.current_token.value
        self._advance()
        
        # Parse arrow
        if not self._current_token_is(TokenType.ARROW):
            raise ParseError("Expected arrow", self.current_token)
        
        arrow = self.current_token.value
        style = self._arrow_to_style(arrow)
        self._advance()
        
        # Parse target node
        if not self._current_token_is(TokenType.IDENTIFIER):
            raise ParseError("Expected target node identifier", self.current_token)
        
        to_node = self.current_token.value
        self._advance()
        
        # Optional edge label
        label = ""
        if (self._current_token_is(TokenType.STRING) or 
            self._current_token_is(TokenType.IDENTIFIER)):
            label = self.current_token.value
            self._advance()
        
        return Edge(from_node, to_node, label, style)
    
    def _is_edge_definition(self) -> bool:
        """Check if current position starts an edge definition."""
        # Look ahead for arrow pattern: ID ARROW ID
        if (self.position + 2 < len(self.tokens) and
            self._current_token_is(TokenType.IDENTIFIER) and
            self.tokens[self.position + 1].type == TokenType.ARROW and
            self.tokens[self.position + 2].type == TokenType.IDENTIFIER):
            return True
        return False
    
    def _ensure_node_exists(self, node_id: str, nodes: Dict[str, Node]):
        """Ensure a node exists in the nodes dictionary."""
        if node_id not in nodes:
            nodes[node_id] = Node(node_id, node_id)
    
    def _arrow_to_style(self, arrow: str) -> str:
        """Convert arrow symbol to style."""
        style_map = {
            '-->': 'solid',
            '-.->': 'dotted',
            '==>': 'thick',
            '--': 'line',
            '-.': 'dotted_line'
        }
        return style_map.get(arrow, 'solid')
    
    def _current_token_is(self, token_type: TokenType) -> bool:
        """Check if current token is of given type."""
        return self.current_token and self.current_token.type == token_type
    
    def _is_at_end(self) -> bool:
        """Check if we're at the end of tokens."""
        return (self.current_token is None or 
                self.current_token.type == TokenType.EOF)
    
    def _advance(self):
        """Move to next token."""
        if self.position < len(self.tokens) - 1:
            self.position += 1
            self.current_token = self.tokens[self.position]
        else:
            self.current_token = None