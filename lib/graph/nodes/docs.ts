import { PipelineState } from '../types';
import { generateDocs } from '../tools';

export async function processDocs(state: PipelineState): Promise<void> {
  console.log('Generating documentation...');
  state.currentNode = 'docs';
  await generateDocs();
  console.log('Documentation generated.');
}
