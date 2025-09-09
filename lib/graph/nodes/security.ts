import { PipelineState } from '../types';
import { securityScan } from '../tools';

export async function processSecurity(state: PipelineState): Promise<void> {
  console.log('Starting security scan...');
  state.currentNode = 'security';
  await securityScan();
  console.log('Security scan completed.');
}
