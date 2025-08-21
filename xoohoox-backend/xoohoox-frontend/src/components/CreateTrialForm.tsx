import React from 'react';
import {
  Box,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  Grid,
  TextField,
  MenuItem,
  IconButton,
  Typography,
} from '@mui/material';
import { Close as CloseIcon } from '@mui/icons-material';

interface CreateTrialFormProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (trialData: TrialFormData) => void;
  juiceVariants: string[];
  yeastStrains: string[];
}

interface TrialFormData {
  juice_variant: string;
  yeast_strain: string;
  target_abv: number;
  initial_sg: number;
  notes: string;
}

export const CreateTrialForm: React.FC<CreateTrialFormProps> = ({
  open,
  onClose,
  onSubmit,
  juiceVariants,
  yeastStrains,
}) => {
  const [formData, setFormData] = React.useState<TrialFormData>({
    juice_variant: '',
    yeast_strain: '',
    target_abv: 0,
    initial_sg: 1.000,
    notes: '',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
    setFormData({
      juice_variant: '',
      yeast_strain: '',
      target_abv: 0,
      initial_sg: 1.000,
      notes: '',
    });
    onClose();
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Typography variant="h6">Create New Trial</Typography>
          <IconButton onClick={onClose} size="small" aria-label="close dialog">
            <CloseIcon />
          </IconButton>
        </Box>
      </DialogTitle>
      <DialogContent>
        <Box component="form" onSubmit={handleSubmit} mt={2}>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <TextField
                select
                fullWidth
                required
                label="Juice Variant"
                value={formData.juice_variant}
                onChange={(e) =>
                  setFormData({ ...formData, juice_variant: e.target.value })
                }
              >
                {juiceVariants.map((variant) => (
                  <MenuItem key={variant} value={variant}>
                    {variant}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>
            <Grid item xs={12}>
              <TextField
                select
                fullWidth
                required
                label="Yeast Strain"
                value={formData.yeast_strain}
                onChange={(e) =>
                  setFormData({ ...formData, yeast_strain: e.target.value })
                }
              >
                {yeastStrains.map((strain) => (
                  <MenuItem key={strain} value={strain}>
                    {strain}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                required
                type="number"
                label="Target ABV %"
                inputProps={{ step: 0.1, min: 0, max: 20 }}
                value={formData.target_abv}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    target_abv: parseFloat(e.target.value),
                  })
                }
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                required
                type="number"
                label="Initial SG"
                inputProps={{ step: 0.001, min: 1.000, max: 1.200 }}
                value={formData.initial_sg}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    initial_sg: parseFloat(e.target.value),
                  })
                }
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                multiline
                rows={4}
                label="Notes"
                value={formData.notes}
                onChange={(e) =>
                  setFormData({ ...formData, notes: e.target.value })
                }
              />
            </Grid>
            <Grid item xs={12}>
              <Button
                type="submit"
                variant="contained"
                color="primary"
                fullWidth
                disabled={!formData.juice_variant || !formData.yeast_strain}
              >
                Create Trial
              </Button>
            </Grid>
          </Grid>
        </Box>
      </DialogContent>
    </Dialog>
  );
}; 