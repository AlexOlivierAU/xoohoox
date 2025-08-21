import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Typography,
} from '@mui/material';

interface UpscaleResult {
  yield_amount: number;
  abv_result: number;
  compound_summary: string;
}

interface Props {
  open: boolean;
  onClose: () => void;
  onSubmit: (result: UpscaleResult) => void;
  upscaleStage: string;
  upscaleVolume: number;
}

export const UpscaleResultDialog: React.FC<Props> = ({
  open,
  onClose,
  onSubmit,
  upscaleStage,
  upscaleVolume,
}) => {
  const [result, setResult] = React.useState<UpscaleResult>({
    yield_amount: 0,
    abv_result: 0,
    compound_summary: '',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(result);
  };

  const isValid = result.yield_amount > 0 && result.abv_result > 0;

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <form onSubmit={handleSubmit}>
        <DialogTitle>
          Record Results for {upscaleStage} ({upscaleVolume}L)
        </DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
            <TextField
              label="Yield Amount"
              type="number"
              required
              value={result.yield_amount}
              onChange={(e) => setResult({ ...result, yield_amount: parseFloat(e.target.value) })}
              inputProps={{ step: 0.1, min: 0 }}
              helperText="Enter yield in L (use decimals for mL)"
            />
            <TextField
              label="ABV Result"
              type="number"
              required
              value={result.abv_result}
              onChange={(e) => setResult({ ...result, abv_result: parseFloat(e.target.value) })}
              inputProps={{ step: 0.1, min: 0, max: 100 }}
              helperText="Enter ABV percentage"
            />
            <TextField
              label="Compound Notes"
              multiline
              rows={4}
              value={result.compound_summary}
              onChange={(e) => setResult({ ...result, compound_summary: e.target.value })}
              helperText="Enter any notes about compounds (methanol, esters, etc.)"
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={onClose}>Cancel</Button>
          <Button
            type="submit"
            variant="contained"
            color="primary"
            disabled={!isValid}
          >
            Save Results
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
}; 