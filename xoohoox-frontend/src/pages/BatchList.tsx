import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  TextField,
  Button,
  Chip,
  IconButton,
  Tooltip,
  Alert,
  CircularProgress,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Stack,
  LinearProgress,
} from '@mui/material';
import {
  Add as AddIcon,
  Visibility as ViewIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  FilterList as FilterIcon,
  Search as SearchIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import batchService from '../services/batchService';

import { Batch } from '../services/batchService';

const BatchList = () => {
  const navigate = useNavigate();
  const [batches, setBatches] = useState<Batch[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');

  useEffect(() => {
    fetchBatches();
  }, []);

  const fetchBatches = async () => {
    try {
      setLoading(true);
      const response = await batchService.getBatches();
      setBatches(response.items);
    } catch (err: any) {
      setError('Failed to fetch batches');
      console.error('Error fetching batches:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
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

  const filteredBatches = batches.filter((batch) => {
    const matchesSearch = 
      batch.fruit_type.toLowerCase().includes(searchTerm.toLowerCase()) ||
      batch.batch_id.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesStatus = statusFilter === 'all' || batch.status.toLowerCase() === statusFilter.toLowerCase();
    
    return matchesSearch && matchesStatus;
  });

  const paginatedBatches = filteredBatches.slice(
    page * rowsPerPage,
    page * rowsPerPage + rowsPerPage
  );

  const handleViewBatch = (batchId: string) => {
    navigate(`/batches/${batchId}`);
  };

  const handleEditBatch = (batchId: string) => {
    navigate(`/batches/${batchId}/edit`);
  };

  const handleDeleteBatch = async (batchId: string) => {
    if (window.confirm('Are you sure you want to delete this batch?')) {
      try {
        await batchService.deleteBatch(batchId);
        fetchBatches();
      } catch (err: any) {
        setError('Failed to delete batch');
      }
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Batch Management
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => navigate('/batches/new')}
        >
          New Batch
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Paper sx={{ p: 2, mb: 2 }}>
        <Stack direction="row" spacing={2} alignItems="center" sx={{ mb: 2 }}>
          <TextField
            placeholder="Search batches..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            InputProps={{
              startAdornment: <SearchIcon sx={{ mr: 1, color: 'text.secondary' }} />,
            }}
            sx={{ minWidth: 300 }}
          />
          
          <FormControl sx={{ minWidth: 150 }}>
            <InputLabel>Status</InputLabel>
            <Select
              value={statusFilter}
              label="Status"
              onChange={(e) => setStatusFilter(e.target.value)}
            >
              <MenuItem value="all">All Status</MenuItem>
              <MenuItem value="active">Active</MenuItem>
              <MenuItem value="in_progress">In Progress</MenuItem>
              <MenuItem value="completed">Completed</MenuItem>
              <MenuItem value="paused">Paused</MenuItem>
              <MenuItem value="cancelled">Cancelled</MenuItem>
            </Select>
          </FormControl>

          <Button
            variant="outlined"
            startIcon={<FilterIcon />}
            onClick={() => {
              setSearchTerm('');
              setStatusFilter('all');
            }}
          >
            Clear Filters
          </Button>
        </Stack>

        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Batch Number</TableCell>
                <TableCell>Product</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Current Stage</TableCell>
                <TableCell>Progress</TableCell>
                <TableCell>Start Date</TableCell>
                <TableCell>Expected Completion</TableCell>
                <TableCell>Quantity</TableCell>
                <TableCell align="center">Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {paginatedBatches.map((batch) => (
                <TableRow key={batch.id} hover>
                  <TableCell>
                    <Typography variant="subtitle2" fontWeight="bold">
                      {batch.batch_id}
                    </Typography>
                  </TableCell>
                  <TableCell>{batch.fruit_type}</TableCell>
                  <TableCell>
                    <Chip
                      label={batch.status}
                      color={getStatusColor(batch.status) as any}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>{batch.current_stage}</TableCell>
                  <TableCell>
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <Box sx={{ width: '100%', mr: 1 }}>
                        <LinearProgress
                          variant="determinate"
                          value={batch.progress}
                          sx={{ height: 8, borderRadius: 4 }}
                        />
                      </Box>
                      <Typography variant="body2" color="text.secondary">
                        {batch.progress}%
                      </Typography>
                    </Box>
                  </TableCell>
                  <TableCell>{new Date(batch.start_date).toLocaleDateString()}</TableCell>
                  <TableCell>{new Date(batch.expected_completion).toLocaleDateString()}</TableCell>
                  <TableCell>
                    {batch.quantity} {batch.unit}
                  </TableCell>
                  <TableCell align="center">
                    <Stack direction="row" spacing={1} justifyContent="center">
                      <Tooltip title="View Details">
                        <IconButton
                          size="small"
                          onClick={() => handleViewBatch(batch.id)}
                        >
                          <ViewIcon />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Edit Batch">
                        <IconButton
                          size="small"
                          onClick={() => handleEditBatch(batch.id)}
                        >
                          <EditIcon />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Delete Batch">
                        <IconButton
                          size="small"
                          color="error"
                          onClick={() => handleDeleteBatch(batch.id)}
                        >
                          <DeleteIcon />
                        </IconButton>
                      </Tooltip>
                    </Stack>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>

        <TablePagination
          rowsPerPageOptions={[5, 10, 25]}
          component="div"
          count={filteredBatches.length}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={handleChangePage}
          onRowsPerPageChange={handleChangeRowsPerPage}
        />
      </Paper>
    </Box>
  );
};

export default BatchList;
