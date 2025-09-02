import { PipelineState } from '../types';
import { openPR, requestReview } from '../../services/github';

/**
 * Review node - creates PR and requests code review
 */
export async function reviewNode(state: PipelineState): Promise<PipelineState> {
  console.log('👥 Creating PR and requesting review...');
  
  try {
    if (!state.codeGeneration?.files || state.codeGeneration.files.length === 0) {
      throw new Error('No generated files found for review');
    }

    // Create pull request
    const prResult = await openPR({
      title: `Automated code generation: ${state.task}`,
      description: `Generated ${state.codeGeneration.files.length} files for: ${state.task}`,
      files: state.codeGeneration.files,
      branch: `auto-gen-${Date.now()}`
    });

    // Request review from team members
    const reviewResult = await requestReview({
      prNumber: prResult.prNumber,
      reviewers: ['team-lead', 'senior-dev'] // Could be configurable
    });

    return {
      ...state,
      review: {
        prNumber: prResult.prNumber,
        prUrl: prResult.url,
        reviewers: reviewResult.reviewers,
        status: 'pending',
        createdAt: new Date().toISOString()
      }
    };
  } catch (error) {
    console.error('❌ Review process failed:', error);
    throw new Error(`Review process failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}