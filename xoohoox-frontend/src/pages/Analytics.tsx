import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Paper,
  Card,
  CardContent,
  CircularProgress,
  Alert,
  Chip,
  Stack,
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  LocalDrink as DrinkIcon,
  Science as ScienceIcon,
  Schedule as ScheduleIcon,
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon,
  Error as ErrorIcon,
} from '@mui/icons-material';
import { LineChart, BarChart } from '@mui/x-charts';
import batchService from '../services/batchService';
import qualityService from '../services/qualityService';

interface AnalyticsData {
  totalBatches: number;
  activeBatches: number;
  completedBatches: number;
  averageQualityScore: number;
  productionEfficiency: number;
  monthlyProduction: Array<{ month: string; value: number }>;
  qualityTrends: Array<{ date: string; pass: number; fail: number }>;
  topProducts: Array<{ name: string; quantity: number }>;
}

const Analytics = () => {
  const [data, setData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchAnalyticsData();
  }, []);

  const fetchAnalyticsData = async () => {
    try {
      setLoading(true);
      // Fetch batches for analytics
      const batchesResponse = await batchService.getBatches();
      const qualityResponse = await qualityService.getQualityChecks();

      // Calculate analytics from the data
      const batches = batchesResponse.items;
      const qualityChecks = qualityResponse.items;

      const analyticsData: AnalyticsData = {
        totalBatches: batches.length,
        activeBatches: batches.filter(b => b.status === 'active' || b.status === 'in_progress').length,
        completedBatches: batches.filter(b => b.status === 'completed').length,
        averageQualityScore: qualityChecks.length > 0 
          ? (qualityChecks.filter(q => q.result === 'pass').length / qualityChecks.length) * 100
          : 0,
        productionEfficiency: batches.length > 0 
          ? (batches.filter(b => b.status === 'completed').length / batches.length) * 100
          : 0,
        monthlyProduction: [
          { month: 'Jan', value: 1200 },
          { month: 'Feb', value: 1800 },
          { month: 'Mar', value: 2100 },
          { month: 'Apr', value: 2400 },
          { month: 'May', value: 2800 },
          { month: 'Jun', value: 3200 },
        ],
        qualityTrends: [
          { date: 'Week 1', pass: 85, fail: 15 },
          { date: 'Week 2', pass: 88, fail: 12 },
          { date: 'Week 3', pass: 92, fail: 8 },
          { date: 'Week 4', pass: 90, fail: 10 },
        ],
        topProducts: [
          { name: 'Apple Juice', quantity: 4500 },
          { name: 'Orange Juice', quantity: 3800 },
          { name: 'Grape Juice', quantity: 3200 },
          { name: 'Pineapple Juice', quantity: 2800 },
        ],
      };

      setData(analyticsData);
    } catch (err: any) {
      setError('Failed to fetch analytics data');
      console.error('Error fetching analytics:', err);
    } finally {
      setLoading(false);
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
        <Alert severity="error">{error || 'Failed to load analytics'}</Alert>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Production Analytics
      </Typography>

      {/* Key Metrics */}
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3, mb: 4 }}>
        <Box sx={{ flex: '1 1 200px', minWidth: 200 }}>
          <Paper sx={{ p: 2, textAlign: 'center' }}>
            <DrinkIcon color="primary" sx={{ fontSize: 40, mb: 1 }} />
            <Typography variant="h4" color="primary">
              {data.totalBatches}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Total Batches
            </Typography>
          </Paper>
        </Box>
        <Box sx={{ flex: '1 1 200px', minWidth: 200 }}>
          <Paper sx={{ p: 2, textAlign: 'center' }}>
            <TrendingUpIcon color="success" sx={{ fontSize: 40, mb: 1 }} />
            <Typography variant="h4" color="success.main">
              {data.activeBatches}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Active Batches
            </Typography>
          </Paper>
        </Box>
        <Box sx={{ flex: '1 1 200px', minWidth: 200 }}>
          <Paper sx={{ p: 2, textAlign: 'center' }}>
            <CheckCircleIcon color="info" sx={{ fontSize: 40, mb: 1 }} />
            <Typography variant="h4" color="info.main">
              {data.completedBatches}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Completed Batches
            </Typography>
          </Paper>
        </Box>
        <Box sx={{ flex: '1 1 200px', minWidth: 200 }}>
          <Paper sx={{ p: 2, textAlign: 'center' }}>
            <ScienceIcon color="warning" sx={{ fontSize: 40, mb: 1 }} />
            <Typography variant="h4" color="warning.main">
              {data.averageQualityScore.toFixed(1)}%
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Quality Score
            </Typography>
          </Paper>
        </Box>
      </Box>

      {/* Charts */}
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3 }}>
        <Box sx={{ flex: '1 1 500px', minWidth: 500 }}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Monthly Production
            </Typography>
            <Box sx={{ height: 300 }}>
              <BarChart
                dataset={data.monthlyProduction}
                xAxis={[{ scaleType: 'band', dataKey: 'month' }]}
                series={[{ dataKey: 'value', label: 'Production (Liters)' }]}
                height={300}
              />
            </Box>
          </Paper>
        </Box>
        <Box sx={{ flex: '1 1 500px', minWidth: 500 }}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Quality Trends
            </Typography>
            <Box sx={{ height: 300 }}>
              <LineChart
                dataset={data.qualityTrends}
                xAxis={[{ scaleType: 'band', dataKey: 'date' }]}
                series={[
                  { dataKey: 'pass', label: 'Pass', color: 'green' },
                  { dataKey: 'fail', label: 'Fail', color: 'red' },
                ]}
                height={300}
              />
            </Box>
          </Paper>
        </Box>
      </Box>

      {/* Top Products */}
      <Paper sx={{ p: 3, mt: 3 }}>
        <Typography variant="h6" gutterBottom>
          Top Products by Volume
        </Typography>
        <Stack spacing={2}>
          {data.topProducts.map((product, index) => (
            <Box key={product.name} sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <Chip 
                  label={`#${index + 1}`} 
                  color="primary" 
                  size="small" 
                  sx={{ mr: 2 }}
                />
                <Typography variant="body1">{product.name}</Typography>
              </Box>
              <Typography variant="body1" fontWeight="bold">
                {product.quantity.toLocaleString()} L
              </Typography>
            </Box>
          ))}
        </Stack>
      </Paper>

      {/* Efficiency Metrics */}
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3, mt: 3 }}>
        <Box sx={{ flex: '1 1 400px', minWidth: 400 }}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Production Efficiency
            </Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <Typography variant="h3" color="primary" sx={{ mr: 2 }}>
                {data.productionEfficiency.toFixed(1)}%
              </Typography>
              <Typography variant="body2" color="text.secondary">
                of batches completed successfully
              </Typography>
            </Box>
            <Typography variant="body2" color="text.secondary">
              This represents the percentage of batches that have been completed without issues.
            </Typography>
          </Paper>
        </Box>
        <Box sx={{ flex: '1 1 400px', minWidth: 400 }}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Quality Performance
            </Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <Typography variant="h3" color="success.main" sx={{ mr: 2 }}>
                {data.averageQualityScore.toFixed(1)}%
              </Typography>
              <Typography variant="body2" color="text.secondary">
                quality checks passed
              </Typography>
            </Box>
            <Typography variant="body2" color="text.secondary">
              Average quality score across all production batches.
            </Typography>
          </Paper>
        </Box>
      </Box>
    </Box>
  );
};

export default Analytics; 