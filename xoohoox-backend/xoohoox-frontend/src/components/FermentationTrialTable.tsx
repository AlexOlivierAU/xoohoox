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
  Chip,
  Tooltip,
  Typography,
} from '@mui/material';
import {
  Info as InfoIcon,
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon,
  Pause as PauseIcon,
} from '@mui/icons-material';

interface Trial {
  trial_id: string;
  juice_variant: string;
  yeast_strain: string;
  sg: number;
  current_abv: number;
  path_taken: 'vinegar' | 'distillation' | 'archived' | null;
  status: string;
}

interface FermentationTrialTableProps {
  trials: Trial[];
  onTrialClick: (trial: Trial) => void;
}

const getStatusIcon = (status: string) => {
  switch (status.toLowerCase()) {
    case 'running':
      return <CheckCircleIcon color="success" />;
    case 'paused':
      return <PauseIcon color="warning" />;
    case 'warning':
      return <WarningIcon color="error" />;
    default:
      return null;
  }
};

const getPathColor = (path: string | null) => {
  switch (path) {
    case 'vinegar':
      return 'warning';
    case 'distillation':
      return 'info';
    case 'archived':
      return 'default';
    default:
      return 'primary';
  }
};

export const FermentationTrialTable: React.FC<FermentationTrialTableProps> = ({
  trials,
  onTrialClick,
}) => {
  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Trial ID</TableCell>
            <TableCell>Juice Type</TableCell>
            <TableCell>Yeast</TableCell>
            <TableCell align="right">SG</TableCell>
            <TableCell align="right">ABV</TableCell>
            <TableCell>Path</TableCell>
            <TableCell>Status</TableCell>
            <TableCell align="center">Actions</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {trials.map((trial) => (
            <TableRow
              key={trial.trial_id}
              sx={{
                '&:hover': { backgroundColor: 'action.hover' },
                cursor: 'pointer',
              }}
              onClick={() => onTrialClick(trial)}
            >
              <TableCell>
                <Typography variant="body2" fontFamily="monospace">
                  {trial.trial_id}
                </Typography>
              </TableCell>
              <TableCell>{trial.juice_variant}</TableCell>
              <TableCell>{trial.yeast_strain}</TableCell>
              <TableCell align="right">{trial.sg.toFixed(3)}</TableCell>
              <TableCell align="right">{trial.current_abv.toFixed(1)}%</TableCell>
              <TableCell>
                {trial.path_taken ? (
                  <Chip
                    label={trial.path_taken}
                    color={getPathColor(trial.path_taken) as any}
                    size="small"
                  />
                ) : (
                  '—'
                )}
              </TableCell>
              <TableCell>
                <Tooltip title={trial.status}>
                  <span>{getStatusIcon(trial.status)}</span>
                </Tooltip>
              </TableCell>
              <TableCell align="center">
                <IconButton
                  size="small"
                  onClick={(e) => {
                    e.stopPropagation();
                    onTrialClick(trial);
                  }}
                >
                  <InfoIcon />
                </IconButton>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}; 