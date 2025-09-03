import { NodeInput, NodeOutput, SDLCState } from '../types'
import { chatComplete } from '../../llm'

export class DevelopmentNode {
  static async execute(input: NodeInput): Promise<NodeOutput> {
    const { state } = input
    
    try {
      if (!state.plan) {
        throw new Error('No plan available for development')
      }
      
      // Use real LLM to generate code based on the plan
      const developmentPrompt = [
        {
          role: 'system' as const,
          content: `You are a senior software developer with expertise in multiple programming languages and frameworks. Your role is to implement code based on detailed development plans.

When given a development plan, you should:
1. Analyze the requirements and architectural decisions
2. Write clean, maintainable, and well-documented code
3. Follow best practices and coding standards
4. Include appropriate error handling
5. Consider security and performance implications
6. Provide code that is ready for testing and review

Format your response with the actual implementation code, including file structure if multiple files are needed.`
        },
        {
          role: 'user' as const,
          content: `Please implement the code based on the following development plan:

Requirements: ${state.requirements}

Development Plan:
${state.plan}

Please provide:
- Complete implementation code
- File structure and organization
- Key implementation decisions made
- Notes for testing and deployment`
        }
      ]

      console.log('Development Node: Calling LLM for code generation...')
      const code = await chatComplete(developmentPrompt)
      console.log('Development Node: LLM response received')
      
      const updatedState: SDLCState = {
        ...state,
        code,
        status: 'reviewing',
        metadata: {
          ...state.metadata,
          developmentTimestamp: new Date().toISOString(),
          developmentAgent: 'OpenAI GPT-4o-mini'
        }
      }
      
      return {
        state: updatedState,
        output: code
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown development error'
      console.error('Development Node error:', error)
      
      return {
        state: {
          ...state,
          errors: [...state.errors, errorMessage]
        },
        output: `Development failed: ${errorMessage}`
      }
    }
  }
}