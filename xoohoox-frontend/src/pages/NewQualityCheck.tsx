import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Grid,
  Alert,
  CircularProgress,
  Divider,
  Chip,
} from '@mui/material';
import {
  Save as SaveIcon,
  Cancel as CancelIcon,
  Add as AddIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import qualityService from '../services/qualityService';

interface Batch {
  id: string;
  batch_number: string;
  status: string;
}

const NewQualityCheck = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  
  // Form state
  const [formData, setFormData] = useState({
    batch_id: '',
    check_type: '',
    result: 'pass' as 'pass' | 'warning' | 'fail',
    performed_by: '',
    notes: '',
    parameters: {
      temperature: '',
      ph_level: '',
      brix_level: '',
      alcohol_content: '',
    }
  });

  // Mock batches for selection
  const [batches] = useState<Batch[]>([
    { id: 'XHR-20250413-01-01-B001', batch_number: 'B001', status: 'active' },
    { id: 'XHR-20250413-01-02-B002', batch_number: 'B002', status: 'active' },
    { id: 'XHR-20250413-01-03-B003', batch_number: 'B003', status: 'active' },
    { id: 'XHR-20250413-01-04-B004', batch_number: 'B004', status: 'active' },
  ]);

  const checkTypes = [
    'pH',
    'Brix',
    'Temperature',
    'Alcohol Content',
    'Turbidity',
    'Color',
    'Aroma',
    'Taste',
    'Density',
    'Viscosity'
  ];

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleParameterChange = (field: string, value: string) => {
    setFormData(prev => ({
      ...prev,
      parameters: {
        ...prev.parameters,
        [field]: value
      }
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      // Convert empty strings to undefined for optional parameters
      const parameters = Object.fromEntries(
        Object.entries(formData.parameters).map(([key, value]) => [
          key,
          value === '' ? undefined : parseFloat(value)
        ])
      );

      const qualityCheckData = {
        ...formData,
        parameters: parameters
      };

      await qualityService.createQualityCheck(qualityCheckData);
      setSuccess('Quality check created successfully!');
      
      // Redirect after a short delay
      setTimeout(() => {
        navigate('/quality-checks');
      }, 1500);
    } catch (err: any) {
      setError('Failed to create quality check. Please try again.');
      console.error('Error creating quality check:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    navigate('/quality-checks');
  };

  const getResultColor = (result: string) => {
    switch (result) {
      case 'pass':
        return 'success';
      case 'warning':
        return 'warning';
      case 'fail':
        return 'error';
      default:
        return 'default';
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Paper sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h4" component="h1">
            Create New Quality Check
          </Typography>
          <Chip 
            label="Distillation Quality Control" 
            color="primary" 
            variant="outlined"
          />
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {success && (
          <Alert severity="success" sx={{ mb: 2 }}>
            {success}
          </Alert>
        )}

        <form onSubmit={handleSubmit}>
          <Grid container spacing={3}>
            {/* Basic Information */}
            <Grid item xs={12}>
              <Typography variant="h6" gutterBottom>
                Basic Information
              </Typography>
              <Divider sx={{ mb: 2 }} />
            </Grid>

            <Grid item xs={12} md={6}>
              <FormControl fullWidth required>
                <InputLabel>Batch</InputLabel>
                <Select
                  value={formData.batch_id}
                  onChange={(e) => handleInputChange('batch_id', e.target.value)}
                  label="Batch"
                >
                  {batches.map((batch) => (
                    <MenuItem key={batch.id} value={batch.id}>
                      {batch.batch_number} - {batch.status}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={12} md={6}>
              <FormControl fullWidth required>
                <InputLabel>Check Type</InputLabel>
                <Select
                  value={formData.check_type}
                  onChange={(e) => handleInputChange('check_type', e.target.value)}
                  label="Check Type"
                >
                  {checkTypes.map((type) => (
                    <MenuItem key={type} value={type}>
                      {type}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={12} md={6}>
              <FormControl fullWidth required>
                <InputLabel>Result</InputLabel>
                <Select
                  value={formData.result}
                  onChange={(e) => handleInputChange('result', e.target.value)}
                  label="Result"
                >
                  <MenuItem value="pass">
                    <Chip label="Pass" color="success" size="small" />
                  </MenuItem>
                  <MenuItem value="warning">
                    <Chip label="Warning" color="warning" size="small" />
                  </MenuItem>
                  <MenuItem value="fail">
                    <Chip label="Fail" color="error" size="small" />
                  </MenuItem>
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                required
                label="Performed By"
                value={formData.performed_by}
                onChange={(e) => handleInputChange('performed_by', e.target.value)}
                placeholder="Lab Technician Name"
              />
            </Grid>

            <Grid item xs={12}>
              <TextField
                fullWidth
                multiline
                rows={3}
                label="Notes"
                value={formData.notes}
                onChange={(e) => handleInputChange('notes', e.target.value)}
                placeholder="Additional observations, comments, or recommendations..."
              />
            </Grid>

            {/* Parameters Section */}
            <Grid item xs={12}>
              <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
                Measurement Parameters
              </Typography>
              <Divider sx={{ mb: 2 }} />
            </Grid>

            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                type="number"
                label="Temperature (°C)"
                value={formData.parameters.temperature}
                onChange={(e) => handleParameterChange('temperature', e.target.value)}
                placeholder="22.5"
                inputProps={{ step: 0.1, min: 0, max: 100 }}
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                type="number"
                label="pH Level"
                value={formData.parameters.ph_level}
                onChange={(e) => handleParameterChange('ph_level', e.target.value)}
                placeholder="4.2"
                inputProps={{ step: 0.1, min: 0, max: 14 }}
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                type="number"
                label="Brix Level (°Bx)"
                value={formData.parameters.brix_level}
                onChange={(e) => handleParameterChange('brix_level', e.target.value)}
                placeholder="18.5"
                inputProps={{ step: 0.1, min: 0, max: 50 }}
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                type="number"
                label="Alcohol Content (%)"
                value={formData.parameters.alcohol_content}
                onChange={(e) => handleParameterChange('alcohol_content', e.target.value)}
                placeholder="6.8"
                inputProps={{ step: 0.1, min: 0, max: 100 }}
              />
            </Grid>

            {/* Action Buttons */}
            <Grid item xs={12}>
              <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end', mt: 3 }}>
                <Button
                  variant="outlined"
                  startIcon={<CancelIcon />}
                  onClick={handleCancel}
                  disabled={loading}
                >
                  Cancel
                </Button>
                <Button
                  type="submit"
                  variant="contained"
                  startIcon={loading ? <CircularProgress size={20} /> : <SaveIcon />}
                  disabled={loading || !formData.batch_id || !formData.check_type || !formData.performed_by}
                >
                  {loading ? 'Creating...' : 'Create Quality Check'}
                </Button>
              </Box>
            </Grid>
          </Grid>
        </form>
      </Paper>
    </Box>
  );
};

export default NewQualityCheck;
