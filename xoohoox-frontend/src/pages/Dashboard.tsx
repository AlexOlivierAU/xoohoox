import React, { useState } from 'react';
import {
  Grid,
  Paper,
  Typography,
  Box,
  LinearProgress,
  Button,
  IconButton,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Chip,
  Divider,
  Card,
  CardContent,
  Stack,
} from '@mui/material';
import {
  Add as AddIcon,
  Refresh as RefreshIcon,
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon,
  Schedule as ScheduleIcon,
  TrendingUp as TrendingUpIcon,
  Science as ScienceIcon,
  LocalDrink as DrinkIcon,
} from '@mui/icons-material';
import { BarChart } from '@mui/x-charts';

const Dashboard = () => {
  // Sample data - this would come from your API
  const stats = {
    activeBatches: 5,
    completedToday: 3,
    qualityChecks: 8,
    maintenanceTasks: 4,
  };

  const batches = [
    {
      id: 'B001',
      product: 'Apple Juice',
      progress: 75,
      status: 'In Progress',
      startDate: '2024-04-10',
      stage: 'Fermentation',
      temperature: '22°C',
      pH: 3.5,
    },
    {
      id: 'B002',
      product: 'Orange Juice',
      progress: 30,
      status: 'Warning',
      startDate: '2024-04-11',
      stage: 'Initial Processing',
      temperature: '24°C',
      pH: 4.0,
    },
    {
      id: 'B003',
      product: 'Grape Juice',
      progress: 90,
      status: 'Near Complete',
      startDate: '2024-04-09',
      stage: 'Quality Check',
      temperature: '21°C',
      pH: 3.8,
    },
  ];

  const recentActivities = [
    {
      id: 1,
      type: 'quality_check',
      description: 'Quality check passed for Batch B001',
      time: '10 minutes ago',
      icon: <CheckCircleIcon color="success" />,
    },
    {
      id: 2,
      type: 'warning',
      description: 'Temperature alert for Batch B002',
      time: '30 minutes ago',
      icon: <WarningIcon color="warning" />,
    },
    {
      id: 3,
      type: 'stage_change',
      description: 'Batch B003 entered Quality Check stage',
      time: '1 hour ago',
      icon: <ScienceIcon color="info" />,
    },
  ];

  const productionData = [
    { month: 'Jan', value: 2400 },
    { month: 'Feb', value: 1398 },
    { month: 'Mar', value: 9800 },
    { month: 'Apr', value: 3908 },
  ];

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">Dashboard</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          sx={{ borderRadius: 2 }}
        >
          New Batch
        </Button>
      </Box>

      {/* Stats Overview */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Paper
            sx={{
              p: 3,
              textAlign: 'center',
              backgroundColor: '#3498DB',
              color: 'white',
              borderRadius: 2,
              transition: 'transform 0.2s',
              '&:hover': {
                transform: 'translateY(-4px)',
              },
            }}
          >
            <Typography variant="h4">{stats.activeBatches}</Typography>
            <Typography variant="subtitle1">Active Batches</Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Paper
            sx={{
              p: 3,
              textAlign: 'center',
              backgroundColor: '#2ECC71',
              color: 'white',
              borderRadius: 2,
              transition: 'transform 0.2s',
              '&:hover': {
                transform: 'translateY(-4px)',
              },
            }}
          >
            <Typography variant="h4">{stats.completedToday}</Typography>
            <Typography variant="subtitle1">Completed Today</Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Paper
            sx={{
              p: 3,
              textAlign: 'center',
              backgroundColor: '#E74C3C',
              color: 'white',
              borderRadius: 2,
              transition: 'transform 0.2s',
              '&:hover': {
                transform: 'translateY(-4px)',
              },
            }}
          >
            <Typography variant="h4">{stats.qualityChecks}</Typography>
            <Typography variant="subtitle1">Quality Checks</Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Paper
            sx={{
              p: 3,
              textAlign: 'center',
              backgroundColor: '#F39C12',
              color: 'white',
              borderRadius: 2,
              transition: 'transform 0.2s',
              '&:hover': {
                transform: 'translateY(-4px)',
              },
            }}
          >
            <Typography variant="h4">{stats.maintenanceTasks}</Typography>
            <Typography variant="subtitle1">Maintenance Tasks</Typography>
          </Paper>
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        {/* Active Batches */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3, borderRadius: 2 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
              <Typography variant="h5">Active Batches</Typography>
              <IconButton>
                <RefreshIcon />
              </IconButton>
            </Box>
            <Grid container spacing={3}>
              {batches.map((batch) => (
                <Grid item xs={12} md={6} key={batch.id}>
                  <Card sx={{ height: '100%' }}>
                    <CardContent>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                        <Typography variant="h6">
                          {batch.product}
                        </Typography>
                        <Chip
                          label={batch.status}
                          color={
                            batch.status === 'Warning'
                              ? 'warning'
                              : batch.status === 'Near Complete'
                              ? 'success'
                              : 'primary'
                          }
                          size="small"
                        />
                      </Box>
                      <Typography variant="subtitle2" color="textSecondary" gutterBottom>
                        Batch ID: {batch.id}
                      </Typography>
                      <Stack spacing={1}>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <ScienceIcon fontSize="small" color="action" />
                          <Typography variant="body2">Stage: {batch.stage}</Typography>
                        </Box>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <ScheduleIcon fontSize="small" color="action" />
                          <Typography variant="body2">Started: {batch.startDate}</Typography>
                        </Box>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <DrinkIcon fontSize="small" color="action" />
                          <Typography variant="body2">pH: {batch.pH} | Temp: {batch.temperature}</Typography>
                        </Box>
                      </Stack>
                      <Box sx={{ mt: 2, display: 'flex', alignItems: 'center' }}>
                        <Box sx={{ width: '100%', mr: 1 }}>
                          <LinearProgress
                            variant="determinate"
                            value={batch.progress}
                            sx={{
                              height: 8,
                              borderRadius: 4,
                              backgroundColor: 'rgba(0, 0, 0, 0.1)',
                              '& .MuiLinearProgress-bar': {
                                borderRadius: 4,
                              },
                            }}
                          />
                        </Box>
                        <Box sx={{ minWidth: 35 }}>
                          <Typography variant="body2" color="textSecondary">
                            {`${Math.round(batch.progress)}%`}
                          </Typography>
                        </Box>
                      </Box>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </Paper>
        </Grid>

        {/* Recent Activities */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, borderRadius: 2, height: '100%' }}>
            <Typography variant="h5" gutterBottom>Recent Activities</Typography>
            <List>
              {recentActivities.map((activity, index) => (
                <React.Fragment key={activity.id}>
                  <ListItem>
                    <ListItemIcon>{activity.icon}</ListItemIcon>
                    <ListItemText
                      primary={activity.description}
                      secondary={activity.time}
                    />
                  </ListItem>
                  {index < recentActivities.length - 1 && <Divider />}
                </React.Fragment>
              ))}
            </List>
          </Paper>
        </Grid>

        {/* Production Chart */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3, borderRadius: 2 }}>
            <Typography variant="h5" gutterBottom>Production Overview</Typography>
            <Box sx={{ width: '100%', height: 300 }}>
              <BarChart
                xAxis={[{ scaleType: 'band', data: productionData.map(d => d.month) }]}
                series={[{ data: productionData.map(d => d.value) }]}
                height={300}
              />
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard; 