import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  Button,
  Chip,
  LinearProgress,
  Alert,
  CircularProgress,
  Stack,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  PlayArrow as PlayIcon,
  Pause as PauseIcon,
  Stop as StopIcon,
  Refresh as RefreshIcon,
  TrendingUp as TrendingUpIcon,
  LocalDrink as DrinkIcon,
  Science as ScienceIcon,
  Schedule as ScheduleIcon,
} from '@mui/icons-material';
import batchService from '../services/batchService';

interface ProductionData {
  activeBatches: number;
  totalProduction: number;
  efficiency: number;
  currentStage: string;
  alerts: Array<{
    id: string;
    type: 'warning' | 'error' | 'info';
    message: string;
    timestamp: string;
  }>;
  recentActivity: Array<{
    id: string;
    action: string;
    batch: string;
    timestamp: string;
  }>;
}

const Production = () => {
  const [data, setData] = useState<ProductionData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchProductionData();
    // Set up real-time updates
    const interval = setInterval(fetchProductionData, 30000); // Update every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchProductionData = async () => {
    try {
      setLoading(true);
      const batchesResponse = await batchService.getBatches();
      const batches = batchesResponse.items;

      const productionData: ProductionData = {
        activeBatches: batches.filter(b => b.status === 'active' || b.status === 'in_progress').length,
        totalProduction: batches.reduce((sum, b) => sum + (b.quantity || 0), 0),
        efficiency: batches.length > 0 
          ? (batches.filter(b => b.status === 'completed').length / batches.length) * 100
          : 0,
        currentStage: 'Fermentation',
        alerts: [
          {
            id: '1',
            type: 'warning',
            message: 'Temperature alert: Batch B001 is above optimal range',
            timestamp: new Date().toISOString(),
          },
          {
            id: '2',
            type: 'info',
            message: 'Quality check completed for Batch B003',
            timestamp: new Date(Date.now() - 300000).toISOString(),
          },
        ],
        recentActivity: [
          {
            id: '1',
            action: 'Batch started',
            batch: 'B004',
            timestamp: new Date().toISOString(),
          },
          {
            id: '2',
            action: 'Quality check performed',
            batch: 'B003',
            timestamp: new Date(Date.now() - 600000).toISOString(),
          },
          {
            id: '3',
            action: 'Stage completed',
            batch: 'B002',
            timestamp: new Date(Date.now() - 900000).toISOString(),
          },
        ],
      };

      setData(productionData);
    } catch (err: any) {
      setError('Failed to fetch production data');
      console.error('Error fetching production data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = () => {
    fetchProductionData();
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error || !data) {
    return (
      <Box sx={{ p: 3 }}>
        <Alert severity="error">{error || 'Failed to load production data'}</Alert>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Production Control
        </Typography>
        <Button
          variant="outlined"
          startIcon={<RefreshIcon />}
          onClick={handleRefresh}
        >
          Refresh
        </Button>
      </Box>

      {/* Production Overview */}
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3, mb: 4 }}>
        <Box sx={{ flex: '1 1 250px', minWidth: 250 }}>
          <Paper sx={{ p: 3, textAlign: 'center' }}>
            <DrinkIcon color="primary" sx={{ fontSize: 40, mb: 1 }} />
            <Typography variant="h3" color="primary">
              {data.activeBatches}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Active Batches
            </Typography>
          </Paper>
        </Box>
        <Box sx={{ flex: '1 1 250px', minWidth: 250 }}>
          <Paper sx={{ p: 3, textAlign: 'center' }}>
            <TrendingUpIcon color="success" sx={{ fontSize: 40, mb: 1 }} />
            <Typography variant="h3" color="success.main">
              {data.totalProduction.toLocaleString()}L
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Total Production
            </Typography>
          </Paper>
        </Box>
        <Box sx={{ flex: '1 1 250px', minWidth: 250 }}>
          <Paper sx={{ p: 3, textAlign: 'center' }}>
            <ScienceIcon color="info" sx={{ fontSize: 40, mb: 1 }} />
            <Typography variant="h3" color="info.main">
              {data.efficiency.toFixed(1)}%
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Efficiency Rate
            </Typography>
          </Paper>
        </Box>
        <Box sx={{ flex: '1 1 250px', minWidth: 250 }}>
          <Paper sx={{ p: 3, textAlign: 'center' }}>
            <ScheduleIcon color="warning" sx={{ fontSize: 40, mb: 1 }} />
            <Typography variant="h3" color="warning.main">
              {data.currentStage}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Current Stage
            </Typography>
          </Paper>
        </Box>
      </Box>

      {/* Production Controls */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Production Controls
        </Typography>
        <Stack direction="row" spacing={2} sx={{ mb: 3 }}>
          <Button
            variant="contained"
            color="success"
            startIcon={<PlayIcon />}
            size="large"
          >
            Start Production
          </Button>
          <Button
            variant="outlined"
            color="warning"
            startIcon={<PauseIcon />}
            size="large"
          >
            Pause All
          </Button>
          <Button
            variant="outlined"
            color="error"
            startIcon={<StopIcon />}
            size="large"
          >
            Emergency Stop
          </Button>
        </Stack>
        
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Typography variant="body2" sx={{ mr: 2 }}>
            System Status:
          </Typography>
          <Chip label="Operational" color="success" />
        </Box>
        
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <Typography variant="body2" sx={{ mr: 2 }}>
            Overall Progress:
          </Typography>
          <LinearProgress
            variant="determinate"
            value={75}
            sx={{ flexGrow: 1, mr: 2 }}
          />
          <Typography variant="body2">
            75%
          </Typography>
        </Box>
      </Paper>

      {/* Alerts and Activity */}
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3 }}>
        <Box sx={{ flex: '1 1 400px', minWidth: 400 }}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Recent Alerts
            </Typography>
            <Stack spacing={2}>
              {data.alerts.map((alert) => (
                <Box key={alert.id} sx={{ display: 'flex', alignItems: 'flex-start' }}>
                  <Alert 
                    severity={alert.type} 
                    sx={{ flexGrow: 1 }}
                  >
                    {alert.message}
                  </Alert>
                </Box>
              ))}
            </Stack>
          </Paper>
        </Box>
        
        <Box sx={{ flex: '1 1 400px', minWidth: 400 }}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Recent Activity
            </Typography>
            <Stack spacing={2}>
              {data.recentActivity.map((activity) => (
                <Box key={activity.id} sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Box>
                    <Typography variant="body2" fontWeight="bold">
                      {activity.action}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      Batch {activity.batch}
                    </Typography>
                  </Box>
                  <Typography variant="caption" color="text.secondary">
                    {new Date(activity.timestamp).toLocaleTimeString()}
                  </Typography>
                </Box>
              ))}
            </Stack>
          </Paper>
        </Box>
      </Box>

      {/* Real-time Monitoring */}
      <Paper sx={{ p: 3, mt: 3 }}>
        <Typography variant="h6" gutterBottom>
          Real-time Monitoring
        </Typography>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
          <Chip label="Temperature: 22°C" color="success" />
          <Chip label="pH Level: 3.5" color="info" />
          <Chip label="Pressure: 1.2 bar" color="primary" />
          <Chip label="Flow Rate: 15 L/min" color="secondary" />
          <Chip label="Humidity: 65%" color="default" />
        </Box>
      </Paper>
    </Box>
  );
};

export default Production; 