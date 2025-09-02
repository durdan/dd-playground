import { SDLCState, SDLCStateSchema } from './types'
import { PlanningNode, DevelopmentNode, ReviewNode } from './nodes'

export class SDLCPipeline {
  private state: SDLCState
  
  constructor(initialState?: Partial<SDLCState>) {
    this.state = SDLCStateSchema.parse(initialState || {})
  }
  
  async executeStep(input: string): Promise<{ state: SDLCState; output: string }> {
    const nodeInput = { state: this.state, input }
    
    let result
    
    switch (this.state.status) {
      case 'planning':
        result = await PlanningNode.execute(nodeInput)
        break
      case 'developing':
        result = await DevelopmentNode.execute(nodeInput)
        break
      case 'reviewing':
        result = await ReviewNode.execute(nodeInput)
        break
      case 'completed':
        return {
          state: this.state,
          output: 'Pipeline already completed'
        }
      default:
        throw new Error(`Unknown status: ${this.state.status}`)
    }
    
    this.state = result.state
    return result
  }
  
  getState(): SDLCState {
    return { ...this.state }
  }
  
  isCompleted(): boolean {
    return this.state.status === 'completed'
  }
  
  hasErrors(): boolean {
    return this.state.errors.length > 0
  }
}