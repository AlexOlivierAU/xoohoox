import React, { useEffect, useState } from 'react';
import { Box, Typography, Paper, Chip, CircularProgress, Alert } from '@mui/material';
import useSocket from '../../hooks/useSocket';
import ProductionChart from '../charts/ProductionChart';

interface BatchStatus {
  id: string;
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
  progress: number;
  startTime: string;
  estimatedCompletion: string;
  currentStage: string;
  qualityScore?: number;
}

interface BatchUpdate {
  batchId: string;
  status: BatchStatus['status'];
  progress: number;
  currentStage: string;
  qualityScore?: number;
}

const BatchStatusMonitor: React.FC = () => {
  const [batches, setBatches] = useState<BatchStatus[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [chartData, setChartData] = useState({
    labels: [] as string[],
    values: [] as number[]
  });

  // Initialize socket connection
  const { isConnected, on, emit } = useSocket({
    url: 'http://localhost:3000',
    autoConnect: true
  });

  // Fetch initial batch data
  useEffect(() => {
    const fetchBatches = async () => {
      try {
        setLoading(true);
        // In a real app, this would be an API call
        // For demo purposes, we'll simulate data
        const mockBatches: BatchStatus[] = [
          {
            id: 'BATCH-001',
            status: 'in_progress',
            progress: 45,
            startTime: new Date(Date.now() - 3600000).toISOString(),
            estimatedCompletion: new Date(Date.now() + 7200000).toISOString(),
            currentStage: 'Fermentation',
            qualityScore: 92
          },
          {
            id: 'BATCH-002',
            status: 'pending',
            progress: 0,
            startTime: new Date().toISOString(),
            estimatedCompletion: new Date(Date.now() + 10800000).toISOString(),
            currentStage: 'Preparation'
          }
        ];
        
        setBatches(mockBatches);
        
        // Set up chart data
        setChartData({
          labels: mockBatches.map(batch => batch.id),
          values: mockBatches.map(batch => batch.progress)
        });
        
        setLoading(false);
      } catch (err) {
        setError('Failed to fetch batch data');
        setLoading(false);
      }
    };

    fetchBatches();
  }, []);

  // Set up WebSocket listeners
  useEffect(() => {
    if (!isConnected) return;

    // Request initial data
    emit('getBatches', {});

    // Listen for batch updates
    const handleBatchUpdate = (update: BatchUpdate) => {
      setBatches(prevBatches => {
        const updatedBatches = prevBatches.map(batch => {
          if (batch.id === update.batchId) {
            return {
              ...batch,
              status: update.status,
              progress: update.progress,
              currentStage: update.currentStage,
              qualityScore: update.qualityScore || batch.qualityScore
            };
          }
          return batch;
        });

        // Update chart data
        setChartData({
          labels: updatedBatches.map(batch => batch.id),
          values: updatedBatches.map(batch => batch.progress)
        });

        return updatedBatches;
      });
    };

    on('batchUpdate', handleBatchUpdate);

    // Clean up
    return () => {
      // The hook will handle cleanup
    };
  }, [isConnected, emit, on]);

  // Get status color
  const getStatusColor = (status: BatchStatus['status']) => {
    switch (status) {
      case 'pending': return 'default';
      case 'in_progress': return 'primary';
      case 'completed': return 'success';
      case 'failed': return 'error';
      default: return 'default';
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mt: 2 }}>
        {error}
      </Alert>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>
        Batch Status Monitor
      </Typography>
      
      <Box sx={{ mb: 3 }}>
        <Chip 
          label={isConnected ? 'Connected' : 'Disconnected'} 
          color={isConnected ? 'success' : 'error'} 
          size="small" 
          sx={{ mr: 1 }} 
        />
        <Typography variant="body2" color="text.secondary" component="span">
          {isConnected ? 'Receiving real-time updates' : 'Connection lost. Attempting to reconnect...'}
        </Typography>
      </Box>
      
      <Box sx={{ mb: 4 }}>
        <Typography variant="h6" gutterBottom>
          Batch Progress Overview
        </Typography>
        <ProductionChart 
          data={chartData} 
          title="Batch Progress" 
          useMUI={true} 
        />
      </Box>
      
      <Typography variant="h6" gutterBottom>
        Active Batches
      </Typography>
      
      {batches.map(batch => (
        <Paper key={batch.id} sx={{ p: 2, mb: 2 }}>
          <Box display="flex" justifyContent="space-between" alignItems="center">
            <Typography variant="subtitle1">
              {batch.id}
            </Typography>
            <Chip 
              label={batch.status.replace('_', ' ')} 
              color={getStatusColor(batch.status)} 
              size="small" 
            />
          </Box>
          
          <Box sx={{ mt: 1 }}>
            <Typography variant="body2" color="text.secondary">
              Current Stage: {batch.currentStage}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Progress: {batch.progress}%
            </Typography>
            {batch.qualityScore && (
              <Typography variant="body2" color="text.secondary">
                Quality Score: {batch.qualityScore}/100
              </Typography>
            )}
          </Box>
          
          <Box sx={{ mt: 2 }}>
            <Typography variant="body2">
              Started: {new Date(batch.startTime).toLocaleString()}
            </Typography>
            <Typography variant="body2">
              Estimated Completion: {new Date(batch.estimatedCompletion).toLocaleString()}
            </Typography>
          </Box>
        </Paper>
      ))}
    </Box>
  );
};

export default BatchStatusMonitor; 