import { useState, useCallback, useEffect } from 'react';
import specificationService from '../services/specificationService';
import integrationService from '../services/integrationService';

export const useSpecificationGeneration = () => {
  const [isGenerating, setIsGenerating] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  useEffect(() => {
    integrationService.connect().catch(console.error);
    return () => integrationService.disconnect();
  }, []);

  const generateSpecification = useCallback(async (chatHistory, requirements) => {
    setIsGenerating(true);
    setProgress(0);
    setError(null);
    setResult(null);

    try {
      const response = await specificationService.generateSpecification(chatHistory, requirements);
      const { jobId } = response;

      const cleanup = specificationService.subscribeToProgress(
        jobId,
        (progressData) => {
          setProgress(progressData.progress);
        },
        (completeData) => {
          setResult(completeData.specification);
          setIsGenerating(false);
          setProgress(100);
        },
        (errorData) => {
          setError(errorData.error);
          setIsGenerating(false);
        }
      );

      return cleanup;
    } catch (err) {
      setError(err.message);
      setIsGenerating(false);
    }
  }, []);

  return {
    generateSpecification,
    isGenerating,
    progress,
    error,
    result,
    clearError: () => setError(null)
  };
};