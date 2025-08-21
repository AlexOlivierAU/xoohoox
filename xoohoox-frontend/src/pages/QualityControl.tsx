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
  Alert,
} from '@mui/material';
import { Add as AddIcon, Edit as EditIcon, Delete as DeleteIcon } from '@mui/icons-material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface QualityCheck {
  id: string;
  batchId: string;
  timestamp: Date;
  ph: number;
  brix: number;
  temperature: number;
  notes: string;
  status: 'Pass' | 'Fail' | 'Warning';
}

export default function QualityControl() {
  const [openDialog, setOpenDialog] = useState(false);
  const [qualityChecks, setQualityChecks] = useState<QualityCheck[]>([
    {
      id: 'QC001',
      batchId: 'B001',
      timestamp: new Date(),
      ph: 3.5,
      brix: 12.5,
      temperature: 25,
      notes: 'Within acceptable range',
      status: 'Pass',
    },
    {
      id: 'QC002',
      batchId: 'B001',
      timestamp: new Date(Date.now() - 3600000),
      ph: 3.6,
      brix: 12.3,
      temperature: 24,
      notes: 'Slight variation in temperature',
      status: 'Warning',
    },
  ]);

  const [newCheck, setNewCheck] = useState<Partial<QualityCheck>>({
    batchId: '',
    ph: 0,
    brix: 0,
    temperature: 0,
    notes: '',
  });

  const handleCreateCheck = () => {
    if (newCheck.batchId && newCheck.ph && newCheck.brix && newCheck.temperature) {
      const check: QualityCheck = {
        id: `QC${String(qualityChecks.length + 1).padStart(3, '0')}`,
        batchId: newCheck.batchId,
        timestamp: new Date(),
        ph: newCheck.ph,
        brix: newCheck.brix,
        temperature: newCheck.temperature,
        notes: newCheck.notes || '',
        status: determineStatus(newCheck.ph, newCheck.brix, newCheck.temperature),
      };
      setQualityChecks([...qualityChecks, check]);
      setOpenDialog(false);
      setNewCheck({
        batchId: '',
        ph: 0,
        brix: 0,
        temperature: 0,
        notes: '',
      });
    }
  };

  const determineStatus = (ph: number, brix: number, temperature: number): 'Pass' | 'Fail' | 'Warning' => {
    // Example thresholds - adjust based on actual requirements
    if (ph < 3.0 || ph > 4.0 || brix < 10 || brix > 15 || temperature < 20 || temperature > 30) {
      return 'Fail';
    }
    if (ph < 3.2 || ph > 3.8 || brix < 11 || brix > 14 || temperature < 22 || temperature > 28) {
      return 'Warning';
    }
    return 'Pass';
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Pass':
        return '#2ECC71';
      case 'Warning':
        return '#F1C40F';
      case 'Fail':
        return '#E74C3C';
      default:
        return '#95A5A6';
    }
  };

  // Prepare data for charts
  const chartData = qualityChecks.map(check => ({
    timestamp: check.timestamp.toLocaleTimeString(),
    ph: check.ph,
    brix: check.brix,
    temperature: check.temperature,
  }));

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">Quality Control</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setOpenDialog(true)}
        >
          New Quality Check
        </Button>
      </Box>

      {/* Charts */}
      <Box sx={{ mb: 4 }}>
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            Quality Metrics Over Time
          </Typography>
          <Box sx={{ height: 400 }}>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="timestamp" />
                <YAxis yAxisId="left" />
                <YAxis yAxisId="right" orientation="right" />
                <Tooltip />
                <Legend />
                <Line yAxisId="left" type="monotone" dataKey="ph" stroke="#8884d8" name="pH" />
                <Line yAxisId="left" type="monotone" dataKey="brix" stroke="#82ca9d" name="Brix" />
                <Line yAxisId="right" type="monotone" dataKey="temperature" stroke="#ffc658" name="Temperature (°C)" />
              </LineChart>
            </ResponsiveContainer>
          </Box>
        </Paper>
      </Box>

      {/* Quality Checks Table */}
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Check ID</TableCell>
              <TableCell>Batch ID</TableCell>
              <TableCell>Timestamp</TableCell>
              <TableCell>pH</TableCell>
              <TableCell>Brix</TableCell>
              <TableCell>Temperature</TableCell>
              <TableCell>Notes</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {qualityChecks.map((check) => (
              <TableRow key={check.id}>
                <TableCell>{check.id}</TableCell>
                <TableCell>{check.batchId}</TableCell>
                <TableCell>{check.timestamp.toLocaleString()}</TableCell>
                <TableCell>{check.ph}</TableCell>
                <TableCell>{check.brix}</TableCell>
                <TableCell>{check.temperature}°C</TableCell>
                <TableCell>{check.notes}</TableCell>
                <TableCell>
                  <Box
                    sx={{
                      backgroundColor: getStatusColor(check.status),
                      color: 'white',
                      padding: '4px 8px',
                      borderRadius: '4px',
                      display: 'inline-block',
                    }}
                  >
                    {check.status}
                  </Box>
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

      {/* New Quality Check Dialog */}
      <Dialog open={openDialog} onClose={() => setOpenDialog(false)}>
        <DialogTitle>New Quality Check</DialogTitle>
        <DialogContent>
          <Box sx={{ mt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
            <TextField
              fullWidth
              label="Batch ID"
              value={newCheck.batchId}
              onChange={(e) => setNewCheck({ ...newCheck, batchId: e.target.value })}
            />
            <TextField
              fullWidth
              label="pH"
              type="number"
              value={newCheck.ph}
              onChange={(e) => setNewCheck({ ...newCheck, ph: parseFloat(e.target.value) })}
              inputProps={{ step: "0.1" }}
            />
            <TextField
              fullWidth
              label="Brix"
              type="number"
              value={newCheck.brix}
              onChange={(e) => setNewCheck({ ...newCheck, brix: parseFloat(e.target.value) })}
              inputProps={{ step: "0.1" }}
            />
            <TextField
              fullWidth
              label="Temperature (°C)"
              type="number"
              value={newCheck.temperature}
              onChange={(e) => setNewCheck({ ...newCheck, temperature: parseFloat(e.target.value) })}
              inputProps={{ step: "0.1" }}
            />
            <TextField
              fullWidth
              label="Notes"
              multiline
              rows={3}
              value={newCheck.notes}
              onChange={(e) => setNewCheck({ ...newCheck, notes: e.target.value })}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
          <Button onClick={handleCreateCheck} variant="contained">
            Create
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
} 