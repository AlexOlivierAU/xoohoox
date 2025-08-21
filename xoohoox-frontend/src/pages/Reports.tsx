import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Stack,
  Chip,
  Alert,
  CircularProgress,
  Card,
  CardContent,
  Grid,
} from '@mui/material';
import {
  Download as DownloadIcon,
  Print as PrintIcon,
  Email as EmailIcon,
  Assessment as AssessmentIcon,
  TrendingUp as TrendingUpIcon,
  LocalDrink as DrinkIcon,
  Science as ScienceIcon,
  Schedule as ScheduleIcon,
} from '@mui/icons-material';
import batchService from '../services/batchService';
import qualityService from '../services/qualityService';

interface ReportData {
  productionSummary: {
    totalBatches: number;
    completedBatches: number;
    totalVolume: number;
    averageEfficiency: number;
  };
  qualityMetrics: {
    totalChecks: number;
    passedChecks: number;
    failedChecks: number;
    averageScore: number;
  };
  topProducts: Array<{
    name: string;
    quantity: number;
    efficiency: number;
  }>;
  monthlyTrends: Array<{
    month: string;
    production: number;
    quality: number;
  }>;
}

const Reports = () => {
  const [data, setData] = useState<ReportData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [reportType, setReportType] = useState('production');
  const [dateRange, setDateRange] = useState('last30');

  useEffect(() => {
    fetchReportData();
  }, [reportType, dateRange]);

  const fetchReportData = async () => {
    try {
      setLoading(true);
      const batchesResponse = await batchService.getBatches();
      const qualityResponse = await qualityService.getQualityChecks();

      const batches = batchesResponse.items;
      const qualityChecks = qualityResponse.items;

      const reportData: ReportData = {
        productionSummary: {
          totalBatches: batches.length,
          completedBatches: batches.filter(b => b.status === 'completed').length,
          totalVolume: batches.reduce((sum, b) => sum + (b.quantity || 0), 0),
          averageEfficiency: batches.length > 0 
            ? (batches.filter(b => b.status === 'completed').length / batches.length) * 100
            : 0,
        },
        qualityMetrics: {
          totalChecks: qualityChecks.length,
          passedChecks: qualityChecks.filter(q => q.result === 'pass').length,
          failedChecks: qualityChecks.filter(q => q.result === 'fail').length,
          averageScore: qualityChecks.length > 0 
            ? (qualityChecks.filter(q => q.result === 'pass').length / qualityChecks.length) * 100
            : 0,
        },
        topProducts: [
          { name: 'Apple Juice', quantity: 4500, efficiency: 95.2 },
          { name: 'Orange Juice', quantity: 3800, efficiency: 92.8 },
          { name: 'Grape Juice', quantity: 3200, efficiency: 89.5 },
          { name: 'Pineapple Juice', quantity: 2800, efficiency: 87.3 },
        ],
        monthlyTrends: [
          { month: 'Jan', production: 1200, quality: 88 },
          { month: 'Feb', production: 1800, quality: 91 },
          { month: 'Mar', production: 2100, quality: 93 },
          { month: 'Apr', production: 2400, quality: 94 },
          { month: 'May', production: 2800, quality: 95 },
          { month: 'Jun', production: 3200, quality: 96 },
        ],
      };

      setData(reportData);
    } catch (err: any) {
      setError('Failed to fetch report data');
      console.error('Error fetching report data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleExport = (format: 'pdf' | 'excel' | 'csv') => {
    // Mock export functionality
    console.log(`Exporting ${reportType} report as ${format}`);
    alert(`Exporting ${reportType} report as ${format.toUpperCase()}`);
  };

  const handlePrint = () => {
    window.print();
  };

  const handleEmail = () => {
    // Mock email functionality
    alert('Report sent via email');
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
        <Alert severity="error">{error || 'Failed to load report data'}</Alert>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Reports & Analytics
      </Typography>

      {/* Report Controls */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Stack direction="row" spacing={2} alignItems="center" sx={{ mb: 3 }}>
          <FormControl sx={{ minWidth: 200 }}>
            <InputLabel>Report Type</InputLabel>
            <Select
              value={reportType}
              label="Report Type"
              onChange={(e) => setReportType(e.target.value)}
            >
              <MenuItem value="production">Production Report</MenuItem>
              <MenuItem value="quality">Quality Report</MenuItem>
              <MenuItem value="efficiency">Efficiency Report</MenuItem>
              <MenuItem value="comprehensive">Comprehensive Report</MenuItem>
            </Select>
          </FormControl>

          <FormControl sx={{ minWidth: 200 }}>
            <InputLabel>Date Range</InputLabel>
            <Select
              value={dateRange}
              label="Date Range"
              onChange={(e) => setDateRange(e.target.value)}
            >
              <MenuItem value="last7">Last 7 Days</MenuItem>
              <MenuItem value="last30">Last 30 Days</MenuItem>
              <MenuItem value="last90">Last 90 Days</MenuItem>
              <MenuItem value="lastYear">Last Year</MenuItem>
            </Select>
          </FormControl>

          <Button
            variant="contained"
            startIcon={<DownloadIcon />}
            onClick={() => handleExport('pdf')}
          >
            Export PDF
          </Button>
          <Button
            variant="outlined"
            startIcon={<DownloadIcon />}
            onClick={() => handleExport('excel')}
          >
            Export Excel
          </Button>
          <Button
            variant="outlined"
            startIcon={<PrintIcon />}
            onClick={handlePrint}
          >
            Print
          </Button>
          <Button
            variant="outlined"
            startIcon={<EmailIcon />}
            onClick={handleEmail}
          >
            Email
          </Button>
        </Stack>
      </Paper>

      {/* Summary Cards */}
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3, mb: 4 }}>
        <Box sx={{ flex: '1 1 200px', minWidth: 200 }}>
          <Card>
            <CardContent sx={{ textAlign: 'center' }}>
              <DrinkIcon color="primary" sx={{ fontSize: 40, mb: 1 }} />
              <Typography variant="h4" color="primary">
                {data.productionSummary.totalBatches}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Total Batches
              </Typography>
            </CardContent>
          </Card>
        </Box>
        <Box sx={{ flex: '1 1 200px', minWidth: 200 }}>
          <Card>
            <CardContent sx={{ textAlign: 'center' }}>
              <TrendingUpIcon color="success" sx={{ fontSize: 40, mb: 1 }} />
              <Typography variant="h4" color="success.main">
                {data.productionSummary.totalVolume.toLocaleString()}L
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Total Production
              </Typography>
            </CardContent>
          </Card>
        </Box>
        <Box sx={{ flex: '1 1 200px', minWidth: 200 }}>
          <Card>
            <CardContent sx={{ textAlign: 'center' }}>
              <ScienceIcon color="info" sx={{ fontSize: 40, mb: 1 }} />
              <Typography variant="h4" color="info.main">
                {data.qualityMetrics.averageScore.toFixed(1)}%
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Quality Score
              </Typography>
            </CardContent>
          </Card>
        </Box>
        <Box sx={{ flex: '1 1 200px', minWidth: 200 }}>
          <Card>
            <CardContent sx={{ textAlign: 'center' }}>
              <ScheduleIcon color="warning" sx={{ fontSize: 40, mb: 1 }} />
              <Typography variant="h4" color="warning.main">
                {data.productionSummary.averageEfficiency.toFixed(1)}%
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Efficiency Rate
              </Typography>
            </CardContent>
          </Card>
        </Box>
      </Box>

      {/* Detailed Reports */}
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3 }}>
        {/* Top Products */}
        <Box sx={{ flex: '1 1 500px', minWidth: 500 }}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Top Products by Volume
            </Typography>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Product</TableCell>
                    <TableCell align="right">Volume (L)</TableCell>
                    <TableCell align="right">Efficiency (%)</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {data.topProducts.map((product) => (
                    <TableRow key={product.name}>
                      <TableCell>{product.name}</TableCell>
                      <TableCell align="right">{product.quantity.toLocaleString()}</TableCell>
                      <TableCell align="right">{product.efficiency}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>
        </Box>

        {/* Monthly Trends */}
        <Box sx={{ flex: '1 1 500px', minWidth: 500 }}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Monthly Trends
            </Typography>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Month</TableCell>
                    <TableCell align="right">Production (L)</TableCell>
                    <TableCell align="right">Quality Score (%)</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {data.monthlyTrends.map((trend) => (
                    <TableRow key={trend.month}>
                      <TableCell>{trend.month}</TableCell>
                      <TableCell align="right">{trend.production.toLocaleString()}</TableCell>
                      <TableCell align="right">{trend.quality}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>
        </Box>
      </Box>

      {/* Quality Metrics */}
      <Paper sx={{ p: 3, mt: 3 }}>
        <Typography variant="h6" gutterBottom>
          Quality Control Summary
        </Typography>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2, mb: 3 }}>
          <Chip 
            label={`Total Checks: ${data.qualityMetrics.totalChecks}`} 
            color="primary" 
          />
          <Chip 
            label={`Passed: ${data.qualityMetrics.passedChecks}`} 
            color="success" 
          />
          <Chip 
            label={`Failed: ${data.qualityMetrics.failedChecks}`} 
            color="error" 
          />
          <Chip 
            label={`Success Rate: ${data.qualityMetrics.averageScore.toFixed(1)}%`} 
            color="info" 
          />
        </Box>
      </Paper>
    </Box>
  );
};

export default Reports; 