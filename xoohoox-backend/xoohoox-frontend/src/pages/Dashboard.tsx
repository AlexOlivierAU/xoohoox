import { useState } from 'react';
import { useTheme } from '@mui/material/styles';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Paper,
  Stack,
  Grid,
  LinearProgress,
} from '@mui/material';
import {
  Add as AddIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
  Pause as PauseIcon
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

interface StatCardProps {
  title: string;
  value: number;
  color: string;
  onClick?: () => void;
}

interface BatchCardProps {
  name: string;
  batchId: string;
  progress: number;
  startDate: Date;
  endDate: Date;
  stage: string;
  status: 'running' | 'paused' | 'warning';
  onInfoClick?: () => void;
}

const StatCard = ({ title, value, color, onClick }: StatCardProps) => (
  <Card 
    sx={{ 
      cursor: onClick ? 'pointer' : 'default',
      '&:hover': onClick ? { transform: 'translateY(-2px)', boxShadow: 3 } : {},
      transition: 'transform 0.2s, box-shadow 0.2s'
    }}
    onClick={onClick}
  >
    <CardContent>
      <Typography variant="h6" color="textSecondary" gutterBottom>
        {title}
      </Typography>
      <Typography variant="h4" component="div" sx={{ color }}>
        {value}
      </Typography>
    </CardContent>
  </Card>
);

const BatchCard: React.FC<BatchCardProps> = ({ name, batchId, progress, startDate, endDate, stage, status, onInfoClick }) => {
  const navigate = useNavigate();

  const getStatusIcon = () => {
    switch (status) {
      case 'running':
        return <CheckCircleIcon color="success" />;
      case 'paused':
        return <PauseIcon color="warning" />;
      case 'warning':
        return <WarningIcon color="error" />;
      default:
        return null;
    }
  };

  const handleClick = () => {
    navigate(`/batches/${batchId}`);
  };

  return (
    <Card 
      sx={{ 
        cursor: 'pointer',
        '&:hover': {
          boxShadow: 6,
        }
      }}
      onClick={handleClick}
    >
      <CardContent>
        <Stack spacing={2}>
          <Stack direction="row" justifyContent="space-between" alignItems="center">
            <Typography variant="h6">{name}</Typography>
            {getStatusIcon()}
          </Stack>
          <Typography color="text.secondary">ID: {batchId}</Typography>
          <Box>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              Progress
            </Typography>
            <Box sx={{ width: '100%', bgcolor: 'background.paper', borderRadius: 1, overflow: 'hidden' }}>
              <Box
                sx={{
                  width: `${progress}%`,
                  height: 8,
                  bgcolor: status === 'warning' ? 'error.main' : 'primary.main',
                }}
              />
            </Box>
          </Box>
          <Typography variant="body2">Stage: {stage}</Typography>
          <Stack direction="row" justifyContent="space-between">
            <Typography variant="caption" color="text.secondary">
              Start: {startDate.toLocaleDateString()}
            </Typography>
            <Typography variant="caption" color="text.secondary">
              End: {endDate.toLocaleDateString()}
            </Typography>
          </Stack>
          <Button variant="outlined" size="small" onClick={onInfoClick}>
            View Details
          </Button>
        </Stack>
      </CardContent>
    </Card>
  );
};

interface BatchDetailsModalProps {
  batch: BatchCardProps | null;
  open: boolean;
  onClose: () => void;
}

const BatchDetailsModal = ({ batch, open, onClose }: BatchDetailsModalProps) => {
  if (!batch) return null;

  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>
        Batch Details: {batch.name}
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Typography variant="subtitle1">Batch Information</Typography>
          <Box sx={{ mt: 2 }}>
            <Typography>ID: {batch.batchId}</Typography>
            <Typography>Stage: {batch.stage}</Typography>
            <Typography>Status: {batch.status}</Typography>
            <Typography>Progress: {batch.progress}%</Typography>
          </Box>
        </Grid>
        <Grid item xs={12} md={6}>
          <Typography variant="subtitle1">Timeline</Typography>
          <Box sx={{ mt: 2 }}>
            <Typography>Start Date: {batch.startDate.toLocaleDateString()}</Typography>
            <Typography>End Date: {batch.endDate.toLocaleDateString()}</Typography>
          </Box>
        </Grid>
      </Grid>
    </Paper>
  );
};

interface BatchCreateModalProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (batch: Omit<BatchCardProps, 'progress' | 'status' | 'onInfoClick'>) => void;
}

const BatchCreateModal = ({ open, onClose, onSubmit }: BatchCreateModalProps) => {
  const [name, setName] = useState('');
  const [stage, setStage] = useState('Initial Processing');
  const [startDate, setStartDate] = useState(new Date().toISOString().split('T')[0]);
  const [endDate, setEndDate] = useState(
    new Date(Date.now() + 5 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
  );

  const handleSubmit = () => {
    onSubmit({
      name,
      batchId: `B${Math.floor(Math.random() * 1000).toString().padStart(3, '0')}`,
      stage,
      startDate: new Date(startDate),
      endDate: new Date(endDate),
    });
    onClose();
  };

  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>
        Create New Batch
      </Typography>
      <Stack spacing={3}>
        <TextField
          label="Batch Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          fullWidth
        />
        <FormControl fullWidth>
          <InputLabel>Stage</InputLabel>
          <Select value={stage} onChange={(e) => setStage(e.target.value)}>
            <MenuItem value="Initial Processing">Initial Processing</MenuItem>
            <MenuItem value="Fermentation">Fermentation</MenuItem>
            <MenuItem value="Quality Check">Quality Check</MenuItem>
            <MenuItem value="Final Processing">Final Processing</MenuItem>
          </Select>
        </FormControl>
        <TextField
          label="Start Date"
          type="date"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
          fullWidth
          InputLabelProps={{ shrink: true }}
        />
        <TextField
          label="End Date"
          type="date"
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
          fullWidth
          InputLabelProps={{ shrink: true }}
        />
        <Stack direction="row" spacing={2} justifyContent="flex-end">
          <Button onClick={onClose}>Cancel</Button>
          <Button variant="contained" onClick={handleSubmit} disabled={!name || !stage}>
            Create
          </Button>
        </Stack>
      </Stack>
    </Paper>
  );
};

export const Dashboard = () => {
  const theme = useTheme();
  const navigate = useNavigate();

  const [stats] = useState({
    activeBatches: 12,
    completedToday: 5,
    qualityChecks: 8,
    maintenanceTasks: 3
  });

  const [selectedBatch, setSelectedBatch] = useState<BatchCardProps | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [stageFilter, setStageFilter] = useState<string>('all');
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);

  const [batches, setBatches] = useState<BatchCardProps[]>([
    {
      name: 'Apple Juice',
      batchId: 'B001',
      progress: 75,
      startDate: new Date('2024-04-10'),
      endDate: new Date('2024-04-15'),
      stage: 'Fermentation',
      status: 'running'
    },
    {
      name: 'Orange Juice',
      batchId: 'B002',
      progress: 30,
      startDate: new Date('2024-04-11'),
      endDate: new Date('2024-04-16'),
      stage: 'Initial Processing',
      status: 'paused'
    },
    {
      name: 'Grape Juice',
      batchId: 'B003',
      progress: 90,
      startDate: new Date('2024-04-09'),
      endDate: new Date('2024-04-14'),
      stage: 'Quality Check',
      status: 'warning'
    }
  ]);

  const handleStatClick = (stat: string) => {
    console.log(`Clicked ${stat}`);
    // TODO: Implement navigation or modal display
  };

  const handleBatchClick = (batch: BatchCardProps) => {
    setSelectedBatch(batch);
  };

  const handleCreateBatch = () => {
    setIsCreateModalOpen(true);
  };

  const handleCreateBatchSubmit = (newBatch: Omit<BatchCardProps, 'progress' | 'status' | 'onInfoClick'>) => {
    setBatches([
      ...batches,
      {
        ...newBatch,
        progress: 0,
        status: 'running'
      }
    ]);
  };

  const filteredBatches = batches.filter(batch => {
    const matchesSearch = batch.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         batch.batchId.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === 'all' || batch.status === statusFilter;
    const matchesStage = stageFilter === 'all' || batch.stage === stageFilter;
    return matchesSearch && matchesStatus && matchesStage;
  });

  return (
    <Box>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom>Dashboard</Typography>
        <Typography variant="subtitle1" color="textSecondary">
          Monitor and manage your active batches
        </Typography>
      </Box>

      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Active Batches"
            value={stats.activeBatches}
            color={theme.palette.primary.main}
            onClick={() => handleStatClick('activeBatches')}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Completed Today"
            value={stats.completedToday}
            color={theme.palette.success.main}
            onClick={() => handleStatClick('completedToday')}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Quality Checks"
            value={stats.qualityChecks}
            color={theme.palette.info.main}
            onClick={() => handleStatClick('qualityChecks')}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Maintenance Tasks"
            value={stats.maintenanceTasks}
            color={theme.palette.warning.main}
            onClick={() => handleStatClick('maintenanceTasks')}
          />
        </Grid>
      </Grid>

      <Box sx={{ mb: 3 }}>
        <Stack direction="row" spacing={2} alignItems="center" sx={{ mb: 2 }}>
          <Typography variant="h5">Active Batches</Typography>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={handleCreateBatch}
            sx={{ ml: 'auto' }}
          >
            New Batch
          </Button>
        </Stack>

        <Stack direction="row" spacing={2} sx={{ mb: 3 }}>
          <TextField
            placeholder="Search batches..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            size="small"
            sx={{ width: 200 }}
          />
          <FormControl size="small" sx={{ width: 150 }}>
            <InputLabel>Status</InputLabel>
            <Select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              label="Status"
            >
              <MenuItem value="all">All</MenuItem>
              <MenuItem value="running">Running</MenuItem>
              <MenuItem value="paused">Paused</MenuItem>
              <MenuItem value="warning">Warning</MenuItem>
            </Select>
          </FormControl>
          <FormControl size="small" sx={{ width: 150 }}>
            <InputLabel>Stage</InputLabel>
            <Select
              value={stageFilter}
              onChange={(e) => setStageFilter(e.target.value)}
              label="Stage"
            >
              <MenuItem value="all">All</MenuItem>
              <MenuItem value="Initial Processing">Initial Processing</MenuItem>
              <MenuItem value="Fermentation">Fermentation</MenuItem>
              <MenuItem value="Quality Check">Quality Check</MenuItem>
            </Select>
          </FormControl>
        </Stack>
      </Box>

      <Grid container spacing={3}>
        {filteredBatches.map((batch) => (
          <Grid item xs={12} sm={6} md={4} lg={3} key={batch.batchId}>
            <BatchCard {...batch} onInfoClick={() => handleBatchClick(batch)} />
          </Grid>
        ))}
      </Grid>

      {selectedBatch && (
        <BatchDetailsModal
          batch={selectedBatch}
          open={!!selectedBatch}
          onClose={() => setSelectedBatch(null)}
        />
      )}

      <BatchCreateModal
        open={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
        onSubmit={handleCreateBatchSubmit}
      />
    </Box>
  );
};
