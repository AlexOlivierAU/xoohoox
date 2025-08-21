import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  Grid,
  Typography,
  Button,
  Box,
  Divider,
  IconButton,
  TextField,
  MenuItem,
} from '@mui/material';
import { Close as CloseIcon } from '@mui/icons-material';
import { LineChart } from '@mui/x-charts/LineChart';

interface DailyReading {
  date: string;
  sg: number;
  abv: number;
  temperature: number;
  ph: number;
  notes?: string;
}

interface Trial {
  trial_id: string;
  juice_variant: string;
  yeast_strain: string;
  sg: number;
  current_abv: number;
  path_taken: 'vinegar' | 'distillation' | 'archived' | null;
  status: string;
  daily_readings: DailyReading[];
  start_date: string;
  target_abv: number;
  notes: string;
}

interface FermentationTrialDetailsProps {
  trial: Trial | null;
  open: boolean;
  onClose: () => void;
  onPathChange: (trialId: string, path: string) => void;
  onAddReading: (trialId: string, reading: Omit<DailyReading, 'date'>) => void;
}

export const FermentationTrialDetails: React.FC<FermentationTrialDetailsProps> = ({
  trial,
  open,
  onClose,
  onPathChange,
  onAddReading,
}) => {
  const [newReading, setNewReading] = React.useState({
    sg: 0,
    abv: 0,
    temperature: 20,
    ph: 7,
    notes: '',
  });

  if (!trial) return null;

  const handleReadingSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onAddReading(trial.trial_id, newReading);
    setNewReading({
      sg: 0,
      abv: 0,
      temperature: 20,
      ph: 7,
      notes: '',
    });
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Typography variant="h6">
            Trial Details: {trial.trial_id}
          </Typography>
          <IconButton onClick={onClose} size="small" aria-label="close dialog">
            <CloseIcon />
          </IconButton>
        </Box>
      </DialogTitle>
      <DialogContent>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Typography variant="subtitle2">Basic Information</Typography>
            <Box mt={1}>
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Typography variant="body2" color="textSecondary">
                    Juice Variant
                  </Typography>
                  <Typography variant="body1">{trial.juice_variant}</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="textSecondary">
                    Yeast Strain
                  </Typography>
                  <Typography variant="body1">{trial.yeast_strain}</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="textSecondary">
                    Current SG
                  </Typography>
                  <Typography variant="body1">{trial.sg.toFixed(3)}</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="textSecondary">
                    Current ABV
                  </Typography>
                  <Typography variant="body1">
                    {trial.current_abv.toFixed(1)}%
                  </Typography>
                </Grid>
                <Grid item xs={12}>
                  <Typography variant="body2" color="textSecondary">
                    Notes
                  </Typography>
                  <Typography variant="body1">{trial.notes || '—'}</Typography>
                </Grid>
              </Grid>
            </Box>
          </Grid>
          <Grid item xs={12} md={6}>
            <Typography variant="subtitle2">Path Selection</Typography>
            <Box mt={1}>
              <TextField
                select
                fullWidth
                label="Current Path"
                value={trial.path_taken || ''}
                onChange={(e) => onPathChange(trial.trial_id, e.target.value)}
              >
                <MenuItem value="">Not Selected</MenuItem>
                <MenuItem value="vinegar">Vinegar</MenuItem>
                <MenuItem value="distillation">Distillation</MenuItem>
                <MenuItem value="archived">Archive</MenuItem>
              </TextField>
            </Box>
          </Grid>
          <Grid item xs={12}>
            <Divider sx={{ my: 2 }} />
            <Typography variant="subtitle2">Fermentation Progress</Typography>
            <Box mt={2} height={300}>
              <LineChart
                xAxis={[{
                  data: trial.daily_readings.map((r) => new Date(r.date).getTime()),
                  scaleType: 'time',
                }]}
                series={[
                  {
                    data: trial.daily_readings.map((r) => r.sg),
                    label: 'Specific Gravity',
                    area: true,
                    showMark: false,
                  },
                  {
                    data: trial.daily_readings.map((r) => r.abv),
                    label: 'ABV %',
                    color: '#2196f3',
                    showMark: false,
                  },
                ]}
                height={300}
              />
            </Box>
          </Grid>
          <Grid item xs={12}>
            <Divider sx={{ my: 2 }} />
            <Typography variant="subtitle2">Add Daily Reading</Typography>
            <Box component="form" onSubmit={handleReadingSubmit} mt={2}>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={3}>
                  <TextField
                    fullWidth
                    label="SG"
                    type="number"
                    inputProps={{ step: 0.001 }}
                    value={newReading.sg}
                    onChange={(e) =>
                      setNewReading({ ...newReading, sg: parseFloat(e.target.value) })
                    }
                  />
                </Grid>
                <Grid item xs={12} sm={3}>
                  <TextField
                    fullWidth
                    label="ABV %"
                    type="number"
                    inputProps={{ step: 0.1 }}
                    value={newReading.abv}
                    onChange={(e) =>
                      setNewReading({ ...newReading, abv: parseFloat(e.target.value) })
                    }
                  />
                </Grid>
                <Grid item xs={12} sm={3}>
                  <TextField
                    fullWidth
                    label="Temperature (°C)"
                    type="number"
                    inputProps={{ step: 0.1 }}
                    value={newReading.temperature}
                    onChange={(e) =>
                      setNewReading({
                        ...newReading,
                        temperature: parseFloat(e.target.value),
                      })
                    }
                  />
                </Grid>
                <Grid item xs={12} sm={3}>
                  <TextField
                    fullWidth
                    label="pH"
                    type="number"
                    inputProps={{ step: 0.1 }}
                    value={newReading.ph}
                    onChange={(e) =>
                      setNewReading({ ...newReading, ph: parseFloat(e.target.value) })
                    }
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="Notes"
                    multiline
                    rows={2}
                    value={newReading.notes}
                    onChange={(e) =>
                      setNewReading({ ...newReading, notes: e.target.value })
                    }
                  />
                </Grid>
                <Grid item xs={12}>
                  <Button
                    type="submit"
                    variant="contained"
                    color="primary"
                    fullWidth
                  >
                    Add Reading
                  </Button>
                </Grid>
              </Grid>
            </Box>
          </Grid>
        </Grid>
      </DialogContent>
    </Dialog>
  );
}; 