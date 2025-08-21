import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Paper,
  Tabs,
  Tab,
  Button,
  CircularProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  IconButton,
  Tooltip,
  Alert,
} from '@mui/material';
import {
  Info as InfoIcon,
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon,
  Pause as PauseIcon,
  Add as AddIcon,
} from '@mui/icons-material';
import axios from '../api/axios';
import BatchJourneyTimeline from '../components/BatchJourneyTimeline';

// Define the stage types
type Stage = 'arrival' | 'prep' | 'heat' | 'ferment' | 'distill';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`batch-tabpanel-${index}`}
      aria-labelledby={`batch-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

interface Batch {
  id: number;
  batch_id: string;
  name: string;
  status: string;
  stage: string;
  start_date: string;
  end_date: string;
  progress: number;
}

interface Trial {
  id: number;
  trial_id: string;
  juice_variant: string;
  yeast_strain: string;
  current_abv: number;
  status: string;
  path_taken: string | null;
}

export const BatchDetails: React.FC = () => {
  const { batchId } = useParams<{ batchId: string }>();
  const navigate = useNavigate();
  const [batch, setBatch] = useState<Batch | null>(null);
  const [trials, setTrials] = useState<Trial[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [tabValue, setTabValue] = useState(0);
  const [eventLog, setEventLog] = useState<any[]>([]);

  useEffect(() => {
    const fetchBatchData = async () => {
      try {
        setLoading(true);
        setError(null);
        console.log('Fetching batch data for ID:', batchId);
        
        // Fetch batch details
        const batchResponse = await axios.get(`/api/v1/batches/${batchId}`);
        console.log('Batch response:', batchResponse.data);
        setBatch(batchResponse.data);
        
        // Fetch trials for this batch
        const trialsResponse = await axios.get(`/api/v1/fermentation-trials/batch/${batchId}`);
        console.log('Trials response:', trialsResponse.data);
        setTrials(trialsResponse.data.trials || []);
        
        // Mock event log for now
        setEventLog([
          {
            stage: 'arrival' as Stage,
            message: 'Batch received and initial inspection completed',
            timestamp: new Date().toISOString()
          },
          {
            stage: 'prep' as Stage,
            message: 'Chemistry analysis started',
            timestamp: new Date(Date.now() - 86400000).toISOString()
          },
          {
            stage: 'heat' as Stage,
            message: 'Heat activation process initiated',
            timestamp: new Date(Date.now() - 172800000).toISOString()
          }
        ]);
      } catch (error) {
        console.error('Error fetching batch data:', error);
        setError(error instanceof Error ? error.message : 'An error occurred while fetching batch data');
      } finally {
        setLoading(false);
      }
    };

    if (batchId) {
      fetchBatchData();
    }
  }, [batchId]);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleViewTrial = (trialId: string) => {
    navigate(`/trials/${trialId}`);
  };

  const getStatusIcon = (status: string) => {
    switch (status.toLowerCase()) {
      case 'fermenting':
        return <CheckCircleIcon color="success" />;
      case 'paused':
        return <PauseIcon color="warning" />;
      case 'failed':
        return <WarningIcon color="error" />;
      default:
        return <InfoIcon />;
    }
  };

  const getPathColor = (path: string | null) => {
    if (!path) return 'default';
    switch (path.toLowerCase()) {
      case 'vinegar':
        return 'warning';
      case 'distillation':
        return 'primary';
      case 'archived':
        return 'default';
      default:
        return 'default';
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ p: 3 }}>
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
        <Button variant="contained" onClick={() => navigate('/')}>
          Back to Dashboard
        </Button>
      </Box>
    );
  }

  if (!batch) {
    return (
      <Box sx={{ p: 3 }}>
        <Alert severity="warning" sx={{ mb: 2 }}>
          Batch not found
        </Alert>
        <Button variant="contained" onClick={() => navigate('/')}>
          Back to Dashboard
        </Button>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Batch: {batch.name}
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" gutterBottom>
        ID: {batch.batch_id}
      </Typography>

      <Paper sx={{ width: '100%', mb: 3 }}>
        <Tabs
          value={tabValue}
          onChange={handleTabChange}
          indicatorColor="primary"
          textColor="primary"
          variant="fullWidth"
        >
          <Tab label="Overview" />
          <Tab label="Trials" />
          <Tab label="Timeline" />
        </Tabs>

        <TabPanel value={tabValue} index={0}>
          <Box sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>Batch Information</Typography>
            <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))', gap: 2 }}>
              <Box>
                <Typography variant="subtitle2" color="text.secondary">Status</Typography>
                <Typography variant="body1">{batch.status}</Typography>
              </Box>
              <Box>
                <Typography variant="subtitle2" color="text.secondary">Stage</Typography>
                <Typography variant="body1">{batch.stage}</Typography>
              </Box>
              <Box>
                <Typography variant="subtitle2" color="text.secondary">Start Date</Typography>
                <Typography variant="body1">{new Date(batch.start_date).toLocaleDateString()}</Typography>
              </Box>
              <Box>
                <Typography variant="subtitle2" color="text.secondary">End Date</Typography>
                <Typography variant="body1">{new Date(batch.end_date).toLocaleDateString()}</Typography>
              </Box>
              <Box>
                <Typography variant="subtitle2" color="text.secondary">Progress</Typography>
                <Box sx={{ width: '100%', bgcolor: 'background.paper', borderRadius: 1, overflow: 'hidden' }}>
                  <Box
                    sx={{
                      width: `${batch.progress}%`,
                      height: 8,
                      bgcolor: 'primary.main',
                    }}
                  />
                </Box>
              </Box>
            </Box>
          </Box>
        </TabPanel>

        <TabPanel value={tabValue} index={1}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h6">Fermentation Trials</Typography>
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              size="small"
            >
              New Trial
            </Button>
          </Box>
          
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Trial ID</TableCell>
                  <TableCell>Juice Type</TableCell>
                  <TableCell>Yeast</TableCell>
                  <TableCell align="right">ABV</TableCell>
                  <TableCell>Path</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell align="center">Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {trials.length > 0 ? (
                  trials.map((trial) => (
                    <TableRow key={trial.id}>
                      <TableCell>
                        <Typography variant="body2" fontFamily="monospace">
                          {trial.trial_id}
                        </Typography>
                      </TableCell>
                      <TableCell>{trial.juice_variant}</TableCell>
                      <TableCell>{trial.yeast_strain}</TableCell>
                      <TableCell align="right">{trial.current_abv.toFixed(1)}%</TableCell>
                      <TableCell>
                        {trial.path_taken ? (
                          <Chip
                            label={trial.path_taken}
                            color={getPathColor(trial.path_taken) as any}
                            size="small"
                          />
                        ) : (
                          '—'
                        )}
                      </TableCell>
                      <TableCell>
                        <Tooltip title={trial.status}>
                          <span>{getStatusIcon(trial.status)}</span>
                        </Tooltip>
                      </TableCell>
                      <TableCell align="center">
                        <Button
                          variant="outlined"
                          size="small"
                          onClick={() => handleViewTrial(trial.trial_id)}
                        >
                          View Trial
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))
                ) : (
                  <TableRow>
                    <TableCell colSpan={7} align="center">
                      No trials found for this batch
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </TableContainer>
        </TabPanel>

        <TabPanel value={tabValue} index={2}>
          <BatchJourneyTimeline
            batchId={batch.batch_id}
            currentStage="ferment"
            eventLog={eventLog}
          />
        </TabPanel>
      </Paper>
    </Box>
  );
};
