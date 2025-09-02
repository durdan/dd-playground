import { PipelineState } from '../types';
import { securityScan } from '../../services/security';

/**
 * Security node - runs security scans on generated code
 */
export async function securityNode(state: PipelineState): Promise<PipelineState> {
  console.log('🔒 Running security scan...');
  
  try {
    if (!state.codeGeneration?.files || state.codeGeneration.files.length === 0) {
      throw new Error('No generated files found for security scanning');
    }

    const scanResult = await securityScan({
      files: state.codeGeneration.files,
      scanTypes: ['vulnerabilities', 'secrets', 'dependencies'],
      severity: 'medium' // Could be configurable
    });

    return {
      ...state,
      security: {
        scanned: true,
        vulnerabilities: scanResult.vulnerabilities,
        secrets: scanResult.secrets,
        dependencyIssues: scanResult.dependencyIssues,
        score: scanResult.score,
        passed: scanResult.vulnerabilities.length === 0 && scanResult.secrets.length === 0,
        timestamp: new Date().toISOString()
      }
    };
  } catch (error) {
    console.error('❌ Security scan failed:', error);
    throw new Error(`Security scan failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}