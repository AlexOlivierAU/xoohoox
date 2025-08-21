import React from 'react';
import {
  Paper,
  Typography,
  Grid,
  Box,
  Chip,
} from '@mui/material';

interface Trial {
  id: number;
  juice_variant: string;
  yeast_strain: string;
  initial_sg: number;
  target_abv: number;
  status: string;
  notes: string;
}

interface Props {
  trial: Trial;
}

export const TrialInfo: React.FC<Props> = ({ trial }) => {
  return (
    <Paper sx={{ p: 3, mb: 3 }}>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Typography variant="h6" gutterBottom>
            Trial Details
          </Typography>
        </Grid>
        
        <Grid item xs={12} sm={6}>
          <Box>
            <Typography variant="subtitle2" color="text.secondary">
              Juice Type
            </Typography>
            <Typography variant="body1">
              {trial.juice_variant}
            </Typography>
          </Box>
        </Grid>

        <Grid item xs={12} sm={6}>
          <Box>
            <Typography variant="subtitle2" color="text.secondary">
              Yeast Strain
            </Typography>
            <Typography variant="body1">
              {trial.yeast_strain}
            </Typography>
          </Box>
        </Grid>

        <Grid item xs={12} sm={6}>
          <Box>
            <Typography variant="subtitle2" color="text.secondary">
              Initial SG
            </Typography>
            <Typography variant="body1">
              {trial.initial_sg.toFixed(3)}
            </Typography>
          </Box>
        </Grid>

        <Grid item xs={12} sm={6}>
          <Box>
            <Typography variant="subtitle2" color="text.secondary">
              Target ABV
            </Typography>
            <Typography variant="body1">
              {trial.target_abv}%
            </Typography>
          </Box>
        </Grid>

        <Grid item xs={12}>
          <Box sx={{ mt: 1 }}>
            <Chip
              label={trial.status}
              color={trial.status === 'Fermenting' ? 'primary' : 'default'}
              size="small"
            />
          </Box>
        </Grid>

        {trial.notes && (
          <Grid item xs={12}>
            <Box>
              <Typography variant="subtitle2" color="text.secondary">
                Notes
              </Typography>
              <Typography variant="body2" sx={{ mt: 1 }}>
                {trial.notes}
              </Typography>
            </Box>
          </Grid>
        )}
      </Grid>
    </Paper>
  );
}; 