import { Token, TokenType, LexerOptions, Position } from './types';

export class Lexer {
  private input: string;
  private position: number;
  private line: number;
  private column: number;
  private options: LexerOptions;
  
  private keywords = new Map<string, TokenType>([
    ['flowchart', TokenType.FLOWCHART],
    ['graph', TokenType.GRAPH],
    ['sequenceDiagram', TokenType.SEQUENCEDIAGRAM],
    ['classDiagram', TokenType.CLASSIAGRAM],
    ['stateDiagram', TokenType.STATEDIAGRAM],
    ['erDiagram', TokenType.ERDIAGRAM],
    ['journey', TokenType.JOURNEY],
    ['gantt', TokenType.GANTT],
    ['pie', TokenType.PIE],
    ['gitGraph', TokenType.GITGRAPH],
    ['mindmap', TokenType.MINDMAP],
    ['subgraph', TokenType.SUBGRAPH],
    ['end', TokenType.END],
    ['TD', TokenType.DIRECTION],
    ['TB', TokenType.DIRECTION],
    ['BT', TokenType.DIRECTION],
    ['RL', TokenType.DIRECTION],
    ['LR', TokenType.DIRECTION]
  ]);

  private arrowPatterns = [
    { pattern: /^-->/, type: TokenType.SOLID_ARROW },
    { pattern: /^-.->/, type: TokenType.DASHED_ARROW },
    { pattern: /^==>/, type: TokenType.THICK_ARROW },
    { pattern: /^..>/, type: TokenType.DOTTED_ARROW },
    { pattern: /^---/, type: TokenType.ARROW },
    { pattern: /^-\.-/, type: TokenType.ARROW },
    { pattern: /^===/, type: TokenType.ARROW },
    { pattern: /^\.\.\./, type: TokenType.ARROW }
  ];

  private nodeShapePatterns = [
    { pattern: /^\[([^\]]*)\]/, type: TokenType.RECT_NODE },
    { pattern: /^\(([^\)]*)\)/, type: TokenType.ROUND_NODE },
    { pattern: /^\(\(([^\)]*)\)\)/, type: TokenType.CIRCLE_NODE },
    { pattern: /^>([^<]*)]/, type: TokenType.ASYMMETRIC_NODE },
    { pattern: /^\{([^\}]*)\}/, type: TokenType.RHOMBUS_NODE },
    { pattern: /^\{\{([^\}]*)\}\}/, type: TokenType.HEXAGON_NODE },
    { pattern: /^\/([^\\]*)\\//, type: TokenType.PARALLELOGRAM_NODE },
    { pattern: /^\\([^\/]*)\//,  type: TokenType.TRAPEZOID_NODE },
    { pattern: /^\[\[([^\]]*)\]\]/, type: TokenType.SUBROUTINE_NODE }
  ];

  constructor(input: string, options: LexerOptions = {}) {
    this.input = input;
    this.position = 0;
    this.line = 1;
    this.column = 1;
    this.options = {
      skipWhitespace: options.skipWhitespace ?? false,
      skipComments: options.skipComments ?? false,
      preserveNewlines: options.preserveNewlines ?? true
    };
  }

  tokenize(): Token[] {
    const tokens: Token[] = [];
    
    while (!this.isEOF()) {
      const token = this.nextToken();
      
      if (token.type === TokenType.WHITESPACE && this.options.skipWhitespace) {
        continue;
      }
      
      if (token.type === TokenType.COMMENT && this.options.skipComments) {
        continue;
      }
      
      if (token.type === TokenType.NEWLINE && !this.options.preserveNewlines) {
        continue;
      }
      
      tokens.push(token);
    }
    
    tokens.push(this.createToken(TokenType.EOF, ''));
    return tokens;
  }

  private nextToken(): Token {
    this.skipWhitespace();
    
    if (this.isEOF()) {
      return this.createToken(TokenType.EOF, '');
    }

    const char = this.currentChar();
    
    // Comments
    if (char === '%' && this.peek() === '%') {
      return this.readComment();
    }

    // Newlines
    if (char === '\n') {
      return this.readNewline();
    }

    // Numbers
    if (this.isDigit(char)) {
      return this.readNumber();
    }

    // String literals
    if (char === '"' || char === "'") {
      return this.readString();
    }

    // Arrow patterns (check before single characters)
    for (const { pattern, type } of this.arrowPatterns) {
      const match = this.input.slice(this.position).match(pattern);
      if (match) {
        const value = match[0];
        const token = this.createToken(type, value);
        this.advance(value.length);
        return token;
      }
    }

    // Node shape patterns
    for (const { pattern, type } of this.nodeShapePatterns) {
      const match = this.input.slice(this.position).match(pattern);
      if (match) {
        const value = match[0];
        const token = this.createToken(type, value);
        this.advance(value.length);
        return token;
      }
    }

    // Single character tokens
    switch (char) {
      case '(':
        return this.readSingleChar(TokenType.LPAREN);
      case ')':
        return this.readSingleChar(TokenType.RPAREN);
      case '[':
        return this.readSingleChar(TokenType.LBRACKET);
      case ']':
        return this.readSingleChar(TokenType.RBRACKET);
      case '{':
        return this.readSingleChar(TokenType.LBRACE);
      case '}':
        return this.readSingleChar(TokenType.RBRACE);
      case '|':
        return this.readSingleChar(TokenType.PIPE);
      case ';':
        return this.readSingleChar(TokenType.SEMICOLON);
      case ':':
        return this.readSingleChar(TokenType.COLON);
      case '#':
        return this.readSingleChar(TokenType.HASH);
      case '$':
        return this.readSingleChar(TokenType.DOLLAR);
      case '@':
        return this.readSingleChar(TokenType.AT);
      case '&':
        return this.readSingleChar(TokenType.AMPERSAND);
      case '%':
        return this.readSingleChar(TokenType.PERCENT);
      case '-':
        if (this.peek() === '-') {
          return this.readArrow();
        }
        return this.readSingleChar(TokenType.ARROW);
      case '=':
        if (this.peek() === '=') {
          return this.readArrow();
        }
        return this.createToken(TokenType.ERROR, char);
      case '.':
        if (this.peek() === '.') {
          return this.readArrow();
        }
        return this.createToken(TokenType.ERROR, char);
      default:
        // Identifiers and keywords
        if (this.isAlpha(char) || char === '_') {
          return this.readIdentifier();
        }
        
        // Whitespace
        if (this.isWhitespace(char)) {
          return this.readWhitespace();
        }
        
        // Unknown character
        return this.readSingleChar(TokenType.ERROR);
    }
  }

  private readComment(): Token {
    const start = this.position;
    this.advance(2); // Skip '%%'
    
    while (!this.isEOF() && this.currentChar() !== '\n') {
      this.advance();
    }
    
    const value = this.input.slice(start, this.position);
    return this.createToken(TokenType.COMMENT, value);
  }

  private readNewline(): Token {
    const token = this.createToken(TokenType.NEWLINE, '\n');
    this.advance();
    this.line++;
    this.column = 1;
    return token;
  }

  private readNumber(): Token {
    const start = this.position;
    
    while (!this.isEOF() && (this.isDigit(this.currentChar()) || this.currentChar() === '.')) {
      this.advance();
    }
    
    const value = this.input.slice(start, this.position);
    return this.createToken(TokenType.NUMBER, value);
  }

  private readString(): Token {
    const quote = this.currentChar();
    const start = this.position;
    this.advance(); // Skip opening quote
    
    while (!this.isEOF() && this.currentChar() !== quote) {
      if (this.currentChar() === '\\') {
        this.advance(); // Skip escape character
        if (!this.isEOF()) {
          this.advance(); // Skip escaped character
        }
      } else {
        this.advance();
      }
    }
    
    if (!this.isEOF()) {
      this.advance(); // Skip closing quote
    }
    
    const value = this.input.slice(start, this.position);
    return this.createToken(TokenType.STRING, value);
  }

  private readArrow(): Token {
    const start = this.position;
    const char = this.currentChar();
    
    if (char === '-') {
      this.advance();
      if (this.currentChar() === '-') {
        this.advance();
        if (this.currentChar() === '>') {
          this.advance();
          return this.createToken(TokenType.SOLID_ARROW, '-->');
        }
        return this.createToken(TokenType.ARROW, '--');
      }
      if (this.currentChar() === '.') {
        this.advance();
        if (this.currentChar() === '-') {
          this.advance();
          if (this.currentChar() === '>') {
            this.advance();
            return this.createToken(TokenType.DASHED_ARROW, '-.->');
          }
          return this.createToken(TokenType.ARROW, '-.-');
        }
      }
    } else if (char === '=') {
      this.advance();
      if (this.currentChar() === '=') {
        this.advance();
        if (this.currentChar() === '>') {
          this.advance();
          return this.createToken(TokenType.THICK_ARROW, '==>');
        }
        return this.createToken(TokenType.ARROW, '==');
      }
    } else if (char === '.') {
      this.advance();
      if (this.currentChar() === '.') {
        this.advance();
        if (this.currentChar() === '>') {
          this.advance();
          return this.createToken(TokenType.DOTTED_ARROW, '..>');
        }
        if (this.currentChar() === '.') {
          this.advance();
          return this.createToken(TokenType.ARROW, '...');
        }
        return this.createToken(TokenType.ARROW, '..');
      }
    }
    
    const value = this.input.slice(start, this.position);
    return this.createToken(TokenType.ARROW, value);
  }

  private readIdentifier(): Token {
    const start = this.position;
    
    while (!this.isEOF() && (this.isAlphaNumeric(this.currentChar()) || this.currentChar() === '_' || this.currentChar() === '-')) {
      this.advance();
    }
    
    const value = this.input.slice(start, this.position);
    const tokenType = this.keywords.get(value) || TokenType.IDENTIFIER;
    return this.createToken(tokenType, value);
  }

  private readWhitespace(): Token {
    const start = this.position;
    
    while (!this.isEOF() && this.isWhitespace(this.currentChar()) && this.currentChar() !== '\n') {
      this.advance();
    }
    
    const value = this.input.slice(start, this.position);
    return this.createToken(TokenType.WHITESPACE, value);
  }

  private readSingleChar(tokenType: TokenType): Token {
    const char = this.currentChar();
    this.advance();
    return this.createToken(tokenType, char);
  }

  private createToken(type: TokenType, value: string): Token {
    return {
      type,
      value,
      line: this.line,
      column: this.column - value.length,
      position: this.position - value.length
    };
  }

  private currentChar(): string {
    return this.input[this.position] || '';
  }

  private peek(offset = 1): string {
    return this.input[this.position + offset] || '';
  }

  private advance(count = 1): void {
    for (let i = 0; i < count; i++) {
      if (this.position < this.input.length) {
        if (this.input[this.position] === '\n') {
          this.line++;
          this.column = 1;
        } else {
          this.column++;
        }
        this.position++;
      }
    }
  }

  private skipWhitespace(): void {
    if (this.options.skipWhitespace) {
      while (!this.isEOF() && this.isWhitespace(this.currentChar()) && this.currentChar() !== '\n') {
        this.advance();
      }
    }
  }

  private isEOF(): boolean {
    return this.position >= this.input.length;
  }

  private isDigit(char: string): boolean {
    return char >= '0' && char <= '9';
  }

  private isAlpha(char: string): boolean {
    return (char >= 'a' && char <= 'z') || (char >= 'A' && char <= 'Z');
  }

  private isAlphaNumeric(char: string): boolean {
    return this.isAlpha(char) || this.isDigit(char);
  }

  private isWhitespace(char: string): boolean {
    return char === ' ' || char === '\t' || char === '\r';
  }
}