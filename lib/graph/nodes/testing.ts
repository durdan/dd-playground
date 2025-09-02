import { PipelineState } from '../types';
import { runUnitTests } from '../../services/testing';

/**
 * Testing node - runs unit tests on generated code
 */
export async function testingNode(state: PipelineState): Promise<PipelineState> {
  console.log('🧪 Running unit tests...');
  
  try {
    if (!state.codeGeneration?.files || state.codeGeneration.files.length === 0) {
      throw new Error('No generated files found for testing');
    }

    const testResult = await runUnitTests({
      files: state.codeGeneration.files,
      testFramework: 'jest', // Could be configurable
      coverage: true
    });

    return {
      ...state,
      testing: {
        passed: testResult.success,
        totalTests: testResult.totalTests,
        passedTests: testResult.passedTests,
        failedTests: testResult.failedTests,
        coverage: testResult.coverage,
        duration: testResult.duration,
        errors: testResult.errors || [],
        timestamp: new Date().toISOString()
      }
    };
  } catch (error) {
    console.error('❌ Testing failed:', error);
    throw new Error(`Testing failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}