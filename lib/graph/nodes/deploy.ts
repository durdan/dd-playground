import { PipelineState } from '../types';
import { buildAndDeploy } from '../../services/deployment';

/**
 * Deployment node - builds and deploys the application
 */
export async function deployNode(state: PipelineState): Promise<PipelineState> {
  console.log('🚀 Building and deploying...');
  
  try {
    // Check prerequisites
    if (!state.codeGeneration?.files || state.codeGeneration.files.length === 0) {
      throw new Error('No generated files found for deployment');
    }

    if (!state.testing?.passed) {
      throw new Error('Cannot deploy: tests have not passed');
    }

    if (!state.security?.passed) {
      throw new Error('Cannot deploy: security scan has not passed');
    }

    const deployResult = await buildAndDeploy({
      files: state.codeGeneration.files,
      environment: 'staging', // Could be configurable
      buildCommand: 'npm run build',
      healthCheck: true
    });

    return {
      ...state,
      deployment: {
        deployed: true,
        environment: deployResult.environment,
        url: deployResult.url,
        version: deployResult.version,
        buildTime: deployResult.buildTime,
        deployTime: deployResult.deployTime,
        healthCheck: deployResult.healthCheck,
        timestamp: new Date().toISOString()
      }
    };
  } catch (error) {
    console.error('❌ Deployment failed:', error);
    throw new Error(`Deployment failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}