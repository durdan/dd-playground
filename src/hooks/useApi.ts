import { useState, useEffect, useCallback } from 'react';
import { ApiError, LoadingState } from '../types/api';

interface UseApiOptions {
  immediate?: boolean;
  onSuccess?: (data: any) => void;
  onError?: (error: ApiError) => void;
}

export function useApi<T>(
  apiCall: () => Promise<T>,
  options: UseApiOptions = {}
) {
  const { immediate = true, onSuccess, onError } = options;
  
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState<boolean>(immediate);
  const [error, setError] = useState<ApiError | null>(null);

  const execute = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      const result = await apiCall();
      setData(result);
      
      if (onSuccess) onSuccess(result);
      
      return result;
    } catch (err) {
      const apiError = err as ApiError;
      setError(apiError);
      
      if (onError) onError(apiError);
      
      throw apiError;
    } finally {
      setLoading(false);
    }
  }, [apiCall, onSuccess, onError]);

  useEffect(() => {
    if (immediate) {
      execute();
    }
  }, [execute, immediate]);

  const reset = useCallback(() => {
    setData(null);
    setError(null);
    setLoading(false);
  }, []);

  return {
    data,
    loading,
    error,
    execute,
    reset
  };
}