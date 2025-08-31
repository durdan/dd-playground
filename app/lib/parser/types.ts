export enum TokenType {
  // Core tokens
  IDENTIFIER = 'IDENTIFIER',
  STRING = 'STRING',
  NUMBER = 'NUMBER',
  ARROW = 'ARROW',
  SEMICOLON = 'SEMICOLON',
  COLON = 'COLON',
  NEWLINE = 'NEWLINE',
  WHITESPACE = 'WHITESPACE',
  COMMENT = 'COMMENT',
  
  // Mermaid diagram types
  FLOWCHART = 'FLOWCHART',
  SEQUENCEDIAGRAM = 'SEQUENCEDIAGRAM',
  GANTT = 'GANTT',
  CLASSIAGRAM = 'CLASSIAGRAM',
  STATEDIAGRAM = 'STATEDIAGRAM',
  ERDIAGRAM = 'ERDIAGRAM',
  JOURNEY = 'JOURNEY',
  GITGRAPH = 'GITGRAPH',
  PIE = 'PIE',
  MINDMAP = 'MINDMAP',
  
  // Flowchart specific
  GRAPH = 'GRAPH',
  SUBGRAPH = 'SUBGRAPH',
  END = 'END',
  DIRECTION = 'DIRECTION',
  
  // Node shapes
  RECT_NODE = 'RECT_NODE',
  ROUND_NODE = 'ROUND_NODE',
  CIRCLE_NODE = 'CIRCLE_NODE',
  ASYMMETRIC_NODE = 'ASYMMETRIC_NODE',
  RHOMBUS_NODE = 'RHOMBUS_NODE',
  HEXAGON_NODE = 'HEXAGON_NODE',
  PARALLELOGRAM_NODE = 'PARALLELOGRAM_NODE',
  TRAPEZOID_NODE = 'TRAPEZOID_NODE',
  SUBROUTINE_NODE = 'SUBROUTINE_NODE',
  
  // Arrows and connections
  SOLID_ARROW = 'SOLID_ARROW',
  DASHED_ARROW = 'DASHED_ARROW',
  THICK_ARROW = 'THICK_ARROW',
  DOTTED_ARROW = 'DOTTED_ARROW',
  
  // Brackets and delimiters
  LPAREN = 'LPAREN',
  RPAREN = 'RPAREN',
  LBRACKET = 'LBRACKET',
  RBRACKET = 'RBRACKET',
  LBRACE = 'LBRACE',
  RBRACE = 'RBRACE',
  PIPE = 'PIPE',
  
  // Special characters
  PERCENT = 'PERCENT',
  HASH = 'HASH',
  DOLLAR = 'DOLLAR',
  AT = 'AT',
  AMPERSAND = 'AMPERSAND',
  
  // End of file
  EOF = 'EOF',
  
  // Error token
  ERROR = 'ERROR'
}

export interface Token {
  type: TokenType;
  value: string;
  line: number;
  column: number;
  position: number;
}

export interface Position {
  line: number;
  column: number;
  index: number;
}

export enum NodeType {
  PROGRAM = 'PROGRAM',
  DIAGRAM = 'DIAGRAM',
  FLOWCHART = 'FLOWCHART',
  SEQUENCE_DIAGRAM = 'SEQUENCE_DIAGRAM',
  CLASS_DIAGRAM = 'CLASS_DIAGRAM',
  STATE_DIAGRAM = 'STATE_DIAGRAM',
  ER_DIAGRAM = 'ER_DIAGRAM',
  GANTT_DIAGRAM = 'GANTT_DIAGRAM',
  PIE_DIAGRAM = 'PIE_DIAGRAM',
  JOURNEY_DIAGRAM = 'JOURNEY_DIAGRAM',
  GITGRAPH_DIAGRAM = 'GITGRAPH_DIAGRAM',
  MINDMAP_DIAGRAM = 'MINDMAP_DIAGRAM',
  
  NODE = 'NODE',
  EDGE = 'EDGE',
  SUBGRAPH = 'SUBGRAPH',
  DIRECTIVE = 'DIRECTIVE',
  PROPERTY = 'PROPERTY',
  IDENTIFIER = 'IDENTIFIER',
  LITERAL = 'LITERAL'
}

export interface ASTNode {
  type: NodeType;
  position: Position;
  children?: ASTNode[];
  value?: string;
  properties?: Record<string, any>;
}

export interface DiagramNode extends ASTNode {
  diagramType: string;
  direction?: string;
  title?: string;
  nodes: NodeDefinition[];
  edges: EdgeDefinition[];
  subgraphs?: SubgraphDefinition[];
}

export interface NodeDefinition {
  id: string;
  label: string;
  shape: string;
  classes?: string[];
  styles?: Record<string, string>;
  position?: Position;
}

export interface EdgeDefinition {
  from: string;
  to: string;
  label?: string;
  type: string;
  classes?: string[];
  styles?: Record<string, string>;
  position?: Position;
}

export interface SubgraphDefinition {
  id: string;
  title: string;
  nodes: string[];
  direction?: string;
  position?: Position;
}

export enum ValidationSeverity {
  ERROR = 'ERROR',
  WARNING = 'WARNING',
  INFO = 'INFO'
}

export interface ValidationError {
  severity: ValidationSeverity;
  message: string;
  position: Position;
  code: string;
  suggestions?: string[];
}

export interface ParseResult {
  ast: ASTNode | null;
  errors: ValidationError[];
  warnings: ValidationError[];
}

export interface LexerOptions {
  skipWhitespace?: boolean;
  skipComments?: boolean;
  preserveNewlines?: boolean;
}

export interface ParserOptions {
  strict?: boolean;
  allowRecovery?: boolean;
  maxErrors?: number;
}

export interface ValidatorOptions {
  checkSyntax?: boolean;
  checkSemantics?: boolean;
  checkStyles?: boolean;
}

export interface TransformOptions {
  optimizeNodes?: boolean;
  optimizeEdges?: boolean;
  removeUnused?: boolean;
  sortElements?: boolean;
}

export interface TransformResult {
  ast: ASTNode;
  optimizations: string[];
  removedElements: string[];
}

export type DiagramType = 
  | 'flowchart'
  | 'sequence'
  | 'class'
  | 'state'
  | 'er'
  | 'gantt'
  | 'pie'
  | 'journey'
  | 'gitgraph'
  | 'mindmap';

export interface ParserEngine {
  tokenize(input: string, options?: LexerOptions): Token[];
  parse(tokens: Token[], options?: ParserOptions): ParseResult;
  validate(ast: ASTNode, options?: ValidatorOptions): ValidationError[];
  transform(ast: ASTNode, options?: TransformOptions): TransformResult;
  parseString(input: string): ParseResult;
}