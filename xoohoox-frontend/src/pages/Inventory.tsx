import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  Alert,
  CircularProgress,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
} from '@mui/icons-material';

interface InventoryItem {
  id: string;
  name: string;
  category: string;
  quantity: number;
  unit: string;
  min_threshold: number;
  max_threshold: number;
  supplier: string;
  last_updated: string;
  status: 'in_stock' | 'low_stock' | 'out_of_stock' | 'expired';
  expiry_date?: string;
  location: string;
  cost_per_unit: number;
}

const Inventory = () => {
  const [items, setItems] = useState<InventoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [openDialog, setOpenDialog] = useState(false);
  const [editingItem, setEditingItem] = useState<InventoryItem | null>(null);

  const [newItem, setNewItem] = useState<Partial<InventoryItem>>({
    name: '',
    category: '',
    quantity: 0,
    unit: 'kg',
    min_threshold: 0,
    max_threshold: 0,
    supplier: '',
    location: '',
    cost_per_unit: 0,
  });

  useEffect(() => {
    fetchInventory();
  }, []);

  const fetchInventory = async () => {
    try {
      setLoading(true);
      // Mock data for now - replace with actual API call
      const mockItems: InventoryItem[] = [
        {
          id: '1',
          name: 'Apples',
          category: 'Fruits',
          quantity: 500,
          unit: 'kg',
          min_threshold: 100,
          max_threshold: 1000,
          supplier: 'Fresh Fruits Co.',
          last_updated: '2024-01-15',
          status: 'in_stock',
          location: 'Cold Storage A',
          cost_per_unit: 2.50,
        },
        {
          id: '2',
          name: 'Oranges',
          category: 'Fruits',
          quantity: 75,
          unit: 'kg',
          min_threshold: 100,
          max_threshold: 800,
          supplier: 'Citrus Suppliers',
          last_updated: '2024-01-14',
          status: 'low_stock',
          location: 'Cold Storage B',
          cost_per_unit: 3.20,
        },
        {
          id: '3',
          name: 'Sugar',
          category: 'Ingredients',
          quantity: 0,
          unit: 'kg',
          min_threshold: 50,
          max_threshold: 500,
          supplier: 'Sweet Supplies',
          last_updated: '2024-01-10',
          status: 'out_of_stock',
          location: 'Dry Storage',
          cost_per_unit: 1.80,
        },
        {
          id: '4',
          name: 'Citric Acid',
          category: 'Additives',
          quantity: 25,
          unit: 'kg',
          min_threshold: 10,
          max_threshold: 100,
          supplier: 'Chemical Co.',
          last_updated: '2024-01-12',
          status: 'in_stock',
          location: 'Chemical Storage',
          cost_per_unit: 8.50,
          expiry_date: '2024-06-15',
        },
      ];
      setItems(mockItems);
    } catch (err: any) {
      setError('Failed to fetch inventory');
      console.error('Error fetching inventory:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSaveItem = async () => {
    try {
      if (editingItem) {
        // Update existing item
        const updatedItems = items.map(item =>
          item.id === editingItem.id ? { ...editingItem, ...newItem } : item
        );
        setItems(updatedItems);
      } else {
        // Add new item
        const newInventoryItem: InventoryItem = {
          ...newItem as InventoryItem,
          id: Date.now().toString(),
          status: 'in_stock',
          last_updated: new Date().toISOString().split('T')[0],
        };
        setItems([...items, newInventoryItem]);
      }
      setOpenDialog(false);
      setEditingItem(null);
      setNewItem({
        name: '',
        category: '',
        quantity: 0,
        unit: 'kg',
        min_threshold: 0,
        max_threshold: 0,
        supplier: '',
        location: '',
        cost_per_unit: 0,
      });
    } catch (err: any) {
      setError('Failed to save item');
      console.error('Error saving item:', err);
    }
  };

  const handleEditItem = (item: InventoryItem) => {
    setEditingItem(item);
    setNewItem(item);
    setOpenDialog(true);
  };

  const handleDeleteItem = (itemId: string) => {
    if (window.confirm('Are you sure you want to delete this item?')) {
      setItems(items.filter(item => item.id !== itemId));
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'in_stock': return 'success';
      case 'low_stock': return 'warning';
      case 'out_of_stock': return 'error';
      case 'expired': return 'error';
      default: return 'default';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'in_stock': return <CheckCircleIcon />;
      case 'low_stock': return <WarningIcon />;
      case 'out_of_stock': return <WarningIcon />;
      case 'expired': return <WarningIcon />;
      default: return undefined;
    }
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
        <Typography variant="h4">Inventory Management</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setOpenDialog(true)}
        >
          Add Item
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>
      )}

      {/* Inventory Summary */}
      <Box sx={{ display: 'flex', gap: 3, mb: 4 }}>
        <Paper sx={{ p: 3, textAlign: 'center', flex: 1 }}>
          <Typography variant="h6" gutterBottom>Total Items</Typography>
          <Typography variant="h3" color="primary">{items.length}</Typography>
        </Paper>
        <Paper sx={{ p: 3, textAlign: 'center', flex: 1 }}>
          <Typography variant="h6" gutterBottom>Low Stock</Typography>
          <Typography variant="h3" color="warning.main">
            {items.filter(item => item.status === 'low_stock').length}
          </Typography>
        </Paper>
        <Paper sx={{ p: 3, textAlign: 'center', flex: 1 }}>
          <Typography variant="h6" gutterBottom>Out of Stock</Typography>
          <Typography variant="h3" color="error.main">
            {items.filter(item => item.status === 'out_of_stock').length}
          </Typography>
        </Paper>
        <Paper sx={{ p: 3, textAlign: 'center', flex: 1 }}>
          <Typography variant="h6" gutterBottom>Total Value</Typography>
          <Typography variant="h3" color="success.main">
            ${items.reduce((sum, item) => sum + (item.quantity * item.cost_per_unit), 0).toFixed(2)}
          </Typography>
        </Paper>
      </Box>

      {/* Inventory Table */}
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Category</TableCell>
              <TableCell>Quantity</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Supplier</TableCell>
              <TableCell>Location</TableCell>
              <TableCell>Last Updated</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {items.map((item) => (
              <TableRow key={item.id}>
                <TableCell>
                  <Typography variant="subtitle2" fontWeight="bold">
                    {item.name}
                  </Typography>
                </TableCell>
                <TableCell>
                  <Chip label={item.category} size="small" />
                </TableCell>
                <TableCell>
                  <Typography variant="body2">
                    {item.quantity} {item.unit}
                  </Typography>
                  {item.quantity <= item.min_threshold && (
                    <Typography variant="caption" color="warning.main">
                      Below threshold
                    </Typography>
                  )}
                </TableCell>
                <TableCell>
                  <Chip
                    icon={getStatusIcon(item.status)}
                    label={item.status.replace('_', ' ')}
                    color={getStatusColor(item.status)}
                    size="small"
                  />
                </TableCell>
                <TableCell>{item.supplier}</TableCell>
                <TableCell>{item.location}</TableCell>
                <TableCell>{item.last_updated}</TableCell>
                <TableCell>
                  <Tooltip title="Edit">
                    <IconButton size="small" onClick={() => handleEditItem(item)}>
                      <EditIcon />
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="Delete">
                    <IconButton size="small" color="error" onClick={() => handleDeleteItem(item.id)}>
                      <DeleteIcon />
                    </IconButton>
                  </Tooltip>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Add/Edit Dialog */}
      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>
          {editingItem ? 'Edit Inventory Item' : 'Add New Item'}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ mt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
            <TextField
              fullWidth
              label="Item Name"
              value={newItem.name}
              onChange={(e) => setNewItem({ ...newItem, name: e.target.value })}
            />
            <FormControl fullWidth>
              <InputLabel>Category</InputLabel>
              <Select
                value={newItem.category}
                label="Category"
                onChange={(e) => setNewItem({ ...newItem, category: e.target.value })}
              >
                <MenuItem value="Fruits">Fruits</MenuItem>
                <MenuItem value="Vegetables">Vegetables</MenuItem>
                <MenuItem value="Ingredients">Ingredients</MenuItem>
                <MenuItem value="Additives">Additives</MenuItem>
                <MenuItem value="Packaging">Packaging</MenuItem>
              </Select>
            </FormControl>
            <Box sx={{ display: 'flex', gap: 2 }}>
              <TextField
                fullWidth
                label="Quantity"
                type="number"
                value={newItem.quantity}
                onChange={(e) => setNewItem({ ...newItem, quantity: parseFloat(e.target.value) })}
              />
              <FormControl fullWidth>
                <InputLabel>Unit</InputLabel>
                <Select
                  value={newItem.unit}
                  label="Unit"
                  onChange={(e) => setNewItem({ ...newItem, unit: e.target.value })}
                >
                  <MenuItem value="kg">kg</MenuItem>
                  <MenuItem value="L">L</MenuItem>
                  <MenuItem value="pieces">pieces</MenuItem>
                  <MenuItem value="boxes">boxes</MenuItem>
                </Select>
              </FormControl>
            </Box>
            <Box sx={{ display: 'flex', gap: 2 }}>
              <TextField
                fullWidth
                label="Min Threshold"
                type="number"
                value={newItem.min_threshold}
                onChange={(e) => setNewItem({ ...newItem, min_threshold: parseFloat(e.target.value) })}
              />
              <TextField
                fullWidth
                label="Max Threshold"
                type="number"
                value={newItem.max_threshold}
                onChange={(e) => setNewItem({ ...newItem, max_threshold: parseFloat(e.target.value) })}
              />
            </Box>
            <TextField
              fullWidth
              label="Supplier"
              value={newItem.supplier}
              onChange={(e) => setNewItem({ ...newItem, supplier: e.target.value })}
            />
            <TextField
              fullWidth
              label="Location"
              value={newItem.location}
              onChange={(e) => setNewItem({ ...newItem, location: e.target.value })}
            />
            <TextField
              fullWidth
              label="Cost per Unit"
              type="number"
              value={newItem.cost_per_unit}
              onChange={(e) => setNewItem({ ...newItem, cost_per_unit: parseFloat(e.target.value) })}
            />
            <TextField
              fullWidth
              label="Expiry Date"
              type="date"
              value={newItem.expiry_date || ''}
              onChange={(e) => setNewItem({ ...newItem, expiry_date: e.target.value })}
              InputLabelProps={{ shrink: true }}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
          <Button onClick={handleSaveItem} variant="contained">
            {editingItem ? 'Update' : 'Add'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Inventory; 