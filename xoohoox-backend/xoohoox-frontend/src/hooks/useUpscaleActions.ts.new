import { useState } from 'react';
import axios from 'axios';
import { useToast } from './useToast';

interface UpscaleRun {
  id: number;
  upscale_id: string;
  stage: string;
  volume: number;
  yield_amount: number | null;
  abv_result: number | null;
  compound_summary: string | null;
  status: 'pending' | 'complete' | 'failed';
  timestamp: string;
}

interface UpscaleResult {
  yield_amount: number;
  abv_result: number;
  compound_summary: string;
}

export const useUpscaleActions = (trialId: number) => {
  const [loading, setLoading] = useState(false);
  const [upscales, setUpscales] = useState<UpscaleRun[]>([]);
  const { showSuccess, showError } = useToast();

  const fetchUpscales = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`/api/v1/trials/${trialId}/upscales`);
      setUpscales(response.data);
    } catch (error) {
      showError('Error fetching upscales');
    } finally {
      setLoading(false);
    }
  };

  const startNextUpscale = async () => {
    try {
      setLoading(true);
      const lastUpscale = upscales[upscales.length - 1];
      const nextStage = lastUpscale ? getNextStage(lastUpscale.stage) : 'Test 4';
      const volume = getVolumeForStage(nextStage);

      const response = await axios.post(`/api/v1/trials/${trialId}/upscales`, {
        stage: nextStage,
        volume,
      });

      setUpscales([...upscales, response.data]);
      showSuccess('New upscale started successfully');
    } catch (error) {
      showError('Error starting new upscale');
    } finally {
      setLoading(false);
    }
  };

  const updateUpscaleResults = async (upscaleId: number, results: UpscaleResult) => {
    try {
      setLoading(true);
      const response = await axios.patch(`/api/v1/upscales/${upscaleId}`, results);
      
      setUpscales(upscales.map(upscale => 
        upscale.id === upscaleId ? response.data : upscale
      ));
      
      showSuccess('Results updated successfully');
    } catch (error) {
      showError('Error updating results');
    } finally {
      setLoading(false);
    }
  };

  const completeUpscale = async (upscaleId: number) => {
    try {
      setLoading(true);
      const response = await axios.post(`/api/v1/upscales/${upscaleId}/complete`);
      
      setUpscales(upscales.map(upscale => 
        upscale.id === upscaleId ? response.data : upscale
      ));
      
      showSuccess('Upscale completed successfully');
    } catch (error) {
      showError('Error completing upscale');
    } finally {
      setLoading(false);
    }
  };

  // Helper functions
  const getNextStage = (currentStage: string): string => {
    const stages = ['Test 4', 'Test 5', 'Test 6'];
    const currentIndex = stages.indexOf(currentStage);
    return stages[currentIndex + 1] || stages[0];
  };

  const getVolumeForStage = (stage: string): number => {
    const volumes: Record<string, number> = {
      'Test 4': 5,
      'Test 5': 30,
      'Test 6': 100,
    };
    return volumes[stage] || 5;
  };

  const canStartNextUpscale = (): boolean => {
    if (upscales.length === 0) return true;
    const lastUpscale = upscales[upscales.length - 1];
    return lastUpscale.status === 'complete' && lastUpscale.stage !== 'Test 6';
  };

  return {
    upscales,
    loading,
    fetchUpscales,
    startNextUpscale,
    updateUpscaleResults,
    completeUpscale,
    canStartNextUpscale,
  };
}; 