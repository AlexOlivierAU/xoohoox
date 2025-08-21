import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import {
  Container,
  Box,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Typography,
  CircularProgress,
} from '@mui/material';
import { TrialInfo } from '../components/TrialInfo';
import { UpscaleHistory } from '../components/UpscaleHistory';
import { UpscaleResultDialog } from '../components/UpscaleResultDialog';
import { useUpscaleActions } from '../hooks/useUpscaleActions';
import axios from 'axios';

interface Trial {
  id: number;
  juice_variant: string;
  yeast_strain: string;
  initial_sg: number;
  target_abv: number;
  status: string;
  notes: string;
}

export const TrialDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [trial, setTrial] = useState<Trial | null>(null);
  const [loading, setLoading] = useState(true);
  const [confirmDialogOpen, setConfirmDialogOpen] = useState(false);
  const [resultDialogOpen, setResultDialogOpen] = useState(false);
  const [selectedUpscaleId, setSelectedUpscaleId] = useState<number | null>(null);

  const {
    upscales,
    loading: upscalesLoading,
    fetchUpscales,
    startNextUpscale,
    updateUpscaleResults,
    completeUpscale,
    canStartNextUpscale,
  } = useUpscaleActions(Number(id));

  useEffect(() => {
    const fetchTrial = async () => {
      try {
        const response = await axios.get(`/api/v1/trials/${id}`);
        setTrial(response.data);
      } catch (error) {
        console.error('Error fetching trial:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchTrial();
    fetchUpscales();
  }, [id, fetchUpscales]);

  const handleStartUpscale = async () => {
    await startNextUpscale();
    setConfirmDialogOpen(false);
  };

  const handleRecordYield = (upscaleId: number) => {
    setSelectedUpscaleId(upscaleId);
    setResultDialogOpen(true);
  };

  const handleResultSubmit = async (results: any) => {
    if (selectedUpscaleId) {
      await updateUpscaleResults(selectedUpscaleId, results);
      await completeUpscale(selectedUpscaleId);
      setResultDialogOpen(false);
      setSelectedUpscaleId(null);
    }
  };

  if (loading || !trial) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <TrialInfo trial={trial} />

        <Box sx={{ mb: 3 }}>
          <UpscaleHistory
            upscales={upscales}
            onStartUpscale={() => setConfirmDialogOpen(true)}
            onRecordYield={handleRecordYield}
            onInputCompound={handleRecordYield}
            onMarkComplete={completeUpscale}
          />
        </Box>

        {trial.status === 'Fermenting' && canStartNextUpscale() && (
          <Button
            variant="contained"
            color="primary"
            onClick={() => setConfirmDialogOpen(true)}
          >
            Start Next Upscale
          </Button>
        )}

        {/* Confirmation Dialog */}
        <Dialog
          open={confirmDialogOpen}
          onClose={() => setConfirmDialogOpen(false)}
        >
          <DialogTitle>Start New Upscale</DialogTitle>
          <DialogContent>
            <Typography>
              Are you sure you want to start the next upscale stage?
              This action cannot be undone.
            </Typography>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setConfirmDialogOpen(false)}>Cancel</Button>
            <Button onClick={handleStartUpscale} variant="contained" color="primary">
              Start Upscale
            </Button>
          </DialogActions>
        </Dialog>

        {/* Result Dialog */}
        {selectedUpscaleId && (
          <UpscaleResultDialog
            open={resultDialogOpen}
            onClose={() => {
              setResultDialogOpen(false);
              setSelectedUpscaleId(null);
            }}
            onSubmit={handleResultSubmit}
            upscaleStage={upscales.find(u => u.id === selectedUpscaleId)?.stage || ''}
            upscaleVolume={upscales.find(u => u.id === selectedUpscaleId)?.volume || 0}
          />
        )}
      </Box>
    </Container>
  );
}; 