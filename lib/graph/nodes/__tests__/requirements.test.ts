import { requirementsNode } from '../requirements';
import { PipelineState } from '../../types';

describe('requirementsNode', () => {
  const mockState: PipelineState = {
    task: 'test task',
    planning: { plan: 'test plan', timestamp: '2023-01-01' }
  };

  it('should process requirements successfully', async () => {
    const result = await requirementsNode(mockState);
    
    expect(result.requirements).toBeDefined();
    expect(result.requirements?.analyzed).toBe(true);
    expect(result.requirements?.timestamp).toBeDefined();
    expect(result.requirements?.dependencies).toEqual([]);
    expect(result.requirements?.conflicts).toEqual([]);
  });

  it('should preserve existing state', async () => {
    const result = await requirementsNode(mockState);
    
    expect(result.task).toBe(mockState.task);
    expect(result.planning).toEqual(mockState.planning);
  });
});