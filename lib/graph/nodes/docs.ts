import { PipelineState } from '../types';
import { generateDocs } from '../../services/documentation';

/**
 * Documentation node - generates documentation for the code
 */
export async function docsNode(state: PipelineState): Promise<PipelineState> {
  console.log('📚 Generating documentation...');
  
  try {
    if (!state.codeGeneration?.files || state.codeGeneration.files.length === 0) {
      throw new Error('No generated files found for documentation');
    }

    const docsResult = await generateDocs({
      files: state.codeGeneration.files,
      format: 'markdown', // Could be configurable
      includeExamples: true,
      includeAPI: true
    });

    return {
      ...state,
      documentation: {
        generated: true,
        files: docsResult.files,
        format: docsResult.format,
        coverage: docsResult.coverage,
        timestamp: new Date().toISOString()
      }
    };
  } catch (error) {
    console.error('❌ Documentation generation failed:', error);
    throw new Error(`Documentation generation failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}