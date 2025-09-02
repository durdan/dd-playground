import { describe, it, expect } from '@jest/globals';
import {
  PipelineStateSchema,
  ReviewNoteSchema,
  TestReportSchema,
  SecurityReportSchema,
  createInitialPipelineState,
  updateLoopCount,
  validatePipelineState,
  type PipelineState
} from '../state';

describe('PipelineState Schema', () => {
  const validMinimalState = {
    req_summary: 'Add user authentication',
    repo_url: 'https://github.com/user/repo.git',
    branch: 'feature/auth'
  };

  it('should validate minimal valid state', () => {
    const result = PipelineStateSchema.safeParse(validMinimalState);
    expect(result.success).toBe(true);
    
    if (result.success) {
      expect(result.data.req_summary).toBe('Add user authentication');
      expect(result.data.repo_url).toBe('https://github.com/user/repo.git');
      expect(result.data.branch).toBe('feature/auth');
      expect(result.data.review_notes).toEqual([]);
      expect(result.data.loop_counts).toEqual({});
      expect(result.data.code_patch).toBeNull();
    }
  });

  it('should reject invalid repo URL', () => {
    const invalidState = {
      ...validMinimalState,
      repo_url: 'not-a-url'
    };
    
    const result = PipelineStateSchema.safeParse(invalidState);
    expect(result.success).toBe(false);
  });

  it('should reject empty req_summary', () => {
    const invalidState = {
      ...validMinimalState,
      req_summary: ''
    };
    
    const result = PipelineStateSchema.safeParse(invalidState);
    expect(result.success).toBe(false);
  });

  it('should use default branch when not provided', () => {
    const stateWithoutBranch = {
      req_summary: 'Add feature',
      repo_url: 'https://github.com/user/repo.git'
    };
    
    const result = PipelineStateSchema.safeParse(stateWithoutBranch);
    expect(result.success).toBe(true);
    
    if (result.success) {
      expect(result.data.branch).toBe('main');
    }
  });
});

describe('ReviewNote Schema', () => {
  it('should validate complete review note', () => {
    const reviewNote = {
      id: 'note-1',
      type: 'suggestion' as const,
      severity: 'high' as const,
      message: 'Consider using async/await',
      file_path: 'src/auth.ts',
      line_number: 42,
      resolved: false
    };
    
    const result = ReviewNoteSchema.safeParse(reviewNote);
    expect(result.success).toBe(true);
  });

  it('should use defaults for optional fields', () => {
    const minimalNote = {
      id: 'note-2',
      type: 'issue' as const,
      message: 'Fix this bug',
      file_path: null,
      line_number: null
    };
    
    const result = ReviewNoteSchema.safeParse(minimalNote);
    expect(result.success).toBe(true);
    
    if (result.success) {
      expect(result.data.severity).toBe('medium');
      expect(result.data.resolved).toBe(false);
      expect(result.data.created_at).toBeInstanceOf(Date);
    }
  });
});

describe('TestReport Schema', () => {
  it('should validate complete test report', () => {
    const testReport = {
      total_tests: 100,
      passed_tests: 95,
      failed_tests: 5,
      skipped_tests: 0,
      coverage_percentage: 85.5,
      test_files: ['test/auth.test.ts', 'test/user.test.ts'],
      failures: [{
        test_name: 'should authenticate user',
        error_message: 'Expected true but got false',
        file_path: 'test/auth.test.ts',
        line_number: 25
      }],
      execution_time_ms: 5000
    };
    
    const result = TestReportSchema.safeParse(testReport);
    expect(result.success).toBe(true);
  });

  it('should use defaults for optional fields', () => {
    const minimalReport = {};
    
    const result = TestReportSchema.safeParse(minimalReport);
    expect(result.success).toBe(true);
    
    if (result.success) {
      expect(result.data.total_tests).toBe(0);
      expect(result.data.passed_tests).toBe(0);
      expect(result.data.test_files).toEqual([]);
      expect(result.data.failures).toEqual([]);
    }
  });
});

describe('Helper Functions', () => {
  it('should create initial pipeline state', () => {
    const state = createInitialPipelineState(
      'Add authentication',
      'https://github.com/user/repo.git',
      'feature/auth'
    );
    
    expect(state.req_summary).toBe('Add authentication');
    expect(state.repo_url).toBe('https://github.com/user/repo.git');
    expect(state.branch).toBe('feature/auth');
    expect(state.code_patch).toBeNull();
    expect(state.review_notes).toEqual([]);
    expect(state.loop_counts).toEqual({});
  });

  it('should update loop count', () => {
    const initialState = createInitialPipelineState(
      'Test',
      'https://github.com/test/repo.git'
    );
    
    const updatedState = updateLoopCount(initialState, 'review_loop');
    expect(updatedState.loop_counts.review_loop).toBe(1);
    
    const updatedAgain = updateLoopCount(updatedState, 'review_loop');
    expect(updatedAgain.loop_counts.review_loop).toBe(2);
  });

  it('should validate pipeline state', () => {
    const validData = {
      req_summary: 'Test summary',
      repo_url: 'https://github.com/test/repo.git',
      branch: 'main'
    };
    
    expect(() => validatePipelineState(validData)).not.toThrow();
    
    const invalidData = {
      req_summary: '',
      repo_url: 'invalid-url'
    };
    
    expect(() => validatePipelineState(invalidData)).toThrow();
  });
});