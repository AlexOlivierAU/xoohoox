import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  TextField,
  Button,
  Chip,
  IconButton,
  Tooltip,
  Alert,
  CircularProgress,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Stack,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import {
  Add as AddIcon,
  Visibility as ViewIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  FilterList as FilterIcon,
  Search as SearchIcon,
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon,
  Error as ErrorIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import qualityService from '../services/qualityService';

interface QualityCheck {
  id: string;
  batch_id: string;
  batch_number: string;
  check_type: string;
  result: 'pass' | 'warning' | 'fail';
  timestamp: string;
  performed_by: string;
  notes: string;
  parameters: {
    temperature?: number;
    ph_level?: number;
    brix_level?: number;
    alcohol_content?: number;
  };
}

const QualityChecks = () => {
  const navigate = useNavigate();
  const [qualityChecks, setQualityChecks] = useState<QualityCheck[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [searchTerm, setSearchTerm] = useState('');
  const [resultFilter, setResultFilter] = useState('all');
  const [checkTypeFilter, setCheckTypeFilter] = useState('all');
  const [selectedCheck, setSelectedCheck] = useState<QualityCheck | null>(null);
  const [dialogOpen, setDialogOpen] = useState(false);

  useEffect(() => {
    fetchQualityChecks();
  }, []);

  const fetchQualityChecks = async () => {
    try {
      setLoading(true);
      const response = await qualityService.getQualityChecks();
      setQualityChecks(response.items);
    } catch (err: any) {
      setError('Failed to fetch quality checks');
      console.error('Error fetching quality checks:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
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

  const getResultIcon = (result: string) => {
    switch (result) {
      case 'pass':
        return <CheckCircleIcon color="success" />;
      case 'warning':
        return <WarningIcon color="warning" />;
      case 'fail':
        return <ErrorIcon color="error" />;
      default:
        return <CheckCircleIcon />;
    }
  };

  const filteredChecks = qualityChecks.filter((check) => {
    const matchesSearch = 
      check.batch_number.toLowerCase().includes(searchTerm.toLowerCase()) ||
      check.check_type.toLowerCase().includes(searchTerm.toLowerCase()) ||
      check.performed_by.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesResult = resultFilter === 'all' || check.result === resultFilter;
    const matchesType = checkTypeFilter === 'all' || check.check_type === checkTypeFilter;
    
    return matchesSearch && matchesResult && matchesType;
  });

  const paginatedChecks = filteredChecks.slice(
    page * rowsPerPage,
    page * rowsPerPage + rowsPerPage
  );

  const handleViewCheck = (check: QualityCheck) => {
    setSelectedCheck(check);
    setDialogOpen(true);
  };

  const handleEditCheck = (checkId: string) => {
    navigate(`/quality-checks/${checkId}/edit`);
  };

  const handleDeleteCheck = async (checkId: string) => {
    if (window.confirm('Are you sure you want to delete this quality check?')) {
      try {
        await qualityService.deleteQualityCheck(checkId);
        fetchQualityChecks();
      } catch (err: any) {
        setError('Failed to delete quality check');
      }
    }
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
    setSelectedCheck(null);
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Quality Control
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => navigate('/quality-checks/new')}
        >
          New Quality Check
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Paper sx={{ p: 2, mb: 2 }}>
        <Stack direction="row" spacing={2} alignItems="center" sx={{ mb: 2 }}>
          <TextField
            placeholder="Search quality checks..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            InputProps={{
              startAdornment: <SearchIcon sx={{ mr: 1, color: 'text.secondary' }} />,
            }}
            sx={{ minWidth: 300 }}
          />
          
          <FormControl sx={{ minWidth: 150 }}>
            <InputLabel>Result</InputLabel>
            <Select
              value={resultFilter}
              label="Result"
              onChange={(e) => setResultFilter(e.target.value)}
            >
              <MenuItem value="all">All Results</MenuItem>
              <MenuItem value="pass">Pass</MenuItem>
              <MenuItem value="warning">Warning</MenuItem>
              <MenuItem value="fail">Fail</MenuItem>
            </Select>
          </FormControl>

          <FormControl sx={{ minWidth: 150 }}>
            <InputLabel>Check Type</InputLabel>
            <Select
              value={checkTypeFilter}
              label="Check Type"
              onChange={(e) => setCheckTypeFilter(e.target.value)}
            >
              <MenuItem value="all">All Types</MenuItem>
              <MenuItem value="temperature">Temperature</MenuItem>
              <MenuItem value="ph_level">pH Level</MenuItem>
              <MenuItem value="brix_level">Brix Level</MenuItem>
              <MenuItem value="alcohol_content">Alcohol Content</MenuItem>
              <MenuItem value="visual_inspection">Visual Inspection</MenuItem>
              <MenuItem value="microbial_test">Microbial Test</MenuItem>
            </Select>
          </FormControl>

          <Button
            variant="outlined"
            startIcon={<FilterIcon />}
            onClick={() => {
              setSearchTerm('');
              setResultFilter('all');
              setCheckTypeFilter('all');
            }}
          >
            Clear Filters
          </Button>
        </Stack>

        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Batch Number</TableCell>
                <TableCell>Check Type</TableCell>
                <TableCell>Result</TableCell>
                <TableCell>Performed By</TableCell>
                <TableCell>Timestamp</TableCell>
                <TableCell align="center">Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {paginatedChecks.map((check) => (
                <TableRow key={check.id} hover>
                  <TableCell>
                    <Typography variant="subtitle2" fontWeight="bold">
                      {check.batch_number}
                    </Typography>
                  </TableCell>
                  <TableCell>{check.check_type}</TableCell>
                  <TableCell>
                    <Chip
                      icon={getResultIcon(check.result)}
                      label={check.result.toUpperCase()}
                      color={getResultColor(check.result) as any}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>{check.performed_by}</TableCell>
                  <TableCell>
                    {new Date(check.timestamp).toLocaleString()}
                  </TableCell>
                  <TableCell align="center">
                    <Stack direction="row" spacing={1} justifyContent="center">
                      <Tooltip title="View Details">
                        <IconButton
                          size="small"
                          onClick={() => handleViewCheck(check)}
                        >
                          <ViewIcon />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Edit Check">
                        <IconButton
                          size="small"
                          onClick={() => handleEditCheck(check.id)}
                        >
                          <EditIcon />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Delete Check">
                        <IconButton
                          size="small"
                          color="error"
                          onClick={() => handleDeleteCheck(check.id)}
                        >
                          <DeleteIcon />
                        </IconButton>
                      </Tooltip>
                    </Stack>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>

        <TablePagination
          rowsPerPageOptions={[5, 10, 25]}
          component="div"
          count={filteredChecks.length}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={handleChangePage}
          onRowsPerPageChange={handleChangeRowsPerPage}
        />
      </Paper>

      {/* Quality Check Details Dialog */}
      <Dialog open={dialogOpen} onClose={handleCloseDialog} maxWidth="md" fullWidth>
        <DialogTitle>
          Quality Check Details
        </DialogTitle>
        <DialogContent>
          {selectedCheck && (
            <Box sx={{ mt: 2 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                <Typography variant="h6">
                  Batch {selectedCheck.batch_number}
                </Typography>
                <Chip
                  icon={getResultIcon(selectedCheck.result)}
                  label={selectedCheck.result.toUpperCase()}
                  color={getResultColor(selectedCheck.result) as any}
                />
              </Box>
              
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3, mb: 3 }}>
                <Box>
                  <Typography variant="body2" color="text.secondary">
                    Check Type
                  </Typography>
                  <Typography variant="body1">
                    {selectedCheck.check_type}
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="body2" color="text.secondary">
                    Performed By
                  </Typography>
                  <Typography variant="body1">
                    {selectedCheck.performed_by}
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="body2" color="text.secondary">
                    Timestamp
                  </Typography>
                  <Typography variant="body1">
                    {new Date(selectedCheck.timestamp).toLocaleString()}
                  </Typography>
                </Box>
              </Box>

              {selectedCheck.parameters && Object.keys(selectedCheck.parameters).length > 0 && (
                <Box sx={{ mb: 3 }}>
                  <Typography variant="h6" gutterBottom>
                    Parameters
                  </Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
                    {selectedCheck.parameters.temperature && (
                      <Chip label={`Temperature: ${selectedCheck.parameters.temperature}°C`} />
                    )}
                    {selectedCheck.parameters.ph_level && (
                      <Chip label={`pH Level: ${selectedCheck.parameters.ph_level}`} />
                    )}
                    {selectedCheck.parameters.brix_level && (
                      <Chip label={`Brix Level: ${selectedCheck.parameters.brix_level}°Bx`} />
                    )}
                    {selectedCheck.parameters.alcohol_content && (
                      <Chip label={`Alcohol: ${selectedCheck.parameters.alcohol_content}%`} />
                    )}
                  </Box>
                </Box>
              )}

              {selectedCheck.notes && (
                <Box>
                  <Typography variant="h6" gutterBottom>
                    Notes
                  </Typography>
                  <Typography variant="body1">
                    {selectedCheck.notes}
                  </Typography>
                </Box>
              )}
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Close</Button>
          {selectedCheck && (
            <Button 
              variant="contained"
              onClick={() => {
                handleCloseDialog();
                handleEditCheck(selectedCheck.id);
              }}
            >
              Edit
            </Button>
          )}
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default QualityChecks;
