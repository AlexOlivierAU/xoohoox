import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
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
  Alert,
  CircularProgress,
  Chip,
} from '@mui/material';
import { Add as AddIcon, Edit as EditIcon, Delete as DeleteIcon } from '@mui/icons-material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import batchService, { Batch, BatchCreate } from '../services/batchService';

export default function BatchManagement() {
  const [openDialog, setOpenDialog] = useState(false);
  const [batches, setBatches] = useState<Batch[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [newBatch, setNewBatch] = useState<Partial<BatchCreate>>({
    fruit_type: '',
    quantity: 0,
    unit: 'L',
    expected_completion: new Date().toISOString().split('T')[0],
  });

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

  const handleCreateBatch = async () => {
    if (newBatch.fruit_type && newBatch.quantity) {
      try {
        await batchService.createBatch(newBatch as BatchCreate);
        fetchBatches();
        setOpenDialog(false);
        setNewBatch({
          fruit_type: '',
          quantity: 0,
          unit: 'L',
          expected_completion: new Date().toISOString().split('T')[0],
        });
      } catch (err: any) {
        setError('Failed to create batch');
        console.error('Error creating batch:', err);
      }
    }
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">Batch Management</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setOpenDialog(true)}
        >
          Create New Batch
        </Button>
      </Box>

      {loading ? (
        <Box display="flex" justifyContent="center" p={3}>
          <CircularProgress />
        </Box>
      ) : error ? (
        <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>
      ) : (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Batch ID</TableCell>
                <TableCell>Fruit Type</TableCell>
                <TableCell>Quantity (L)</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Expected Completion</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {batches.map((batch) => (
                <TableRow key={batch.id}>
                  <TableCell>{batch.batch_id}</TableCell>
                  <TableCell>{batch.fruit_type}</TableCell>
                  <TableCell>{batch.quantity}</TableCell>
                  <TableCell>
                    <Chip 
                      label={batch.status} 
                      color={batch.status === 'completed' ? 'success' : 
                             batch.status === 'active' ? 'primary' : 'default'}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>{batch.expected_completion}</TableCell>
                  <TableCell>
                    <IconButton size="small">
                      <EditIcon />
                    </IconButton>
                    <IconButton size="small" color="error">
                      <DeleteIcon />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      <Dialog open={openDialog} onClose={() => setOpenDialog(false)}>
        <DialogTitle>Create New Batch</DialogTitle>
        <DialogContent>
          <Box sx={{ mt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
            <TextField
              fullWidth
              label="Fruit Type"
              value={newBatch.fruit_type}
              onChange={(e) => setNewBatch({ ...newBatch, fruit_type: e.target.value })}
            />
            <TextField
              fullWidth
              label="Quantity"
              type="number"
              value={newBatch.quantity}
              onChange={(e) => setNewBatch({ ...newBatch, quantity: parseInt(e.target.value) })}
            />
            <TextField
              fullWidth
              label="Unit"
              value={newBatch.unit}
              onChange={(e) => setNewBatch({ ...newBatch, unit: e.target.value })}
            />
            <TextField
              fullWidth
              label="Expected Completion Date"
              type="date"
              value={newBatch.expected_completion}
              onChange={(e) => setNewBatch({ ...newBatch, expected_completion: e.target.value })}
              InputLabelProps={{ shrink: true }}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
          <Button onClick={handleCreateBatch} variant="contained">
            Create
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
} 