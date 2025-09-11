import re
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class DiagramType(Enum):
    FLOWCHART = "flowchart"
    GRAPH = "graph"
    SEQUENCE = "sequenceDiagram"
    CLASS = "classDiagram"

class NodeShape(Enum):
    RECTANGLE = "rectangle"
    ROUNDED = "rounded"
    CIRCLE = "circle"
    RHOMBUS = "rhombus"
    HEXAGON = "hexagon"

@dataclass
class DiagramNode:
    id: str
    label: str
    shape: NodeShape = NodeShape.RECTANGLE

@dataclass
class DiagramEdge:
    from_node: str
    to_node: str
    label: Optional[str] = None
    arrow_type: str = "-->"

@dataclass
class MermaidDiagram:
    diagram_type: DiagramType
    direction: Optional[str] = None
    nodes: List[DiagramNode] = None
    edges: List[DiagramEdge] = None
    
    def __post_init__(self):
        if self.nodes is None:
            self.nodes = []
        if self.edges is None:
            self.edges = []

class MermaidParseError(Exception):
    """Custom exception for Mermaid parsing errors"""
    pass

class MermaidParser:
    def __init__(self):
        self.node_shapes = {
            '[]': NodeShape.RECTANGLE,
            '()': NodeShape.ROUNDED,
            '(())': NodeShape.CIRCLE,
            '{}': NodeShape.RHOMBUS,
            '{{}}': NodeShape.HEXAGON
        }
        
    def parse(self, mermaid_text: str) -> MermaidDiagram:
        """Parse Mermaid diagram text into structured data"""
        if not mermaid_text or not mermaid_text.strip():
            raise MermaidParseError("Empty input provided")
            
        lines = self._clean_lines(mermaid_text)
        if not lines:
            raise MermaidParseError("No valid content found")
            
        diagram_type, direction = self._parse_header(lines[0])
        diagram = MermaidDiagram(diagram_type=diagram_type, direction=direction)
        
        for line in lines[1:]:
            if self._is_node_definition(line):
                node = self._parse_node(line)
                if not self._node_exists(diagram.nodes, node.id):
                    diagram.nodes.append(node)
            elif self._is_edge_definition(line):
                edge = self._parse_edge(line)
                diagram.edges.append(edge)
                # Add nodes if they don't exist
                self._ensure_nodes_exist(diagram, edge)
                
        return diagram
    
    def _clean_lines(self, text: str) -> List[str]:
        """Clean and filter input lines"""
        lines = []
        for line in text.split('\n'):
            line = line.strip()
            if line and not line.startswith('%%'):  # Skip comments
                lines.append(line)
        return lines
    
    def _parse_header(self, header_line: str) -> Tuple[DiagramType, Optional[str]]:
        """Parse diagram type and direction from header"""
        header_line = header_line.strip()
        
        # Match patterns like "flowchart TD", "graph LR", "sequenceDiagram"
        patterns = [
            r'^(flowchart|graph)\s+([A-Z]{2})$',
            r'^(sequenceDiagram|classDiagram)$'
        ]
        
        for pattern in patterns:
            match = re.match(pattern, header_line)
            if match:
                diagram_type_str = match.group(1)
                direction = match.group(2) if len(match.groups()) > 1 else None
                
                try:
                    diagram_type = DiagramType(diagram_type_str)
                    return diagram_type, direction
                except ValueError:
                    pass
        
        raise MermaidParseError(f"Invalid diagram header: {header_line}")
    
    def _is_node_definition(self, line: str) -> bool:
        """Check if line defines a standalone node"""
        # Pattern: nodeId[label] or nodeId(label) etc.
        return bool(re.match(r'^\s*\w+[\[\(\{].*[\]\)\}]\s*$', line))
    
    def _is_edge_definition(self, line: str) -> bool:
        """Check if line defines an edge/connection"""
        # Pattern: nodeA --> nodeB or nodeA[label] --> nodeB[label]
        return bool(re.search(r'--[>-]|==>', line))
    
    def _parse_node(self, line: str) -> DiagramNode:
        """Parse a node definition"""
        line = line.strip()
        
        # Extract node ID and content
        match = re.match(r'^(\w+)([\[\(\{].*[\]\)\}])$', line)
        if not match:
            raise MermaidParseError(f"Invalid node syntax: {line}")
            
        node_id = match.group(1)
        content_with_brackets = match.group(2)
        
        # Determine shape and extract label
        shape = self._determine_shape(content_with_brackets)
        label = self._extract_label(content_with_brackets)
        
        return DiagramNode(id=node_id, label=label, shape=shape)
    
    def _parse_edge(self, line: str) -> DiagramEdge:
        """Parse an edge definition"""
        line = line.strip()
        
        # Pattern: from_node --> to_node or from_node[label] --> to_node[label]
        # Also handle edge labels: from_node -->|label| to_node
        
        # First, extract edge label if present
        edge_label = None
        edge_label_match = re.search(r'\|([^|]+)\|', line)
        if edge_label_match:
            edge_label = edge_label_match.group(1)
            line = re.sub(r'\|[^|]+\|', '', line)  # Remove label from line
        
        # Find arrow pattern
        arrow_match = re.search(r'(--[>-]|==>)', line)
        if not arrow_match:
            raise MermaidParseError(f"No valid arrow found in: {line}")
            
        arrow_type = arrow_match.group(1)
        arrow_pos = arrow_match.start()
        
        # Split by arrow
        from_part = line[:arrow_pos].strip()
        to_part = line[arrow_match.end():].strip()
        
        # Extract node IDs (handle both simple IDs and node definitions)
        from_node = self._extract_node_id(from_part)
        to_node = self._extract_node_id(to_part)
        
        return DiagramEdge(
            from_node=from_node,
            to_node=to_node,
            label=edge_label,
            arrow_type=arrow_type
        )
    
    def _extract_node_id(self, node_part: str) -> str:
        """Extract node ID from node part (handles both 'nodeId' and 'nodeId[label]')"""
        match = re.match(r'^(\w+)', node_part.strip())
        if not match:
            raise MermaidParseError(f"Invalid node reference: {node_part}")
        return match.group(1)
    
    def _determine_shape(self, content_with_brackets: str) -> NodeShape:
        """Determine node shape from bracket style"""
        for brackets, shape in self.node_shapes.items():
            if content_with_brackets.startswith(brackets[0]) and content_with_brackets.endswith(brackets[-1]):
                return shape
        return NodeShape.RECTANGLE
    
    def _extract_label(self, content_with_brackets: str) -> str:
        """Extract label from bracketed content"""
        # Remove outer brackets
        if len(content_with_brackets) >= 2:
            # Handle different bracket types
            if content_with_brackets.startswith('((') and content_with_brackets.endswith('))'):
                return content_with_brackets[2:-2]
            elif content_with_brackets.startswith('{{') and content_with_brackets.endswith('}}'):
                return content_with_brackets[2:-2]
            else:
                return content_with_brackets[1:-1]
        return content_with_brackets
    
    def _node_exists(self, nodes: List[DiagramNode], node_id: str) -> bool:
        """Check if node with given ID already exists"""
        return any(node.id == node_id for node in nodes)
    
    def _ensure_nodes_exist(self, diagram: MermaidDiagram, edge: DiagramEdge):
        """Ensure both nodes in edge exist in diagram"""
        for node_id in [edge.from_node, edge.to_node]:
            if not self._node_exists(diagram.nodes, node_id):
                diagram.nodes.append(DiagramNode(id=node_id, label=node_id))