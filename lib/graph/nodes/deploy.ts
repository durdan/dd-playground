import { PipelineState } from '../types';
import { buildAndDeploy } from '../tools';

export async function processDeploy(state: PipelineState): Promise<void> {
  console.log('Building and deploying...');
  state.currentNode = 'deploy';
  await buildAndDeploy();
  console.log('Deployment completed.');
}
