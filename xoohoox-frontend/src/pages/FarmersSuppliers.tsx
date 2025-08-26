import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  TextField,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  Alert,
  CircularProgress,
  Card,
  CardContent,
  Avatar,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Agriculture as FarmIcon,
  Business as BusinessIcon,
  Phone as PhoneIcon,
  Email as EmailIcon,
  LocationOn as LocationIcon,
} from '@mui/icons-material';

interface Supplier {
  id: string;
  name: string;
  type: 'farmer' | 'supplier' | 'distributor';
  contact_person: string;
  email: string;
  phone: string;
  address: string;
  city: string;
  state: string;
  zip_code: string;
  country: string;
  fruit_types: string[];
  certification: string[];
  rating: number;
  status: 'active' | 'inactive' | 'pending';
  notes?: string;
  created_date: string;
  last_order_date?: string;
}

interface SupplierCreate {
  name: string;
  type: 'farmer' | 'supplier' | 'distributor';
  contact_person: string;
  email: string;
  phone: string;
  address: string;
  city: string;
  state: string;
  zip_code: string;
  country: string;
  fruit_types: string[];
  certification: string[];
  notes?: string;
}

export default function FarmersSuppliers() {
  const [openDialog, setOpenDialog] = useState(false);
  const [suppliers, setSuppliers] = useState<Supplier[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [editingSupplier, setEditingSupplier] = useState<Supplier | null>(null);

  const [newSupplier, setNewSupplier] = useState<Partial<SupplierCreate>>({
    name: '',
    type: 'farmer',
    contact_person: '',
    email: '',
    phone: '',
    address: '',
    city: '',
    state: '',
    zip_code: '',
    country: 'Australia',
    fruit_types: [],
    certification: [],
    notes: '',
  });

  const fruitTypes = [
    'Lemon', 'Lime', 'Orange', 'Grapefruit', 'Apple', 'Grape', 'Pineapple', 'Mango', 'Mixed Citrus'
  ];

  const certifications = [
    'Organic', 'Fair Trade', 'GAP Certified', 'HACCP', 'ISO 22000', 'Kosher', 'Halal'
  ];

  useEffect(() => {
    fetchSuppliers();
  }, []);

  const fetchSuppliers = async () => {
    try {
      setLoading(true);
      // Mock data for now
      const mockSuppliers: Supplier[] = [
        {
          id: '1',
          name: 'Sunshine Citrus Farms',
          type: 'farmer',
          contact_person: 'John Smith',
          email: 'john@sunshinecitrus.com',
          phone: '(02) 9876 5432',
          address: '123 Citrus Grove Rd',
          city: 'Mildura',
          state: 'VIC',
          zip_code: '3500',
          country: 'Australia',
          fruit_types: ['Lemon', 'Lime', 'Orange'],
          certification: ['Organic', 'GAP Certified'],
          rating: 4.8,
          status: 'active',
          notes: 'Premium citrus supplier with excellent quality',
          created_date: '2024-01-15',
          last_order_date: '2024-04-10'
        },
        {
          id: '2',
          name: 'Golden Apple Orchards',
          type: 'farmer',
          contact_person: 'Sarah Johnson',
          email: 'sarah@goldenapple.com',
          phone: '(03) 8765 4321',
          address: '456 Apple Valley Dr',
          city: 'Hobart',
          state: 'TAS',
          zip_code: '7000',
          country: 'Australia',
          fruit_types: ['Apple', 'Grape'],
          certification: ['Organic', 'Fair Trade'],
          rating: 4.6,
          status: 'active',
          notes: 'Sustainable farming practices',
          created_date: '2024-02-20',
          last_order_date: '2024-04-05'
        },
        {
          id: '3',
          name: 'Tropical Fruit Distributors',
          type: 'distributor',
          contact_person: 'Mike Wilson',
          email: 'mike@tropicalfruit.com',
          phone: '(07) 7654 3210',
          address: '789 Tropical Blvd',
          city: 'Cairns',
          state: 'QLD',
          zip_code: '4870',
          country: 'Australia',
          fruit_types: ['Pineapple', 'Mango', 'Mixed Citrus'],
          certification: ['HACCP', 'ISO 22000'],
          rating: 4.4,
          status: 'active',
          notes: 'Large distributor with international sources',
          created_date: '2024-03-01',
          last_order_date: '2024-04-12'
        }
      ];
      setSuppliers(mockSuppliers);
    } catch (err: any) {
      setError('Failed to fetch suppliers');
      console.error('Error fetching suppliers:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateSupplier = async () => {
    if (newSupplier.name && newSupplier.contact_person && newSupplier.email) {
      try {
        const supplier: Supplier = {
          id: Date.now().toString(),
          name: newSupplier.name!,
          type: newSupplier.type!,
          contact_person: newSupplier.contact_person!,
          email: newSupplier.email!,
          phone: newSupplier.phone!,
          address: newSupplier.address!,
          city: newSupplier.city!,
          state: newSupplier.state!,
          zip_code: newSupplier.zip_code!,
          country: newSupplier.country!,
          fruit_types: newSupplier.fruit_types!,
          certification: newSupplier.certification!,
          rating: 0,
          status: 'pending',
          notes: newSupplier.notes,
          created_date: new Date().toISOString().split('T')[0],
        };
        
        setSuppliers([...suppliers, supplier]);
        setOpenDialog(false);
        resetForm();
      } catch (err: any) {
        setError('Failed to create supplier');
        console.error('Error creating supplier:', err);
      }
    }
  };

  const handleUpdateSupplier = async () => {
    if (editingSupplier && newSupplier.name && newSupplier.contact_person && newSupplier.email) {
      try {
        const updatedSupplier = {
          ...editingSupplier,
          ...newSupplier,
        };
        
        setSuppliers(suppliers.map(s => s.id === editingSupplier.id ? updatedSupplier : s));
        setOpenDialog(false);
        setEditingSupplier(null);
        resetForm();
      } catch (err: any) {
        setError('Failed to update supplier');
        console.error('Error updating supplier:', err);
      }
    }
  };

  const handleDeleteSupplier = async (supplierId: string) => {
    try {
      setSuppliers(suppliers.filter(s => s.id !== supplierId));
    } catch (err: any) {
      setError('Failed to delete supplier');
      console.error('Error deleting supplier:', err);
    }
  };

  const resetForm = () => {
    setNewSupplier({
      name: '',
      type: 'farmer',
      contact_person: '',
      email: '',
      phone: '',
      address: '',
      city: '',
      state: '',
      zip_code: '',
      country: 'Australia',
      fruit_types: [],
      certification: [],
      notes: '',
    });
  };

  const openEditDialog = (supplier: Supplier) => {
    setEditingSupplier(supplier);
    setNewSupplier({
      name: supplier.name,
      type: supplier.type,
      contact_person: supplier.contact_person,
      email: supplier.email,
      phone: supplier.phone,
      address: supplier.address,
      city: supplier.city,
      state: supplier.state,
      zip_code: supplier.zip_code,
      country: supplier.country,
      fruit_types: supplier.fruit_types,
      certification: supplier.certification,
      notes: supplier.notes,
    });
    setOpenDialog(true);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'success';
      case 'inactive':
        return 'error';
      case 'pending':
        return 'warning';
      default:
        return 'default';
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'farmer':
        return <FarmIcon />;
      case 'supplier':
        return <BusinessIcon />;
      case 'distributor':
        return <BusinessIcon />;
      default:
        return <BusinessIcon />;
    }
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">Farmers & Suppliers Management</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => {
            setEditingSupplier(null);
            resetForm();
            setOpenDialog(true);
          }}
        >
          Add Supplier
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {/* Summary Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Suppliers
              </Typography>
              <Typography variant="h4">
                {suppliers.length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Active Suppliers
              </Typography>
              <Typography variant="h4">
                {suppliers.filter(s => s.status === 'active').length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Farmers
              </Typography>
              <Typography variant="h4">
                {suppliers.filter(s => s.type === 'farmer').length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Average Rating
              </Typography>
              <Typography variant="h4">
                {(suppliers.reduce((acc, s) => acc + s.rating, 0) / suppliers.length).toFixed(1)}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Suppliers Table */}
      <Paper sx={{ p: 2 }}>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Supplier</TableCell>
                <TableCell>Type</TableCell>
                <TableCell>Contact</TableCell>
                <TableCell>Location</TableCell>
                <TableCell>Fruit Types</TableCell>
                <TableCell>Certifications</TableCell>
                <TableCell>Rating</TableCell>
                <TableCell>Status</TableCell>
                <TableCell align="center">Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {suppliers.map((supplier) => (
                <TableRow key={supplier.id} hover>
                  <TableCell>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Avatar sx={{ bgcolor: 'primary.main' }}>
                        {getTypeIcon(supplier.type)}
                      </Avatar>
                      <Box>
                        <Typography variant="subtitle2" fontWeight="bold">
                          {supplier.name}
                        </Typography>
                        <Typography variant="caption" color="textSecondary">
                          {supplier.contact_person}
                        </Typography>
                      </Box>
                    </Box>
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={supplier.type}
                      color={supplier.type === 'farmer' ? 'success' : 'primary'}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    <Box>
                      <Typography variant="body2" sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                        <EmailIcon fontSize="small" />
                        {supplier.email}
                      </Typography>
                      <Typography variant="body2" sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                        <PhoneIcon fontSize="small" />
                        {supplier.phone}
                      </Typography>
                    </Box>
                  </TableCell>
                  <TableCell>
                    <Box>
                      <Typography variant="body2">
                        {supplier.city}, {supplier.state}
                      </Typography>
                      <Typography variant="caption" color="textSecondary">
                        {supplier.country}
                      </Typography>
                    </Box>
                  </TableCell>
                  <TableCell>
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                      {supplier.fruit_types.map((fruit, index) => (
                        <Chip
                          key={index}
                          label={fruit}
                          size="small"
                          variant="outlined"
                        />
                      ))}
                    </Box>
                  </TableCell>
                  <TableCell>
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                      {supplier.certification.map((cert, index) => (
                        <Chip
                          key={index}
                          label={cert}
                          size="small"
                          color="secondary"
                        />
                      ))}
                    </Box>
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2" fontWeight="bold">
                      {supplier.rating}/5.0
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={supplier.status}
                      color={getStatusColor(supplier.status) as any}
                      size="small"
                    />
                  </TableCell>
                  <TableCell align="center">
                    <IconButton size="small" onClick={() => openEditDialog(supplier)}>
                      <EditIcon />
                    </IconButton>
                    <IconButton size="small" color="error" onClick={() => handleDeleteSupplier(supplier.id)}>
                      <DeleteIcon />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>

      {/* Add/Edit Supplier Dialog */}
      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>
          {editingSupplier ? 'Edit Supplier' : 'Add New Supplier'}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ mt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Supplier Name"
                  value={newSupplier.name}
                  onChange={(e) => setNewSupplier({ ...newSupplier, name: e.target.value })}
                  required
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <FormControl fullWidth required>
                  <InputLabel>Type</InputLabel>
                  <Select
                    value={newSupplier.type}
                    label="Type"
                    onChange={(e) => setNewSupplier({ ...newSupplier, type: e.target.value as any })}
                  >
                    <MenuItem value="farmer">Farmer</MenuItem>
                    <MenuItem value="supplier">Supplier</MenuItem>
                    <MenuItem value="distributor">Distributor</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Contact Person"
                  value={newSupplier.contact_person}
                  onChange={(e) => setNewSupplier({ ...newSupplier, contact_person: e.target.value })}
                  required
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Email"
                  type="email"
                  value={newSupplier.email}
                  onChange={(e) => setNewSupplier({ ...newSupplier, email: e.target.value })}
                  required
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Phone"
                  value={newSupplier.phone}
                  onChange={(e) => setNewSupplier({ ...newSupplier, phone: e.target.value })}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Country"
                  value={newSupplier.country}
                  onChange={(e) => setNewSupplier({ ...newSupplier, country: e.target.value })}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Address"
                  value={newSupplier.address}
                  onChange={(e) => setNewSupplier({ ...newSupplier, address: e.target.value })}
                />
              </Grid>
              <Grid item xs={12} md={4}>
                <TextField
                  fullWidth
                  label="City"
                  value={newSupplier.city}
                  onChange={(e) => setNewSupplier({ ...newSupplier, city: e.target.value })}
                />
              </Grid>
              <Grid item xs={12} md={4}>
                <TextField
                  fullWidth
                  label="State"
                  value={newSupplier.state}
                  onChange={(e) => setNewSupplier({ ...newSupplier, state: e.target.value })}
                />
              </Grid>
              <Grid item xs={12} md={4}>
                <TextField
                  fullWidth
                                  label="Postal Code"
                value={newSupplier.zip_code}
                onChange={(e) => setNewSupplier({ ...newSupplier, zip_code: e.target.value })}
                />
              </Grid>
              <Grid item xs={12}>
                <FormControl fullWidth>
                  <InputLabel>Fruit Types</InputLabel>
                  <Select
                    multiple
                    value={newSupplier.fruit_types}
                    label="Fruit Types"
                    onChange={(e) => setNewSupplier({ ...newSupplier, fruit_types: e.target.value as string[] })}
                  >
                    {fruitTypes.map((fruit) => (
                      <MenuItem key={fruit} value={fruit}>{fruit}</MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12}>
                <FormControl fullWidth>
                  <InputLabel>Certifications</InputLabel>
                  <Select
                    multiple
                    value={newSupplier.certification}
                    label="Certifications"
                    onChange={(e) => setNewSupplier({ ...newSupplier, certification: e.target.value as string[] })}
                  >
                    {certifications.map((cert) => (
                      <MenuItem key={cert} value={cert}>{cert}</MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Notes"
                  multiline
                  rows={3}
                  value={newSupplier.notes}
                  onChange={(e) => setNewSupplier({ ...newSupplier, notes: e.target.value })}
                />
              </Grid>
            </Grid>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
          <Button 
            onClick={editingSupplier ? handleUpdateSupplier : handleCreateSupplier} 
            variant="contained"
          >
            {editingSupplier ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
