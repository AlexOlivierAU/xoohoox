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
} from '@mui/material';
import { Add as AddIcon, Edit as EditIcon, Delete as DeleteIcon } from '@mui/icons-material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import equipmentService, { MaintenanceRecord, MaintenanceRecordCreate } from '../services/equipmentService';

export default function EquipmentMaintenance() {
  const [openDialog, setOpenDialog] = useState(false);
  const [maintenanceRecords, setMaintenanceRecords] = useState<MaintenanceRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [newRecord, setNewRecord] = useState<Partial<MaintenanceRecordCreate>>({
    equipment_id: '',
    maintenance_type: 'preventive',
    description: '',
    scheduled_date: new Date().toISOString().split('T')[0],
    technician: '',
    notes: '',
  });

  useEffect(() => {
    fetchMaintenanceRecords();
  }, []);

  const fetchMaintenanceRecords = async () => {
    try {
      setLoading(true);
      const response = await equipmentService.getMaintenanceRecords();
      setMaintenanceRecords(response.items);
    } catch (err: any) {
      setError('Failed to fetch maintenance records');
      console.error('Error fetching maintenance records:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateRecord = async () => {
    if (newRecord.equipment_id && newRecord.description && newRecord.technician) {
      try {
        await equipmentService.createMaintenanceRecord(newRecord as MaintenanceRecordCreate);
        fetchMaintenanceRecords();
        setOpenDialog(false);
        setNewRecord({
          equipment_id: '',
          maintenance_type: 'preventive',
          description: '',
          scheduled_date: new Date().toISOString().split('T')[0],
          technician: '',
          notes: '',
        });
      } catch (err: any) {
        setError('Failed to create maintenance record');
        console.error('Error creating maintenance record:', err);
      }
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Completed':
        return '#2ECC71';
      case 'In Progress':
        return '#3498DB';
      case 'Scheduled':
        return '#F1C40F';
      case 'Overdue':
        return '#E74C3C';
      default:
        return '#95A5A6';
    }
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">Equipment Maintenance</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setOpenDialog(true)}
        >
          Schedule Maintenance
        </Button>
      </Box>

      {loading ? (
        <Box display="flex" justifyContent="center" p={3}>
          <CircularProgress />
        </Box>
      ) : error ? (
        <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>
      ) : (
        <>
          {/* Maintenance Schedule Overview */}
          <Box sx={{ display: 'flex', gap: 3, mb: 4 }}>
            <Paper sx={{ p: 3, textAlign: 'center', flex: 1 }}>
              <Typography variant="h6" gutterBottom>
                Scheduled
              </Typography>
              <Typography variant="h3" color="primary">
                {maintenanceRecords.filter(r => r.status === 'scheduled').length}
              </Typography>
            </Paper>
            <Paper sx={{ p: 3, textAlign: 'center', flex: 1 }}>
              <Typography variant="h6" gutterBottom>
                In Progress
              </Typography>
              <Typography variant="h3" color="info">
                {maintenanceRecords.filter(r => r.status === 'in_progress').length}
              </Typography>
            </Paper>
            <Paper sx={{ p: 3, textAlign: 'center', flex: 1 }}>
              <Typography variant="h6" gutterBottom>
                Overdue
              </Typography>
              <Typography variant="h3" color="error">
                {maintenanceRecords.filter(r => r.status === 'overdue').length}
              </Typography>
            </Paper>
          </Box>

          {/* Maintenance Records Table */}
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Record ID</TableCell>
                  <TableCell>Equipment ID</TableCell>
                  <TableCell>Type</TableCell>
                  <TableCell>Description</TableCell>
                  <TableCell>Scheduled Date</TableCell>
                  <TableCell>Technician</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {maintenanceRecords.map((record) => (
                  <TableRow key={record.id}>
                    <TableCell>{record.id}</TableCell>
                    <TableCell>{record.equipment_id}</TableCell>
                    <TableCell>
                      <Chip
                        label={record.maintenance_type}
                        color={
                          record.maintenance_type === 'emergency'
                            ? 'error'
                            : record.maintenance_type === 'preventive'
                            ? 'success'
                            : 'warning'
                        }
                        size="small"
                      />
                    </TableCell>
                    <TableCell>{record.description}</TableCell>
                    <TableCell>{record.scheduled_date}</TableCell>
                    <TableCell>{record.technician}</TableCell>
                    <TableCell>
                      <Chip
                        label={record.status}
                        color={getStatusColor(record.status)}
                        size="small"
                      />
                    </TableCell>
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
        </>
      )}

      {/* New Maintenance Record Dialog */}
      <Dialog open={openDialog} onClose={() => setOpenDialog(false)}>
        <DialogTitle>Schedule Maintenance</DialogTitle>
        <DialogContent>
          <Box sx={{ mt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
            <TextField
              fullWidth
              label="Equipment ID"
              value={newRecord.equipment_id}
              onChange={(e) => setNewRecord({ ...newRecord, equipment_id: e.target.value })}
            />
            <FormControl fullWidth>
              <InputLabel>Maintenance Type</InputLabel>
              <Select
                value={newRecord.maintenance_type}
                label="Maintenance Type"
                onChange={(e) => setNewRecord({ ...newRecord, maintenance_type: e.target.value as 'preventive' | 'corrective' | 'emergency' })}
              >
                <MenuItem value="preventive">Preventive</MenuItem>
                <MenuItem value="corrective">Corrective</MenuItem>
                <MenuItem value="emergency">Emergency</MenuItem>
              </Select>
            </FormControl>
            <TextField
              fullWidth
              label="Description"
              multiline
              rows={2}
              value={newRecord.description}
              onChange={(e) => setNewRecord({ ...newRecord, description: e.target.value })}
            />
            <TextField
              fullWidth
              label="Scheduled Date"
              type="date"
              value={newRecord.scheduled_date}
              onChange={(e) => setNewRecord({ ...newRecord, scheduled_date: e.target.value })}
              InputLabelProps={{ shrink: true }}
            />
            <TextField
              fullWidth
              label="Technician"
              value={newRecord.technician}
              onChange={(e) => setNewRecord({ ...newRecord, technician: e.target.value })}
            />
            <TextField
              fullWidth
              label="Notes"
              multiline
              rows={3}
              value={newRecord.notes}
              onChange={(e) => setNewRecord({ ...newRecord, notes: e.target.value })}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
          <Button onClick={handleCreateRecord} variant="contained">
            Schedule
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
} 