// testing.ts - Handles the agent node for testing
import { PipelineState } from '../types';

/**
 * Processes testing node.
 * Simulates running unit tests.
 * @param {PipelineState} state - The current state of the pipeline.
 */
export async function processTesting(state: PipelineState): Promise<void> {
  console.log('Running unit tests...');
  state.updateNodeState('testing', 'completed');
}
