import { PipelineState } from '../types';
import { openPR, requestReview } from '../tools';

export async function processReview(state: PipelineState): Promise<void> {
  console.log('Starting review process...');
  state.currentNode = 'review';
  await openPR();
  await requestReview();
  console.log('Review process completed.');
}
