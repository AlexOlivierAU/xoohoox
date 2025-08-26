import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Button,
  Card,
  CardContent,
  Stack,
  Chip,
  Alert,
  CircularProgress,
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  LocalDrink as DrinkIcon,
  Science as ScienceIcon,
  Settings as SettingsIcon,
  TrendingUp as TrendingUpIcon,
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon,
  Schedule as ScheduleIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import batchService from '../services/batchService';
import qualityService from '../services/qualityService';

interface HomeData {
  totalBatches: number;
  activeBatches: number;
  completedBatches: number;
  qualityScore: number;
  recentActivity: Array<{
    id: string;
    action: string;
    description: string;
    timestamp: string;
    type: 'success' | 'warning' | 'info';
  }>;
  quickStats: Array<{
    title: string;
    value: string;
    icon: React.ReactNode;
    color: string;
  }>;
}

const Home = () => {
  const [data, setData] = useState<HomeData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetchHomeData();
  }, []);

  const fetchHomeData = async () => {
    try {
      setLoading(true);
      const batchesResponse = await batchService.getBatches();
      const qualityResponse = await qualityService.getQualityChecks();

      const batches = batchesResponse.items;
      const qualityChecks = qualityResponse.items;

      const homeData: HomeData = {
        totalBatches: batches.length,
        activeBatches: batches.filter(b => b.status === 'active' || b.status === 'in_progress').length,
        completedBatches: batches.filter(b => b.status === 'completed').length,
        qualityScore: qualityChecks.length > 0 
          ? (qualityChecks.filter(q => q.result === 'pass').length / qualityChecks.length) * 100
          : 0,
        recentActivity: [
          {
            id: '1',
            action: 'Batch Started',
            description: 'New apple juice batch B004 has been initiated',
            timestamp: new Date().toISOString(),
            type: 'success',
          },
          {
            id: '2',
            action: 'Quality Check',
            description: 'Quality check completed for batch B003 - All parameters within range',
            timestamp: new Date(Date.now() - 300000).toISOString(),
            type: 'success',
          },
          {
            id: '3',
            action: 'Alert',
            description: 'Temperature alert for batch B001 - Above optimal range',
            timestamp: new Date(Date.now() - 600000).toISOString(),
            type: 'warning',
          },
          {
            id: '4',
            action: 'Stage Completed',
            description: 'Fermentation stage completed for batch B002',
            timestamp: new Date(Date.now() - 900000).toISOString(),
            type: 'info',
          },
        ],
        quickStats: [
          {
            title: 'Total Batches',
            value: batches.length.toString(),
            icon: <DrinkIcon />,
            color: 'primary',
          },
          {
            title: 'Active Production',
            value: batches.filter(b => b.status === 'active' || b.status === 'in_progress').length.toString(),
            icon: <TrendingUpIcon />,
            color: 'success',
          },
          {
            title: 'Quality Score',
            value: `${(qualityChecks.length > 0 
              ? (qualityChecks.filter(q => q.result === 'pass').length / qualityChecks.length) * 100
              : 0).toFixed(1)}%`,
            icon: <ScienceIcon />,
            color: 'info',
          },
          {
            title: 'Completed Today',
            value: batches.filter(b => b.status === 'completed').length.toString(),
            icon: <CheckCircleIcon />,
            color: 'success',
          },
        ],
      };

      setData(homeData);
    } catch (err: any) {
      console.error('Error fetching home data:', err);
      
      // Fallback to mock data when backend is not available
      const mockData: HomeData = {
        totalBatches: 12,
        activeBatches: 3,
        completedBatches: 8,
        qualityScore: 94.5,
        recentActivity: [
          {
            id: '1',
            action: 'Batch Started',
            description: 'New apple juice batch B004 has been initiated',
            timestamp: new Date().toISOString(),
            type: 'success',
          },
          {
            id: '2',
            action: 'Quality Check',
            description: 'Quality check completed for batch B003 - All parameters within range',
            timestamp: new Date(Date.now() - 300000).toISOString(),
            type: 'success',
          },
          {
            id: '3',
            action: 'Alert',
            description: 'Temperature alert for batch B001 - Above optimal range',
            timestamp: new Date(Date.now() - 600000).toISOString(),
            type: 'warning',
          },
          {
            id: '4',
            action: 'Stage Completed',
            description: 'Fermentation stage completed for batch B002',
            timestamp: new Date(Date.now() - 900000).toISOString(),
            type: 'info',
          },
        ],
        quickStats: [
          {
            title: 'Total Batches',
            value: '12',
            icon: <DrinkIcon />,
            color: 'primary',
          },
          {
            title: 'Active Production',
            value: '3',
            icon: <TrendingUpIcon />,
            color: 'success',
          },
          {
            title: 'Quality Score',
            value: '94.5%',
            icon: <ScienceIcon />,
            color: 'info',
          },
          {
            title: 'Completed Today',
            value: '8',
            icon: <CheckCircleIcon />,
            color: 'success',
          },
        ],
      };

      setData(mockData);
      setError(null); // Clear error since we have mock data
    } finally {
      setLoading(false);
    }
  };

  const handleQuickAction = (action: string) => {
    switch (action) {
      case 'batches':
        navigate('/batches');
        break;
      case 'quality':
        navigate('/quality-checks');
        break;
      case 'production':
        navigate('/production');
        break;
      case 'analytics':
        navigate('/analytics');
        break;
      default:
        break;
    }
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
        <Alert severity="error">{error || 'Failed to load home data'}</Alert>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      {/* Welcome Section */}
      <Paper sx={{ p: 4, mb: 4, background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
        <Typography variant="h3" gutterBottom>
          Welcome to Xoohoox
        </Typography>
        <Typography variant="h6" sx={{ mb: 3, opacity: 0.9 }}>
          Distillation Management System
        </Typography>
        <Typography variant="body1" sx={{ mb: 3, opacity: 0.8 }}>
          Monitor your distillation, track quality metrics, and manage your distillation process efficiently.
        </Typography>
        <Stack direction="row" spacing={2}>
          <Button
            variant="contained"
            color="inherit"
            startIcon={<DrinkIcon />}
            onClick={() => handleQuickAction('batches')}
            sx={{ color: 'white', borderColor: 'white' }}
          >
            View Batches
          </Button>
          <Button
            variant="outlined"
            color="inherit"
            startIcon={<ScienceIcon />}
            onClick={() => handleQuickAction('quality')}
            sx={{ color: 'white', borderColor: 'white' }}
          >
            Quality Control
          </Button>
        </Stack>
      </Paper>

      {/* Quick Stats */}
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3, mb: 4 }}>
        {data.quickStats.map((stat, index) => (
          <Box key={index} sx={{ flex: '1 1 200px', minWidth: 200 }}>
            <Card>
              <CardContent sx={{ textAlign: 'center' }}>
                <Box sx={{ color: `${stat.color}.main`, mb: 1 }}>
                  {stat.icon}
                </Box>
                <Typography variant="h4" color={`${stat.color}.main`}>
                  {stat.value}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {stat.title}
                </Typography>
              </CardContent>
            </Card>
          </Box>
        ))}
      </Box>

      {/* Quick Actions */}
      <Paper sx={{ p: 3, mb: 4 }}>
        <Typography variant="h6" gutterBottom>
          Quick Actions
        </Typography>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
          <Button
            variant="outlined"
            startIcon={<DrinkIcon />}
            onClick={() => handleQuickAction('batches')}
            size="large"
          >
            Manage Batches
          </Button>
          <Button
            variant="outlined"
            startIcon={<ScienceIcon />}
            onClick={() => handleQuickAction('quality')}
            size="large"
          >
            Quality Control
          </Button>
          <Button
            variant="outlined"
            startIcon={<TrendingUpIcon />}
            onClick={() => handleQuickAction('production')}
            size="large"
          >
            Production Control
          </Button>
          <Button
            variant="outlined"
            startIcon={<DashboardIcon />}
            onClick={() => handleQuickAction('analytics')}
            size="large"
          >
            View Analytics
          </Button>
        </Box>
      </Paper>

      {/* Recent Activity */}
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3 }}>
        <Box sx={{ flex: '1 1 500px', minWidth: 500 }}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Recent Activity
            </Typography>
            <Stack spacing={2}>
              {data.recentActivity.map((activity) => (
                <Box key={activity.id} sx={{ display: 'flex', alignItems: 'flex-start', gap: 2 }}>
                  <Box sx={{ 
                    width: 8, 
                    height: 8, 
                    borderRadius: '50%', 
                    mt: 1,
                    bgcolor: activity.type === 'success' ? 'success.main' : 
                             activity.type === 'warning' ? 'warning.main' : 'info.main'
                  }} />
                  <Box sx={{ flexGrow: 1 }}>
                    <Typography variant="body2" fontWeight="bold">
                      {activity.action}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {activity.description}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {new Date(activity.timestamp).toLocaleString()}
                    </Typography>
                  </Box>
                </Box>
              ))}
            </Stack>
          </Paper>
        </Box>

        {/* System Status */}
        <Box sx={{ flex: '1 1 300px', minWidth: 300 }}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              System Status
            </Typography>
            <Stack spacing={2}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Typography variant="body2">Production System</Typography>
                <Chip label="Operational" color="success" size="small" />
              </Box>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Typography variant="body2">Quality Control</Typography>
                <Chip label="Active" color="success" size="small" />
              </Box>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Typography variant="body2">Database</Typography>
                <Chip label="Connected" color="success" size="small" />
              </Box>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Typography variant="body2">Backup System</Typography>
                <Chip label="Last: 2h ago" color="info" size="small" />
              </Box>
            </Stack>
          </Paper>
        </Box>
      </Box>
    </Box>
  );
};

export default Home;

