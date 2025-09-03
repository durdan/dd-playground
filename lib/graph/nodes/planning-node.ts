import { NodeInput, NodeOutput, SDLCState } from '../types'
import { chatComplete } from '../../llm'

export class PlanningNode {
  static async execute(input: NodeInput): Promise<NodeOutput> {
    const { state, input: userInput } = input
    
    try {
      // Use real LLM to create development plan
      const planningPrompt = [
        {
          role: 'system' as const,
          content: `You are a senior software architect and project planning expert. Your role is to analyze requirements and create detailed, actionable development plans.

When given requirements, you should:
1. Break down the requirements into clear, specific tasks
2. Identify the architecture and technology decisions needed
3. Create a logical sequence of implementation steps
4. Consider testing, security, and deployment aspects
5. Provide clear deliverables for each phase

Format your response as a structured development plan with numbered steps and clear objectives.`
        },
        {
          role: 'user' as const,
          content: `Please create a detailed development plan for the following requirements:

Requirements: ${userInput}

Please provide a comprehensive plan that includes:
- Analysis of the requirements
- Architecture recommendations
- Implementation phases
- Testing strategy
- Deployment considerations`
        }
      ]

      console.log('Planning Node: Calling LLM for development plan...')
      const plan = await chatComplete(planningPrompt)
      console.log('Planning Node: LLM response received')
      
      const updatedState: SDLCState = {
        ...state,
        requirements: userInput,
        plan,
        status: 'developing',
        metadata: {
          ...state.metadata,
          planningTimestamp: new Date().toISOString(),
          planningAgent: 'OpenAI GPT-4o-mini'
        }
      }
      
      return {
        state: updatedState,
        output: plan
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown planning error'
      console.error('Planning Node error:', error)
      
      return {
        state: {
          ...state,
          errors: [...state.errors, errorMessage]
        },
        output: `Planning failed: ${errorMessage}`
      }
    }
  }
}