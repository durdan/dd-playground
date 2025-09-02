import { testingNode } from '../testing';
import { PipelineState } from '../../types';
import { runUnitTests } from '../../../services/testing';

jest.mock('../../../services/testing');

describe('testingNode', () => {
  const mockRunUnitTests = runUnitTests as jest.MockedFunction<typeof runUnitTests>;

  const mockState: PipelineState = {
    task: 'test task',
    codeGeneration: {
      files: [{ path: 'test.ts', content: 'test content' }],
      timestamp: '2023-01-01'
    }
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should run tests successfully', async () => {
    mockRunUnitTests.mockResolvedValue({
      success: true,
      totalTests: 10,
      passedTests: 10,
      failedTests: 0,
      coverage: 85,
      duration: 1500
    });

    const result = await testingNode(mockState);
    
    expect(result.testing).toBeDefined();
    expect(result.testing?.passed).toBe(true);
    expect(result.testing?.totalTests).toBe(10);
    expect(result.testing?.coverage).toBe(85);
  });

  it('should handle test failures', async () => {
    mockRunUnitTests.mockResolvedValue({
      success: false,
      totalTests: 10,
      passedTests: 8,
      failedTests: 2,
      coverage: 75,
      duration: 1200,
      errors: ['Test 1 failed', 'Test 2 failed']
    });

    const result = await testingNode(mockState);
    
    expect(result.testing?.passed).toBe(false);
    expect(result.testing?.failedTests).toBe(2);
    expect(result.testing?.errors).toEqual(['Test 1 failed', 'Test 2 failed']);
  });
});