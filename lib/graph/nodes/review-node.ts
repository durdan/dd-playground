import { NodeInput, NodeOutput, SDLCState } from '../types'
import { chatComplete } from '../../llm'

export class ReviewNode {
  static async execute(input: NodeInput): Promise<NodeOutput> {
    const { state } = input
    
    try {
      if (!state.code) {
        throw new Error('No code available for review')
      }
      
      // Use real LLM to review the generated code
      const reviewPrompt = [
        {
          role: 'system' as const,
          content: `You are a senior software engineer and code reviewer with extensive experience in code quality, security, and best practices. Your role is to provide thorough, constructive code reviews.

When reviewing code, you should:
1. Analyze code quality, structure, and readability
2. Check for security vulnerabilities and best practices
3. Evaluate performance implications
4. Assess maintainability and scalability
5. Verify adherence to coding standards
6. Suggest specific improvements with examples
7. Identify potential bugs or edge cases

Format your review with:
- Summary of overall code quality
- Specific strengths found
- Issues identified with severity levels
- Actionable recommendations
- Final approval status (Approved/Needs Changes/Rejected)`
        },
        {
          role: 'user' as const,
          content: `Please review the following code implementation:

Original Requirements: ${state.requirements}

Development Plan: ${state.plan}

Implementation Code:
${state.code}

Please provide a comprehensive code review covering:
- Code quality and structure
- Security considerations
- Performance implications
- Best practices adherence
- Specific improvement suggestions
- Overall recommendation`
        }
      ]

      console.log('Review Node: Calling LLM for code review...')
      const review = await chatComplete(reviewPrompt)
      console.log('Review Node: LLM response received')
      
      const updatedState: SDLCState = {
        ...state,
        review,
        status: 'completed',
        metadata: {
          ...state.metadata,
          reviewTimestamp: new Date().toISOString(),
          reviewAgent: 'OpenAI GPT-4o-mini'
        }
      }
      
      return {
        state: updatedState,
        output: review
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown review error'
      console.error('Review Node error:', error)
      
      return {
        state: {
          ...state,
          errors: [...state.errors, errorMessage]
        },
        output: `Review failed: ${errorMessage}`
      }
    }
  }
}