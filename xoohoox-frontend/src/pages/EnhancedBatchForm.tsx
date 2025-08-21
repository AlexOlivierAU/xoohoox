import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Button,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Grid,
  Card,
  CardContent,
  Checkbox,
  FormControlLabel,
  FormGroup,
  Alert,
  Chip,
} from '@mui/material';
import {
  Save as SaveIcon,
  Science as ScienceIcon,
  LocalDrink as DrinkIcon,
  Agriculture as FarmIcon,
  Inventory as InventoryIcon,
} from '@mui/icons-material';

interface BatchFormData {
  batchId: string;
  name: string;
  fruitType: string;
  processType: string;
  sourceType: 'farmer' | 'supplier';
  sourceName: string;
  juicingRequired: boolean;
  juicingMethod: string;
  targetVolume: number;
  targetPh: number;
  targetSg: number;
  targetBrix: number;
  targetTemperature: number;
  byproducts: {
    peels: boolean;
    pulp: boolean;
    rejects: boolean;
    skins: boolean;
  };
  notes: string;
}

const EnhancedBatchForm: React.FC = () => {
  const [formData, setFormData] = useState<BatchFormData>({
    batchId: '',
    name: '',
    fruitType: '',
    processType: '',
    sourceType: 'farmer',
    sourceName: '',
    juicingRequired: true,
    juicingMethod: 'cold_press',
    targetVolume: 100,
    targetPh: 4.5,
    targetSg: 1.07,
    targetBrix: 20,
    targetTemperature: 22,
    byproducts: {
      peels: true,
      pulp: true,
      rejects: true,
      skins: true,
    },
    notes: '',
  });

  const fruitTypes = ['Lemon', 'Lime', 'Orange', 'Apple', 'Grape', 'Pineapple', 'Mango', 'Mixed'];
  const processTypes = ['Fermentation', 'Distillation', 'Vinegar', 'Juice', 'Mixed'];
  const juicingMethods = [
    { value: 'cold_press', label: 'Cold Press' },
    { value: 'centrifuge', label: 'Centrifuge' },
    { value: 'steam_heat', label: 'Steam/Heat' },
  ];

  const handleSubmit = () => {
    console.log('Creating batch:', formData);
    alert('Batch created successfully!');
  };

  const handleInputChange = (field: keyof BatchFormData, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleByproductChange = (byproduct: keyof BatchFormData['byproducts']) => {
    setFormData(prev => ({
      ...prev,
      byproducts: {
        ...prev.byproducts,
        [byproduct]: !prev.byproducts[byproduct]
      }
    }));
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Enhanced Batch Creation
      </Typography>
      
      <Paper sx={{ p: 3 }}>
        <Grid container spacing={3}>
          {/* Basic Information */}
          <Grid item xs={12}>
            <Typography variant="h6" gutterBottom>
              Basic Information
            </Typography>
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Batch Name"
              value={formData.name}
              onChange={(e) => handleInputChange('name', e.target.value)}
              required
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Batch ID (Auto-generated if empty)"
              value={formData.batchId}
              onChange={(e) => handleInputChange('batchId', e.target.value)}
              placeholder="YYMMDD-FARMER-VARIETAL-XXX"
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <FormControl fullWidth required>
              <InputLabel>Fruit Type</InputLabel>
              <Select
                value={formData.fruitType}
                onChange={(e) => handleInputChange('fruitType', e.target.value)}
              >
                {fruitTypes.map(type => (
                  <MenuItem key={type} value={type}>{type}</MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} md={6}>
            <FormControl fullWidth required>
              <InputLabel>Process Type</InputLabel>
              <Select
                value={formData.processType}
                onChange={(e) => handleInputChange('processType', e.target.value)}
              >
                {processTypes.map(type => (
                  <MenuItem key={type} value={type}>{type}</MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>

          {/* Source Information */}
          <Grid item xs={12}>
            <Typography variant="h6" gutterBottom>
              Source Information
            </Typography>
          </Grid>
          <Grid item xs={12} md={6}>
            <FormControl fullWidth required>
              <InputLabel>Source Type</InputLabel>
              <Select
                value={formData.sourceType}
                onChange={(e) => handleInputChange('sourceType', e.target.value)}
              >
                <MenuItem value="farmer">
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <FarmIcon fontSize="small" />
                    Farmer (Whole Fruit)
                  </Box>
                </MenuItem>
                <MenuItem value="supplier">
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <InventoryIcon fontSize="small" />
                    Supplier (Premade Juice)
                  </Box>
                </MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Source Name"
              value={formData.sourceName}
              onChange={(e) => handleInputChange('sourceName', e.target.value)}
              required
            />
          </Grid>

          {/* Juicing Process */}
          <Grid item xs={12}>
            <Typography variant="h6" gutterBottom>
              Juicing Process
            </Typography>
          </Grid>
          <Grid item xs={12}>
            <FormControlLabel
              control={
                <Checkbox
                  checked={formData.juicingRequired}
                  onChange={(e) => handleInputChange('juicingRequired', e.target.checked)}
                />
              }
              label="Juicing Required"
            />
          </Grid>
          {formData.juicingRequired && (
            <Grid item xs={12} md={6}>
              <FormControl fullWidth required>
                <InputLabel>Juicing Method</InputLabel>
                <Select
                  value={formData.juicingMethod}
                  onChange={(e) => handleInputChange('juicingMethod', e.target.value)}
                >
                  {juicingMethods.map(method => (
                    <MenuItem key={method.value} value={method.value}>
                      {method.label}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
          )}

          {/* Chemistry Targets */}
          <Grid item xs={12}>
            <Typography variant="h6" gutterBottom>
              Chemistry Targets
            </Typography>
            <Alert severity="info" sx={{ mb: 2 }}>
              Target ranges: pH 4.0-5.0, SG &gt; 1.07, Brix &gt; 20, Temp 20-25°C
            </Alert>
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Target Volume (L)"
              type="number"
              value={formData.targetVolume}
              onChange={(e) => handleInputChange('targetVolume', parseFloat(e.target.value))}
              inputProps={{ min: 1, step: 0.1 }}
              required
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Target pH"
              type="number"
              value={formData.targetPh}
              onChange={(e) => handleInputChange('targetPh', parseFloat(e.target.value))}
              inputProps={{ min: 1, max: 14, step: 0.1 }}
              required
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Target SG"
              type="number"
              value={formData.targetSg}
              onChange={(e) => handleInputChange('targetSg', parseFloat(e.target.value))}
              inputProps={{ min: 1.0, max: 1.2, step: 0.001 }}
              required
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Target Brix (°Bx)"
              type="number"
              value={formData.targetBrix}
              onChange={(e) => handleInputChange('targetBrix', parseFloat(e.target.value))}
              inputProps={{ min: 0, max: 50, step: 0.1 }}
              required
            />
          </Grid>

          {/* Byproduct Tracking */}
          <Grid item xs={12}>
            <Typography variant="h6" gutterBottom>
              Byproduct Tracking
            </Typography>
            <Alert severity="info" sx={{ mb: 2 }}>
              Select which byproducts to track during processing
            </Alert>
          </Grid>
          <Grid item xs={12}>
            <FormGroup>
              <Grid container spacing={2}>
                <Grid item xs={12} md={6}>
                  <Card variant="outlined">
                    <CardContent>
                      <FormControlLabel
                        control={
                          <Checkbox
                            checked={formData.byproducts.peels}
                            onChange={() => handleByproductChange('peels')}
                          />
                        }
                        label="Peels - Oils"
                      />
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Card variant="outlined">
                    <CardContent>
                      <FormControlLabel
                        control={
                          <Checkbox
                            checked={formData.byproducts.pulp}
                            onChange={() => handleByproductChange('pulp')}
                          />
                        }
                        label="Pulp - Acids/Flavor"
                      />
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Card variant="outlined">
                    <CardContent>
                      <FormControlLabel
                        control={
                          <Checkbox
                            checked={formData.byproducts.rejects}
                            onChange={() => handleByproductChange('rejects')}
                          />
                        }
                        label="Rejects - Cleaners/Compost"
                      />
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Card variant="outlined">
                    <CardContent>
                      <FormControlLabel
                        control={
                          <Checkbox
                            checked={formData.byproducts.skins}
                            onChange={() => handleByproductChange('skins')}
                          />
                        }
                        label="Skins/Seeds - Enzymes"
                      />
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>
            </FormGroup>
          </Grid>

          {/* Notes */}
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Additional Notes"
              multiline
              rows={4}
              value={formData.notes}
              onChange={(e) => handleInputChange('notes', e.target.value)}
            />
          </Grid>

          {/* Submit Button */}
          <Grid item xs={12}>
            <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 2 }}>
              <Button
                variant="contained"
                size="large"
                startIcon={<SaveIcon />}
                onClick={handleSubmit}
              >
                Create Batch
              </Button>
            </Box>
          </Grid>
        </Grid>
      </Paper>
    </Box>
  );
};

export default EnhancedBatchForm;
