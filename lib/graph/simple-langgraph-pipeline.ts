import { StateGraph, START, END } from "@langchain/langgraph"

// Simple state interface without complex dependencies
interface SimpleState {
  requirements: string
  output: string
  stage: string
}

export class SimpleLangGraphPipeline {
  private graph: StateGraph<SimpleState>
  private onUpdate?: (stage: string, status: string, content?: string) => void

  constructor(onUpdate?: (stage: string, status: string, content?: string) => void) {
    this.onUpdate = onUpdate
    this.graph = this.createGraph()
  }

  private createGraph(): StateGraph<SimpleState> {
    const graph = new StateGraph<SimpleState>({
      channels: {
        requirements: {
          value: (prev: string, next: string) => next || prev,
          default: () => ""
        },
        output: {
          value: (prev: string, next: string) => next || prev,
          default: () => ""
        },
        stage: {
          value: (prev: string, next: string) => next || prev,
          default: () => "planning"
        }
      }
    })

    // Add nodes
    graph.addNode("planning", this.planningNode.bind(this))
    graph.addNode("development", this.developmentNode.bind(this))
    graph.addNode("review", this.reviewNode.bind(this))

    // Define the flow
    graph.addEdge(START, "planning")
    graph.addEdge("planning", "development")
    graph.addEdge("development", "review")
    graph.addEdge("review", END)

    return graph
  }

  private async planningNode(state: SimpleState): Promise<Partial<SimpleState>> {
    this.onUpdate?.("planning", "running")
    
    // Simulate streaming content generation
    const content = `## Development Plan for: ${state.requirements}

1. **System Architecture Analysis**
   - Design REST API endpoints for user management
   - Define authentication and authorization mechanisms
   - Plan database schema for user data storage

2. **Technology Stack Selection**
   - Backend: Node.js with Express/Fastify
   - Database: PostgreSQL or MongoDB
   - Authentication: JWT tokens
   - Validation: Joi or Zod schemas

3. **Implementation Phases**
   - Phase 1: Basic CRUD operations
   - Phase 2: Authentication system
   - Phase 3: Role-based access control
   - Phase 4: Testing and documentation

4. **Security Considerations**
   - Password hashing with bcrypt
   - Rate limiting for API endpoints
   - Input validation and sanitization
   - HTTPS enforcement`

    // Simulate real-time streaming
    let partialContent = ""
    const lines = content.split('\n')
    
    for (let i = 0; i < lines.length; i++) {
      partialContent += lines[i] + '\n'
      this.onUpdate?.("planning", "streaming", partialContent.trim())
      await new Promise(resolve => setTimeout(resolve, 100 + Math.random() * 200))
    }

    this.onUpdate?.("planning", "completed", content)
    return { output: content, stage: "development" }
  }

  private async developmentNode(state: SimpleState): Promise<Partial<SimpleState>> {
    this.onUpdate?.("development", "running")
    
    const content = `## Generated Code Implementation

\`\`\`javascript
// User Model (MongoDB/Mongoose)
const userSchema = new mongoose.Schema({
  username: { type: String, required: true, unique: true },
  email: { type: String, required: true, unique: true },
  password: { type: String, required: true },
  role: { type: String, enum: ['user', 'admin'], default: 'user' },
  createdAt: { type: Date, default: Date.now },
  updatedAt: { type: Date, default: Date.now }
});

// API Routes
app.post('/api/users', async (req, res) => {
  try {
    const { username, email, password } = req.body;
    const hashedPassword = await bcrypt.hash(password, 10);
    const user = new User({ username, email, password: hashedPassword });
    await user.save();
    res.status(201).json({ message: 'User created successfully' });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

app.get('/api/users/:id', auth, async (req, res) => {
  try {
    const user = await User.findById(req.params.id).select('-password');
    if (!user) return res.status(404).json({ error: 'User not found' });
    res.json(user);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
\`\`\``

    // Simulate streaming
    let partialContent = ""
    const lines = content.split('\n')
    
    for (let i = 0; i < lines.length; i++) {
      partialContent += lines[i] + '\n'
      this.onUpdate?.("development", "streaming", partialContent.trim())
      await new Promise(resolve => setTimeout(resolve, 80 + Math.random() * 120))
    }

    this.onUpdate?.("development", "completed", content)
    return { output: content, stage: "review" }
  }

  private async reviewNode(state: SimpleState): Promise<Partial<SimpleState>> {
    this.onUpdate?.("review", "running")
    
    const content = `## Code Review Analysis

### ✅ Strengths
- Clean separation of concerns
- Proper password hashing with bcrypt
- Input validation and error handling
- RESTful API design principles

### ⚠️ Security Recommendations
1. **Rate Limiting**: Add express-rate-limit middleware
2. **Input Validation**: Implement Joi/Zod schemas
3. **CORS Configuration**: Set appropriate CORS headers
4. **Logging**: Add structured logging for audit trails

### 🔧 Performance Optimizations
- Add database indexing on email and username
- Implement pagination for user listings
- Consider caching for frequently accessed data
- Add connection pooling for database

### 📋 Testing Requirements
- Unit tests for all endpoints
- Integration tests for authentication flow
- Load testing for concurrent user creation
- Security testing with OWASP guidelines

**Overall Rating: 8/10** - Solid foundation with room for security enhancements.`

    // Simulate streaming
    let partialContent = ""
    const lines = content.split('\n')
    
    for (let i = 0; i < lines.length; i++) {
      partialContent += lines[i] + '\n'
      this.onUpdate?.("review", "streaming", partialContent.trim())
      await new Promise(resolve => setTimeout(resolve, 90 + Math.random() * 150))
    }

    this.onUpdate?.("review", "completed", content)
    return { output: content, stage: "completed" }
  }

  async execute(requirements: string): Promise<SimpleState> {
    const initialState: SimpleState = {
      requirements,
      output: "",
      stage: "planning"
    }

    this.onUpdate?.("start", "completed")
    
    try {
      const compiledGraph = this.graph.compile()
      const result = await compiledGraph.invoke(initialState)
      
      this.onUpdate?.("pipeline", "completed", "LangGraph pipeline execution completed!")
      return result
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : "Pipeline execution failed"
      this.onUpdate?.("pipeline", "error", errorMsg)
      throw error
    }
  }
}