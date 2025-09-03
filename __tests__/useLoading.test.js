import { renderHook, act } from '@testing-library/react';
import { useLoading } from '../hooks/useLoading';

describe('useLoading', () => {
  test('should initialize with default state', () => {
    const { result } = renderHook(() => useLoading());
    
    expect(result.current.isLoading).toBe(false);
    expect(result.current.error).toBe(null);
  });

  test('should initialize with custom initial state', () => {
    const { result } = renderHook(() => useLoading(true));
    
    expect(result.current.isLoading).toBe(true);
  });

  test('should start and stop loading', () => {
    const { result } = renderHook(() => useLoading());
    
    act(() => {
      result.current.startLoading();
    });
    expect(result.current.isLoading).toBe(true);
    expect(result.current.error).toBe(null);
    
    act(() => {
      result.current.stopLoading();
    });
    expect(result.current.isLoading).toBe(false);
  });

  test('should handle errors', () => {
    const { result } = renderHook(() => useLoading());
    
    act(() => {
      result.current.setLoadingError('Test error');
    });
    
    expect(result.current.isLoading).toBe(false);
    expect(result.current.error).toBe('Test error');
  });

  test('should execute async function successfully', async () => {
    const { result } = renderHook(() => useLoading());
    const mockAsyncFn = jest.fn().mockResolvedValue('success');
    
    let promise;
    act(() => {
      promise = result.current.executeAsync(mockAsyncFn);
    });
    
    expect(result.current.isLoading).toBe(true);
    
    const response = await promise;
    
    expect(response).toBe('success');
    expect(result.current.isLoading).toBe(false);
    expect(result.current.error).toBe(null);
  });

  test('should handle async function errors', async () => {
    const { result } = renderHook(() => useLoading());
    const mockAsyncFn = jest.fn().mockRejectedValue(new Error('Async error'));
    
    let promise;
    act(() => {
      promise = result.current.executeAsync(mockAsyncFn);
    });
    
    expect(result.current.isLoading).toBe(true);
    
    await expect(promise).rejects.toThrow('Async error');
    expect(result.current.isLoading).toBe(false);
    expect(result.current.error).toBe('Async error');
  });
});