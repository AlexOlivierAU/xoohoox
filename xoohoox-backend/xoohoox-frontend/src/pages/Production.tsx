import { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Stepper,
  Step,
  StepLabel,
  Card,
  CardContent,
  TextField,
  Button,
  Stack,
  Alert,
} from '@mui/material';
import {
  Science as ScienceIcon,
  Thermostat as ThermostatIcon,
  Biotech as BiotechIcon,
  LocalDrink as LocalDrinkIcon,
} from '@mui/icons-material';

// Process phase steps
const processSteps = [
  {
    label: 'Raw Material & Chemistry',
    icon: <ScienceIcon />,
    description: 'Initial preparation and chemistry adjustments'
  },
  {
    label: 'Heat Activation',
    icon: <ThermostatIcon />,
    description: 'Temperature control and nutrient preparation'
  },
  {
    label: 'Fermentation',
    icon: <BiotechIcon />,
    description: 'Monitor fermentation kinetics'
  },
  {
    label: 'Distillation',
    icon: <LocalDrinkIcon />,
    description: 'Distillation ladder progression'
  }
];

interface ProcessData {
  rawMaterial: {
    initialPh: number;
    initialSg: number;
    targetPh: number;
    targetSg: number;
    sodiumBicarbonate: number;
  };
  heatActivation: {
    temperature: number;
    restTime: number;
    nutrientMix: number;
    yeastAmount: number;
  };
  fermentation: {
    currentAbv: number;
    targetAbv: number;
    dailyReadings: Array<{
      date: string;
      abv: number;
      ph: number;
      temperature: number;
    }>;
  };
  distillation: {
    currentTest: number;
    yields: Array<{
      test: number;
      volume: number;
      yield: number;
    }>;
  };
}

export const Production = () => {
  const [activeStep, setActiveStep] = useState(0);
  const [processData, setProcessData] = useState<ProcessData>({
    rawMaterial: {
      initialPh: 1.8,
      initialSg: 1.03,
      targetPh: 5.0,
      targetSg: 1.07,
      sodiumBicarbonate: 11.5
    },
    heatActivation: {
      temperature: 31,
      restTime: 24,
      nutrientMix: 4.5,
      yeastAmount: 5
    },
    fermentation: {
      currentAbv: 5.2,
      targetAbv: 7.5,
      dailyReadings: [
        { date: '2024-04-12', abv: 5.2, ph: 4.2, temperature: 22 }
      ]
    },
    distillation: {
      currentTest: 3,
      yields: [
        { test: 3, volume: 1, yield: 0.1 }
      ]
    }
  });

  const handleUpdateProcessData = (phase: keyof ProcessData, data: any) => {
    setProcessData(prev => ({
      ...prev,
      [phase]: { ...prev[phase], ...data }
    }));
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Production Management
      </Typography>

      <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
        {processSteps.map((step, index) => (
          <Step key={step.label} completed={index < activeStep}>
            <StepLabel icon={step.icon}>
              <Typography variant="subtitle2">{step.label}</Typography>
              <Typography variant="caption" color="text.secondary">
                {step.description}
              </Typography>
            </StepLabel>
          </Step>
        ))}
      </Stepper>

      <Stack spacing={3}>
        {/* Raw Material & Chemistry Card */}
        <Card>
          <CardContent>
            <Stack direction="row" alignItems="center" spacing={2} sx={{ mb: 2 }}>
              <ScienceIcon color="primary" />
              <Typography variant="h6">Raw Material & Chemistry Prep</Typography>
              {processData.rawMaterial.initialPh < processData.rawMaterial.targetPh && (
                <Alert severity="warning" sx={{ ml: 'auto' }}>
                  pH adjustment needed
                </Alert>
              )}
            </Stack>
            <Stack spacing={2}>
              <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 2 }}>
                <TextField
                  label="Initial pH"
                  type="number"
                  value={processData.rawMaterial.initialPh}
                  onChange={(e) => handleUpdateProcessData('rawMaterial', { initialPh: parseFloat(e.target.value) })}
                  inputProps={{ step: 0.1 }}
                />
                <TextField
                  label="Initial SG"
                  type="number"
                  value={processData.rawMaterial.initialSg}
                  onChange={(e) => handleUpdateProcessData('rawMaterial', { initialSg: parseFloat(e.target.value) })}
                  inputProps={{ step: 0.01 }}
                />
                <TextField
                  label="Target pH"
                  type="number"
                  value={processData.rawMaterial.targetPh}
                  InputProps={{ readOnly: true }}
                />
                <TextField
                  label="Target SG"
                  type="number"
                  value={processData.rawMaterial.targetSg}
                  InputProps={{ readOnly: true }}
                />
              </Box>
              <Box>
                <Typography variant="subtitle2" gutterBottom>
                  Sodium Bicarbonate Required
                </Typography>
                <Typography variant="h5" color="primary">
                  {processData.rawMaterial.sodiumBicarbonate} kg
                </Typography>
              </Box>
            </Stack>
          </CardContent>
        </Card>

        {/* Heat Activation Card */}
        <Card>
          <CardContent>
            <Stack direction="row" alignItems="center" spacing={2} sx={{ mb: 2 }}>
              <ThermostatIcon color="primary" />
              <Typography variant="h6">Heat Activation & Nutrient Prep</Typography>
            </Stack>
            <Stack spacing={2}>
              <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 2 }}>
                <TextField
                  label="Temperature (°C)"
                  type="number"
                  value={processData.heatActivation.temperature}
                  onChange={(e) => handleUpdateProcessData('heatActivation', { temperature: parseFloat(e.target.value) })}
                  error={processData.heatActivation.temperature < 30 || processData.heatActivation.temperature > 32}
                  helperText="Target: 30-32°C"
                  inputProps={{ step: 0.1 }}
                />
                <TextField
                  label="Rest Time (hours)"
                  type="number"
                  value={processData.heatActivation.restTime}
                  onChange={(e) => handleUpdateProcessData('heatActivation', { restTime: parseFloat(e.target.value) })}
                  inputProps={{ step: 1 }}
                />
                <TextField
                  label="Nutrient Mix (g/L)"
                  type="number"
                  value={processData.heatActivation.nutrientMix}
                  onChange={(e) => handleUpdateProcessData('heatActivation', { nutrientMix: parseFloat(e.target.value) })}
                  helperText="Target: 4-5 g/L"
                  inputProps={{ step: 0.1 }}
                />
                <TextField
                  label="Yeast Amount (g/L)"
                  type="number"
                  value={processData.heatActivation.yeastAmount}
                  onChange={(e) => handleUpdateProcessData('heatActivation', { yeastAmount: parseFloat(e.target.value) })}
                  helperText="Target: 5 g/L"
                  inputProps={{ step: 0.1 }}
                />
              </Box>
            </Stack>
          </CardContent>
        </Card>

        {/* Fermentation Card */}
        <Card>
          <CardContent>
            <Stack direction="row" alignItems="center" spacing={2} sx={{ mb: 2 }}>
              <BiotechIcon color="primary" />
              <Typography variant="h6">Fermentation Monitoring</Typography>
              {processData.fermentation.currentAbv < processData.fermentation.targetAbv && (
                <Alert severity="info" sx={{ ml: 'auto' }}>
                  Fermentation in progress
                </Alert>
              )}
            </Stack>
            <Stack spacing={2}>
              <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 2 }}>
                <TextField
                  label="Current ABV (%)"
                  type="number"
                  value={processData.fermentation.currentAbv}
                  onChange={(e) => handleUpdateProcessData('fermentation', { currentAbv: parseFloat(e.target.value) })}
                  inputProps={{ step: 0.1 }}
                />
                <TextField
                  label="Target ABV (%)"
                  type="number"
                  value={processData.fermentation.targetAbv}
                  InputProps={{ readOnly: true }}
                />
              </Box>
              <Typography variant="subtitle2" gutterBottom>
                Daily Readings
              </Typography>
              <Box sx={{ maxHeight: 200, overflow: 'auto' }}>
                <Stack spacing={1}>
                  {processData.fermentation.dailyReadings.map((reading, index) => (
                    <Paper key={index} sx={{ p: 2 }}>
                      <Stack direction="row" spacing={2} alignItems="center">
                        <Typography variant="body2" color="text.secondary">
                          {reading.date}
                        </Typography>
                        <Typography>
                          ABV: {reading.abv}%
                        </Typography>
                        <Typography>
                          pH: {reading.ph}
                        </Typography>
                        <Typography>
                          Temp: {reading.temperature}°C
                        </Typography>
                      </Stack>
                    </Paper>
                  ))}
                </Stack>
              </Box>
              <Button
                variant="outlined"
                onClick={() => {
                  const newReading = {
                    date: new Date().toISOString().split('T')[0],
                    abv: processData.fermentation.currentAbv,
                    ph: 4.2,
                    temperature: 22
                  };
                  handleUpdateProcessData('fermentation', {
                    dailyReadings: [...processData.fermentation.dailyReadings, newReading]
                  });
                }}
              >
                Add Daily Reading
              </Button>
            </Stack>
          </CardContent>
        </Card>

        {/* Distillation Card */}
        <Card>
          <CardContent>
            <Stack direction="row" alignItems="center" spacing={2} sx={{ mb: 2 }}>
              <LocalDrinkIcon color="primary" />
              <Typography variant="h6">Distillation Ladder</Typography>
            </Stack>
            <Stack spacing={2}>
              <Typography variant="subtitle2" gutterBottom>
                Current Test: {processData.distillation.currentTest}
              </Typography>
              <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: 2 }}>
                {[
                  { test: 3, volume: 1, expectedYield: 0.1 },
                  { test: 4, volume: 5, expectedYield: 0.5 },
                  { test: 5, volume: 30, expectedYield: 3 },
                  { test: 6, volume: 100, expectedYield: 15 }
                ].map((testData) => (
                  <Paper
                    key={testData.test}
                    sx={{
                      p: 2,
                      bgcolor: processData.distillation.currentTest === testData.test ? 'action.selected' : 'background.paper'
                    }}
                  >
                    <Typography variant="subtitle2">
                      Test {testData.test}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Volume: {testData.volume}L
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Expected Yield: {testData.expectedYield}L
                    </Typography>
                    {processData.distillation.yields.find(y => y.test === testData.test) && (
                      <Typography variant="body2" color="primary">
                        Actual Yield: {processData.distillation.yields.find(y => y.test === testData.test)?.yield}L
                      </Typography>
                    )}
                  </Paper>
                ))}
              </Box>
              <Button
                variant="contained"
                disabled={processData.distillation.currentTest >= 6}
                onClick={() => {
                  const nextTest = processData.distillation.currentTest + 1;
                  handleUpdateProcessData('distillation', {
                    currentTest: nextTest,
                    yields: [
                      ...processData.distillation.yields,
                      { test: nextTest, volume: [1, 5, 30, 100][nextTest - 3], yield: 0 }
                    ]
                  });
                }}
              >
                Progress to Next Test
              </Button>
            </Stack>
          </CardContent>
        </Card>
      </Stack>
    </Box>
  );
}; 