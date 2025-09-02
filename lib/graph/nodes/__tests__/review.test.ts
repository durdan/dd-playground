import { reviewNode } from '../review';
import { PipelineState } from '../../types';
import { openPR, requestReview } from '../../../services/github';

jest.mock('../../../services/github');

describe('reviewNode', () => {
  const mockOpenPR = openPR as jest.MockedFunction<typeof openPR>;
  const mockRequestReview = requestReview as jest.MockedFunction<typeof requestReview>;

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

  it('should create PR and request review successfully', async () => {
    mockOpenPR.mockResolvedValue({ prNumber: 123, url: 'https://github.com/test/pr/123' });
    mockRequestReview.mockResolvedValue({ reviewers: ['team-lead', 'senior-dev'] });

    const result = await reviewNode(mockState);
    
    expect(result.review).toBeDefined();
    expect(result.review?.prNumber).toBe(123);
    expect(result.review?.prUrl).toBe('https://github.com/test/pr/123');
    expect(result.review?.reviewers).toEqual(['team-lead', 'senior-dev']);
    expect(result.review?.status).toBe('pending');
  });

  it('should throw error when no files are generated', async () => {
    const stateWithoutFiles = { ...mockState, codeGeneration: undefined };
    
    await expect(reviewNode(stateWithoutFiles)).rejects.toThrow('No generated files found for review');
  });
});