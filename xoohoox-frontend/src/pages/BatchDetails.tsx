import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Chip,
  LinearProgress,
  Button,
  IconButton,
  Tooltip,
  Alert,
  CircularProgress,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
} from '@mui/material';
import {
  ArrowBack as ArrowBackIcon,
  Edit as EditIcon,
  PlayArrow as PlayIcon,
  Pause as PauseIcon,
  Stop as StopIcon,
  Science as ScienceIcon,
  LocalDrink as DrinkIcon,
  TrendingUp as TrendingUpIcon,
  Schedule as ScheduleIcon,
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon,
  Error as ErrorIcon,
} from '@mui/icons-material';
import { useParams, useNavigate } from 'react-router-dom';
import batchService from '../services/batchService';

import { Batch } from '../services/batchService';

interface BatchDetails extends Batch {
  // Additional properties specific to detailed view
}

const BatchDetails = () => {
  const { batchId } = useParams<{ batchId: string }>();
  const navigate = useNavigate();
  const [batch, setBatch] = useState<BatchDetails | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (batchId) {
      fetchBatchDetails();
    }
  }, [batchId]);

  const fetchBatchDetails = async () => {
    try {
      setLoading(true);
      const response = await batchService.getBatch(batchId!);
      setBatch(response);
    } catch (err: any) {
      setError('Failed to fetch batch details');
      console.error('Error fetching batch details:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleStatusChange = async (newStatus: string) => {
    try {
      await batchService.updateBatchStatus(batchId!, newStatus);
      fetchBatchDetails();
    } catch (err: any) {
      setError('Failed to update batch status');
    }
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'active':
      case 'in_progress':
        return 'primary';
      case 'completed':
        return 'success';
      case 'paused':
        return 'warning';
      case 'cancelled':
        return 'error';
      default:
        return 'default';
    }
  };

  const getStageIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircleIcon color="success" />;
      case 'in_progress':
        return <TrendingUpIcon color="primary" />;
      case 'pending':
        return <ScheduleIcon color="disabled" />;
      default:
        return <ScheduleIcon />;
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error || !batch) {
    return (
      <Box sx={{ p: 3 }}>
        <Alert severity="error">{error || 'Batch not found'}</Alert>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
        <IconButton onClick={() => navigate('/batches')} sx={{ mr: 2 }}>
          <ArrowBackIcon />
        </IconButton>
        <Box sx={{ flexGrow: 1 }}>
          <Typography variant="h4" component="h1">
            Batch {batch.batch_id}
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            {batch.fruit_type}
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Tooltip title="Edit Batch">
            <IconButton onClick={() => navigate(`/batches/${batchId}/edit`)}>
              <EditIcon />
            </IconButton>
          </Tooltip>
          {batch.status === 'active' && (
            <Tooltip title="Pause Batch">
              <IconButton onClick={() => handleStatusChange('paused')}>
                <PauseIcon />
              </IconButton>
            </Tooltip>
          )}
          {batch.status === 'paused' && (
            <Tooltip title="Resume Batch">
              <IconButton onClick={() => handleStatusChange('active')}>
                <PlayIcon />
              </IconButton>
            </Tooltip>
          )}
          <Tooltip title="Stop Batch">
            <IconButton 
              color="error"
              onClick={() => handleStatusChange('cancelled')}
            >
              <StopIcon />
            </IconButton>
          </Tooltip>
        </Box>
      </Box>

      <Box sx={{ display: 'flex', gap: 3, flexWrap: 'wrap' }}>
        {/* Main Info Card */}
        <Box sx={{ flex: '1 1 600px' }}>
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Batch Information
            </Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
              <Box sx={{ minWidth: 200 }}>
                <Typography variant="body2" color="text.secondary">
                  Status
                </Typography>
                <Chip
                  label={batch.status}
                  color={getStatusColor(batch.status) as any}
                  sx={{ mt: 1 }}
                />
              </Box>
              <Box sx={{ minWidth: 200 }}>
                <Typography variant="body2" color="text.secondary">
                  Current Stage
                </Typography>
                <Typography variant="body1" sx={{ mt: 1 }}>
                  {batch.current_stage}
                </Typography>
              </Box>
              <Box sx={{ minWidth: 200 }}>
                <Typography variant="body2" color="text.secondary">
                  Progress
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                  <LinearProgress
                    variant="determinate"
                    value={batch.progress}
                    sx={{ flexGrow: 1, mr: 1 }}
                  />
                  <Typography variant="body2">
                    {batch.progress}%
                  </Typography>
                </Box>
              </Box>
              <Box sx={{ minWidth: 200 }}>
                <Typography variant="body2" color="text.secondary">
                  Quantity
                </Typography>
                <Typography variant="body1" sx={{ mt: 1 }}>
                  {batch.quantity} {batch.unit}
                </Typography>
              </Box>
            </Box>
            
            <Divider sx={{ my: 2 }} />
            
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
              <Box sx={{ minWidth: 200 }}>
                <Typography variant="body2" color="text.secondary">
                  Start Date
                </Typography>
                <Typography variant="body1" sx={{ mt: 1 }}>
                  {new Date(batch.start_date).toLocaleDateString()}
                </Typography>
              </Box>
              <Box sx={{ minWidth: 200 }}>
                <Typography variant="body2" color="text.secondary">
                  Expected Completion
                </Typography>
                <Typography variant="body1" sx={{ mt: 1 }}>
                  {new Date(batch.expected_completion).toLocaleDateString()}
                </Typography>
              </Box>
            </Box>
          </Paper>

          {/* Process Stages */}
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Process Stages
            </Typography>
            <List>
              {batch.stages?.map((stage, index) => (
                <ListItem key={stage.name}>
                  <ListItemIcon>
                    {getStageIcon(stage.status)}
                  </ListItemIcon>
                  <ListItemText
                    primary={stage.name}
                    secondary={
                      <Box>
                        <Typography variant="body2" color="text.secondary">
                          {stage.status === 'completed' ? 'Completed' : 
                           stage.status === 'in_progress' ? 'In Progress' : 'Pending'}
                        </Typography>
                        {stage.start_date && (
                          <Typography variant="caption" color="text.secondary">
                            Started: {new Date(stage.start_date).toLocaleDateString()}
                          </Typography>
                        )}
                      </Box>
                    }
                  />
                </ListItem>
              ))}
            </List>
          </Paper>
        </Box>

        {/* Parameters Card */}
        <Box sx={{ flex: '0 1 300px' }}>
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Current Parameters
            </Typography>
            <List>
              <ListItem>
                <ListItemIcon>
                  <ScienceIcon />
                </ListItemIcon>
                <ListItemText
                  primary="Temperature"
                  secondary={`${batch.temperature}°C`}
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <DrinkIcon />
                </ListItemIcon>
                <ListItemText
                  primary="pH Level"
                  secondary={batch.ph_level}
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <TrendingUpIcon />
                </ListItemIcon>
                <ListItemText
                  primary="Brix Level"
                  secondary={`${batch.brix_level}°Bx`}
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <DrinkIcon />
                </ListItemIcon>
                <ListItemText
                  primary="Alcohol Content"
                  secondary={`${batch.alcohol_content}%`}
                />
              </ListItem>
            </List>
          </Paper>

          {/* Quality Checks */}
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Recent Quality Checks
            </Typography>
            <List>
              {batch.quality_checks?.slice(0, 5).map((check) => (
                <ListItem key={check.id}>
                  <ListItemIcon>
                    {check.result === 'pass' ? (
                      <CheckCircleIcon color="success" />
                    ) : check.result === 'warning' ? (
                      <WarningIcon color="warning" />
                    ) : (
                      <ErrorIcon color="error" />
                    )}
                  </ListItemIcon>
                  <ListItemText
                    primary={check.check_type}
                    secondary={`${check.result} - ${new Date(check.timestamp).toLocaleString()}`}
                  />
                </ListItem>
              ))}
            </List>
            {batch.quality_checks && batch.quality_checks.length > 5 && (
              <Button
                fullWidth
                variant="outlined"
                onClick={() => navigate(`/batches/${batchId}/quality-checks`)}
              >
                View All Quality Checks
              </Button>
            )}
          </Paper>
        </Box>
      </Box>

      {/* Notes */}
      {batch.notes && (
        <Paper sx={{ p: 3, mt: 3 }}>
          <Typography variant="h6" gutterBottom>
            Notes
          </Typography>
          <Typography variant="body1">
            {batch.notes}
          </Typography>
        </Paper>
      )}
    </Box>
  );
};

export default BatchDetails;
