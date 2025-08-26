import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  TextField,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  Alert,
  CircularProgress,
  Card,
  CardContent,
  LinearProgress,
  Tooltip,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Science as ScienceIcon,
  TrendingUp as TrendingUpIcon,
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon,
  Schedule as ScheduleIcon,
  LocalDrink as DrinkIcon,
} from '@mui/icons-material';

interface FermentationTrial {
  id: string;
  trial_id: string;
  batch_id: string;
  yeast_strain: string;
  fruit_type: string;
  initial_sg: number;
  current_sg: number;
  target_sg: number;
  temperature: number;
  ph: number;
  alcohol_content: number;
  status: 'active' | 'completed' | 'failed' | 'paused';
  start_date: string;
  end_date?: string;
  notes?: string;
  aroma_score: number;
  flocculation: 'high' | 'medium' | 'low';
  fermentation_rate: number;
  created_by: string;
}

interface TrialCreate {
  batch_id: string;
  yeast_strain: string;
  fruit_type: string;
  initial_sg: number;
  target_sg: number;
  temperature: number;
  ph: number;
  notes?: string;
}

export default function FermentationTrials() {
  const [openDialog, setOpenDialog] = useState(false);
  const [trials, setTrials] = useState<FermentationTrial[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [editingTrial, setEditingTrial] = useState<FermentationTrial | null>(null);

  const [newTrial, setNewTrial] = useState<Partial<TrialCreate>>({
    batch_id: '',
    yeast_strain: '',
    fruit_type: '',
    initial_sg: 1.080,
    target_sg: 1.020,
    temperature: 22,
    ph: 4.5,
    notes: '',
  });

  const yeastStrains = [
    'Saccharomyces cerevisiae - EC1118',
    'Saccharomyces cerevisiae - D47',
    'Saccharomyces cerevisiae - 71B',
    'Saccharomyces bayanus - Premier Cuvee',
    'Saccharomyces cerevisiae - Red Star Premier Blanc',
    'Saccharomyces cerevisiae - Lalvin ICV-D254',
    'Saccharomyces cerevisiae - Lalvin RC212',
    'Saccharomyces cerevisiae - Lalvin BM4x4'
  ];

  const fruitTypes = [
    'Lemon', 'Lime', 'Orange', 'Grapefruit', 'Apple', 'Grape', 'Pineapple', 'Mango', 'Mixed Citrus'
  ];

  useEffect(() => {
    fetchTrials();
  }, []);

  const fetchTrials = async () => {
    try {
      setLoading(true);
      // Mock data for now
      const mockTrials: FermentationTrial[] = [
        {
          id: '1',
          trial_id: 'T-001-01',
          batch_id: 'B-2024-001',
          yeast_strain: 'Saccharomyces cerevisiae - EC1118',
          fruit_type: 'Lemon',
          initial_sg: 1.080,
          current_sg: 1.045,
          target_sg: 1.020,
          temperature: 22,
          ph: 4.2,
          alcohol_content: 4.6,
          status: 'active',
          start_date: '2024-04-10',
          notes: 'Strong fermentation, good aroma development',
          aroma_score: 8.5,
          flocculation: 'high',
          fermentation_rate: 0.85,
          created_by: 'John Smith'
        },
        {
          id: '2',
          trial_id: 'T-001-02',
          batch_id: 'B-2024-001',
          yeast_strain: 'Saccharomyces cerevisiae - D47',
          fruit_type: 'Lemon',
          initial_sg: 1.080,
          current_sg: 1.015,
          target_sg: 1.020,
          temperature: 22,
          ph: 4.0,
          alcohol_content: 8.5,
          status: 'completed',
          start_date: '2024-04-10',
          end_date: '2024-04-15',
          notes: 'Excellent fermentation, high alcohol tolerance',
          aroma_score: 9.2,
          flocculation: 'medium',
          fermentation_rate: 1.0,
          created_by: 'Sarah Johnson'
        },
        {
          id: '3',
          trial_id: 'T-002-01',
          batch_id: 'B-2024-002',
          yeast_strain: 'Saccharomyces bayanus - Premier Cuvee',
          fruit_type: 'Orange',
          initial_sg: 1.075,
          current_sg: 1.060,
          target_sg: 1.025,
          temperature: 24,
          ph: 4.5,
          alcohol_content: 2.0,
          status: 'active',
          start_date: '2024-04-12',
          notes: 'Slow start, monitoring closely',
          aroma_score: 6.8,
          flocculation: 'low',
          fermentation_rate: 0.4,
          created_by: 'Mike Wilson'
        },
        {
          id: '4',
          trial_id: 'T-003-01',
          batch_id: 'B-2024-003',
          yeast_strain: 'Saccharomyces cerevisiae - 71B',
          fruit_type: 'Apple',
          initial_sg: 1.085,
          current_sg: 1.030,
          target_sg: 1.020,
          temperature: 21,
          ph: 4.3,
          alcohol_content: 7.2,
          status: 'active',
          start_date: '2024-04-08',
          notes: 'Good fermentation, nice apple character',
          aroma_score: 8.8,
          flocculation: 'high',
          fermentation_rate: 0.92,
          created_by: 'Lisa Chen'
        }
      ];
      setTrials(mockTrials);
    } catch (err: any) {
      setError('Failed to fetch fermentation trials');
      console.error('Error fetching trials:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTrial = async () => {
    if (newTrial.batch_id && newTrial.yeast_strain && newTrial.fruit_type) {
      try {
        const trial: FermentationTrial = {
          id: Date.now().toString(),
          trial_id: `T-${newTrial.batch_id}-${Math.floor(Math.random() * 100).toString().padStart(2, '0')}`,
          batch_id: newTrial.batch_id!,
          yeast_strain: newTrial.yeast_strain!,
          fruit_type: newTrial.fruit_type!,
          initial_sg: newTrial.initial_sg!,
          current_sg: newTrial.initial_sg!,
          target_sg: newTrial.target_sg!,
          temperature: newTrial.temperature!,
          ph: newTrial.ph!,
          alcohol_content: 0,
          status: 'active',
          start_date: new Date().toISOString().split('T')[0],
          notes: newTrial.notes,
          aroma_score: 0,
          flocculation: 'low',
          fermentation_rate: 0,
          created_by: 'Current User'
        };
        
        setTrials([...trials, trial]);
        setOpenDialog(false);
        resetForm();
      } catch (err: any) {
        setError('Failed to create trial');
        console.error('Error creating trial:', err);
      }
    }
  };

  const handleUpdateTrial = async () => {
    if (editingTrial && newTrial.batch_id && newTrial.yeast_strain && newTrial.fruit_type) {
      try {
        const updatedTrial = {
          ...editingTrial,
          ...newTrial,
        };
        
        setTrials(trials.map(t => t.id === editingTrial.id ? updatedTrial : t));
        setOpenDialog(false);
        setEditingTrial(null);
        resetForm();
      } catch (err: any) {
        setError('Failed to update trial');
        console.error('Error updating trial:', err);
      }
    }
  };

  const handleDeleteTrial = async (trialId: string) => {
    try {
      setTrials(trials.filter(t => t.id !== trialId));
    } catch (err: any) {
      setError('Failed to delete trial');
      console.error('Error deleting trial:', err);
    }
  };

  const resetForm = () => {
    setNewTrial({
      batch_id: '',
      yeast_strain: '',
      fruit_type: '',
      initial_sg: 1.080,
      target_sg: 1.020,
      temperature: 22,
      ph: 4.5,
      notes: '',
    });
  };

  const openEditDialog = (trial: FermentationTrial) => {
    setEditingTrial(trial);
    setNewTrial({
      batch_id: trial.batch_id,
      yeast_strain: trial.yeast_strain,
      fruit_type: trial.fruit_type,
      initial_sg: trial.initial_sg,
      target_sg: trial.target_sg,
      temperature: trial.temperature,
      ph: trial.ph,
      notes: trial.notes,
    });
    setOpenDialog(true);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'primary';
      case 'completed':
        return 'success';
      case 'failed':
        return 'error';
      case 'paused':
        return 'warning';
      default:
        return 'default';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active':
        return <TrendingUpIcon />;
      case 'completed':
        return <CheckCircleIcon />;
      case 'failed':
        return <WarningIcon />;
      case 'paused':
        return <ScheduleIcon />;
      default:
        return <ScienceIcon />;
    }
  };

  const calculateProgress = (trial: FermentationTrial) => {
    const total = trial.initial_sg - trial.target_sg;
    const completed = trial.initial_sg - trial.current_sg;
    return Math.min(100, Math.max(0, (completed / total) * 100));
  };

  const getFlocculationColor = (flocculation: string) => {
    switch (flocculation) {
      case 'high':
        return 'success';
      case 'medium':
        return 'warning';
      case 'low':
        return 'error';
      default:
        return 'default';
    }
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">Fermentation Trials</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => {
            setEditingTrial(null);
            resetForm();
            setOpenDialog(true);
          }}
        >
          New Trial
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {/* Summary Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Trials
              </Typography>
              <Typography variant="h4">
                {trials.length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Active Trials
              </Typography>
              <Typography variant="h4">
                {trials.filter(t => t.status === 'active').length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Completed
              </Typography>
              <Typography variant="h4">
                {trials.filter(t => t.status === 'completed').length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Avg Aroma Score
              </Typography>
              <Typography variant="h4">
                {(trials.reduce((acc, t) => acc + t.aroma_score, 0) / trials.length).toFixed(1)}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Trials Table */}
      <Paper sx={{ p: 2 }}>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Trial ID</TableCell>
                <TableCell>Batch</TableCell>
                <TableCell>Yeast Strain</TableCell>
                <TableCell>Fruit Type</TableCell>
                <TableCell>Progress</TableCell>
                <TableCell>Current SG</TableCell>
                <TableCell>Alcohol %</TableCell>
                <TableCell>Temperature</TableCell>
                <TableCell>pH</TableCell>
                <TableCell>Aroma Score</TableCell>
                <TableCell>Flocculation</TableCell>
                <TableCell>Status</TableCell>
                <TableCell align="center">Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {trials.map((trial) => (
                <TableRow key={trial.id} hover>
                  <TableCell>
                    <Typography variant="subtitle2" fontWeight="bold">
                      {trial.trial_id}
                    </Typography>
                  </TableCell>
                  <TableCell>{trial.batch_id}</TableCell>
                  <TableCell>
                    <Typography variant="body2">
                      {trial.yeast_strain.split(' - ')[1]}
                    </Typography>
                    <Typography variant="caption" color="textSecondary">
                      {trial.yeast_strain.split(' - ')[0]}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={trial.fruit_type}
                      size="small"
                      variant="outlined"
                    />
                  </TableCell>
                  <TableCell>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Box sx={{ width: '100%', mr: 1 }}>
                        <LinearProgress
                          variant="determinate"
                          value={calculateProgress(trial)}
                          sx={{ height: 8, borderRadius: 4 }}
                        />
                      </Box>
                      <Typography variant="caption">
                        {calculateProgress(trial).toFixed(0)}%
                      </Typography>
                    </Box>
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2" fontWeight="bold">
                      {trial.current_sg.toFixed(3)}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2" fontWeight="bold">
                      {trial.alcohol_content.toFixed(1)}%
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2">
                      {trial.temperature}°C
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2">
                      {trial.ph.toFixed(1)}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2" fontWeight="bold">
                      {trial.aroma_score}/10
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={trial.flocculation}
                      color={getFlocculationColor(trial.flocculation) as any}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                      {getStatusIcon(trial.status)}
                      <Chip
                        label={trial.status}
                        color={getStatusColor(trial.status) as any}
                        size="small"
                      />
                    </Box>
                  </TableCell>
                  <TableCell align="center">
                    <IconButton size="small" onClick={() => openEditDialog(trial)}>
                      <EditIcon />
                    </IconButton>
                    <IconButton size="small" color="error" onClick={() => handleDeleteTrial(trial.id)}>
                      <DeleteIcon />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>

      {/* Add/Edit Trial Dialog */}
      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>
          {editingTrial ? 'Edit Fermentation Trial' : 'New Fermentation Trial'}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ mt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Batch ID"
                  value={newTrial.batch_id}
                  onChange={(e) => setNewTrial({ ...newTrial, batch_id: e.target.value })}
                  required
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <FormControl fullWidth required>
                  <InputLabel>Yeast Strain</InputLabel>
                  <Select
                    value={newTrial.yeast_strain}
                    label="Yeast Strain"
                    onChange={(e) => setNewTrial({ ...newTrial, yeast_strain: e.target.value })}
                  >
                    {yeastStrains.map((strain) => (
                      <MenuItem key={strain} value={strain}>{strain}</MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} md={6}>
                <FormControl fullWidth required>
                  <InputLabel>Fruit Type</InputLabel>
                  <Select
                    value={newTrial.fruit_type}
                    label="Fruit Type"
                    onChange={(e) => setNewTrial({ ...newTrial, fruit_type: e.target.value })}
                  >
                    {fruitTypes.map((fruit) => (
                      <MenuItem key={fruit} value={fruit}>{fruit}</MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Temperature (°C)"
                  type="number"
                  value={newTrial.temperature}
                  onChange={(e) => setNewTrial({ ...newTrial, temperature: parseFloat(e.target.value) })}
                  inputProps={{ step: 0.1, min: 15, max: 35 }}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Initial Specific Gravity"
                  type="number"
                  value={newTrial.initial_sg}
                  onChange={(e) => setNewTrial({ ...newTrial, initial_sg: parseFloat(e.target.value) })}
                  inputProps={{ step: 0.001, min: 1.000, max: 1.200 }}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Target Specific Gravity"
                  type="number"
                  value={newTrial.target_sg}
                  onChange={(e) => setNewTrial({ ...newTrial, target_sg: parseFloat(e.target.value) })}
                  inputProps={{ step: 0.001, min: 0.990, max: 1.100 }}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="pH"
                  type="number"
                  value={newTrial.ph}
                  onChange={(e) => setNewTrial({ ...newTrial, ph: parseFloat(e.target.value) })}
                  inputProps={{ step: 0.1, min: 3.0, max: 6.0 }}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Notes"
                  multiline
                  rows={3}
                  value={newTrial.notes}
                  onChange={(e) => setNewTrial({ ...newTrial, notes: e.target.value })}
                />
              </Grid>
            </Grid>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
          <Button 
            onClick={editingTrial ? handleUpdateTrial : handleCreateTrial} 
            variant="contained"
          >
            {editingTrial ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
