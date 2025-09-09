// security.ts - Handles the agent node for security scanning
import { PipelineState } from '../types';

/**
 * Processes security node.
 * Simulates a security scan.
 * @param {PipelineState} state - The current state of the pipeline.
 */
export async function processSecurity(state: PipelineState): Promise<void> {
  console.log('Performing security scan...');
  state.updateNodeState('security', 'completed');
}
