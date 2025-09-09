import { PipelineState } from '../types';
import { runUnitTests } from '../tools';

export async function processTesting(state: PipelineState): Promise<void> {
  console.log('Running unit tests...');
  state.currentNode = 'testing';
  await runUnitTests();
  console.log('Unit tests completed.');
}
