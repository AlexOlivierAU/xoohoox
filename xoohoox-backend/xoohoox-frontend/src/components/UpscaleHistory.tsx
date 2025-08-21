import React from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  IconButton,
  Tooltip,
  Box,
  Typography,
} from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import PendingIcon from '@mui/icons-material/Pending';
import { green } from '@mui/material/colors';

interface UpscaleRun {
  id: number;
  upscale_id: string;
  stage: string;
  volume: number;
  yield_amount: number | null;
  abv_result: number | null;
  compound_summary: string | null;
  status: 'pending' | 'complete' | 'failed';
  timestamp: string;
}

interface Props {
  upscales: UpscaleRun[];
  onStartUpscale: () => void;
  onRecordYield: (upscaleId: number) => void;
  onInputCompound: (upscaleId: number) => void;
  onMarkComplete: (upscaleId: number) => void;
}

export const UpscaleHistory: React.FC<Props> = ({
  upscales,
  onStartUpscale,
  onRecordYield,
  onInputCompound,
  onMarkComplete,
}) => {
  const formatVolume = (volume: number) => `${volume}L`;
  const formatYield = (yield_amount: number | null) => 
    yield_amount ? (yield_amount >= 1 ? `${yield_amount}L` : `${yield_amount * 1000}mL`) : '—';
  const formatABV = (abv: number | null) => abv ? `${abv}%` : '—';
  const formatDate = (timestamp: string) => 
    timestamp ? new Date(timestamp).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) : '—';

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Upscale History
      </Typography>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Stage</TableCell>
              <TableCell>Volume</TableCell>
              <TableCell>Date</TableCell>
              <TableCell>Yield</TableCell>
              <TableCell>ABV</TableCell>
              <TableCell>Compound</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {upscales.map((upscale) => (
              <TableRow key={upscale.id}>
                <TableCell>{upscale.stage}</TableCell>
                <TableCell>{formatVolume(upscale.volume)}</TableCell>
                <TableCell>{formatDate(upscale.timestamp)}</TableCell>
                <TableCell>{formatYield(upscale.yield_amount)}</TableCell>
                <TableCell>{formatABV(upscale.abv_result)}</TableCell>
                <TableCell>
                  {upscale.status === 'complete' ? (
                    <Tooltip title="Compounds OK">
                      <CheckCircleIcon sx={{ color: green[500] }} />
                    </Tooltip>
                  ) : (
                    <Tooltip title="Pending">
                      <IconButton
                        size="small"
                        onClick={() => onInputCompound(upscale.id)}
                      >
                        <PendingIcon />
                      </IconButton>
                    </Tooltip>
                  )}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}; 