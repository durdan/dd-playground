import { StateGraph, START, END } from "@langchain/langgraph"
import { BaseMessage, HumanMessage } from "@langchain/core/messages"
import { ChatOpenAI } from "@langchain/openai"

// Define the state interface for our graph
interface GraphStateType {
  messages: BaseMessage[]
  requirements: string
  planOutput: string
  devOutput: string
  reviewOutput: string
  currentStage: string
  errors: string[]
}

export class LangGraphSDLCPipeline {
  private llm: ChatOpenAI
  private graph: StateGraph<GraphStateType>
  private onUpdate?: (stage: string, status: string, content?: string) => void

  constructor(onUpdate?: (stage: string, status: string, content?: string) => void) {
    this.onUpdate = onUpdate
    this.llm = new ChatOpenAI({
      modelName: "gpt-4o-mini",
      temperature: 0.7,
      streaming: true, // Enable streaming
    })
    
    this.graph = this.createGraph()
  }

  private createGraph(): StateGraph<GraphStateType> {
    const graph = new StateGraph<GraphStateType>({
      channels: {
        messages: {
          value: (prev: BaseMessage[], next: BaseMessage[]) => prev.concat(next),
          default: () => []
        },
        requirements: {
          value: (prev: string, next: string) => next || prev,
          default: () => ""
        },
        planOutput: {
          value: (prev: string, next: string) => next || prev,
          default: () => ""
        },
        devOutput: {
          value: (prev: string, next: string) => next || prev,
          default: () => ""
        },
        reviewOutput: {
          value: (prev: string, next: string) => next || prev,
          default: () => ""
        },
        currentStage: {
          value: (prev: string, next: string) => next || prev,
          default: () => "planning"
        },
        errors: {
          value: (prev: string[], next: string[]) => prev.concat(next),
          default: () => []
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

  private async planningNode(state: GraphStateType): Promise<Partial<GraphStateType>> {
    this.onUpdate?.("planning", "running")
    
    const prompt = `You are a senior software architect. Analyze the following requirements and create a detailed development plan:

Requirements: ${state.requirements}

Provide a comprehensive plan including:
1. System architecture overview
2. Key components and their responsibilities  
3. Technology stack recommendations
4. Implementation phases
5. Potential challenges and solutions

Format your response in clear sections with bullet points.`

    try {
      let content = ""
      const stream = await this.llm.stream([new HumanMessage(prompt)])
      
      for await (const chunk of stream) {
        if (chunk.content) {
          content += chunk.content
          // Send partial updates during streaming
          this.onUpdate?.("planning", "streaming", content)
        }
      }

      this.onUpdate?.("planning", "completed", content)
      
      return {
        planOutput: content,
        currentStage: "development",
        messages: [...state.messages, new HumanMessage(prompt)]
      }
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : "Planning failed"
      this.onUpdate?.("planning", "error", errorMsg)
      return {
        errors: [...state.errors, errorMsg],
        currentStage: "failed"
      }
    }
  }

  private async developmentNode(state: GraphStateType): Promise<Partial<GraphStateType>> {
    this.onUpdate?.("development", "running")

    const prompt = `You are a senior full-stack developer. Based on the following plan, generate production-ready code:

Original Requirements: ${state.requirements}

Development Plan:
${state.planOutput}

Generate:
1. API endpoint implementations
2. Database schema/models
3. Core business logic
4. Error handling
5. Basic tests

Provide clean, well-documented code with proper error handling.`

    try {
      let content = ""
      const stream = await this.llm.stream([new HumanMessage(prompt)])
      
      for await (const chunk of stream) {
        if (chunk.content) {
          content += chunk.content
          this.onUpdate?.("development", "streaming", content)
        }
      }

      this.onUpdate?.("development", "completed", content)
      
      return {
        devOutput: content,
        currentStage: "review",
        messages: [...state.messages, new HumanMessage(prompt)]
      }
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : "Development failed"
      this.onUpdate?.("development", "error", errorMsg)
      return {
        errors: [...state.errors, errorMsg],
        currentStage: "failed"
      }
    }
  }

  private async reviewNode(state: GraphStateType): Promise<Partial<GraphStateType>> {
    this.onUpdate?.("review", "running")

    const prompt = `You are a senior code reviewer and security expert. Review the following implementation:

Original Requirements: ${state.requirements}

Generated Code:
${state.devOutput}

Provide a comprehensive code review including:
1. Code quality assessment
2. Security vulnerabilities
3. Performance considerations
4. Best practices compliance
5. Specific improvement recommendations
6. Testing completeness

Give specific, actionable feedback.`

    try {
      let content = ""
      const stream = await this.llm.stream([new HumanMessage(prompt)])
      
      for await (const chunk of stream) {
        if (chunk.content) {
          content += chunk.content
          this.onUpdate?.("review", "streaming", content)
        }
      }

      this.onUpdate?.("review", "completed", content)
      
      return {
        reviewOutput: content,
        currentStage: "completed",
        messages: [...state.messages, new HumanMessage(prompt)]
      }
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : "Review failed"
      this.onUpdate?.("review", "error", errorMsg)
      return {
        errors: [...state.errors, errorMsg],
        currentStage: "failed"
      }
    }
  }

  async execute(requirements: string): Promise<GraphStateType> {
    const initialState: GraphStateType = {
      messages: [],
      requirements,
      planOutput: "",
      devOutput: "",
      reviewOutput: "",
      currentStage: "planning",
      errors: []
    }

    this.onUpdate?.("start", "completed")
    
    try {
      const compiledGraph = this.graph.compile()
      const result = await compiledGraph.invoke(initialState)
      
      this.onUpdate?.("pipeline", "completed", "All stages completed successfully!")
      return result
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : "Pipeline execution failed"
      this.onUpdate?.("pipeline", "error", errorMsg)
      throw error
    }
  }
}