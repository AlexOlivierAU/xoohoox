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
  Avatar,
  Switch,
  FormControlLabel,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Person as PersonIcon,
  AdminPanelSettings as AdminIcon,
  Security as SecurityIcon,
} from '@mui/icons-material';

interface User {
  id: string;
  username: string;
  email: string;
  full_name: string;
  role: 'admin' | 'manager' | 'operator' | 'viewer';
  status: 'active' | 'inactive';
  last_login?: string;
  created_at: string;
  permissions: string[];
  avatar?: string;
}

const UserManagement = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [openDialog, setOpenDialog] = useState(false);
  const [editingUser, setEditingUser] = useState<User | null>(null);

  const [newUser, setNewUser] = useState<Partial<User>>({
    username: '',
    email: '',
    full_name: '',
    role: 'operator',
    status: 'active',
    permissions: [],
  });

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      setLoading(true);
      // Mock data for now - replace with actual API call
      const mockUsers: User[] = [
        {
          id: '1',
          username: 'admin',
          email: 'admin@xoohoox.com',
          full_name: 'System Administrator',
          role: 'admin',
          status: 'active',
          last_login: '2024-01-15 10:30:00',
          created_at: '2024-01-01',
          permissions: ['all'],
        },
        {
          id: '2',
          username: 'manager1',
          email: 'manager@xoohoox.com',
          full_name: 'Production Manager',
          role: 'manager',
          status: 'active',
          last_login: '2024-01-14 15:45:00',
          created_at: '2024-01-05',
          permissions: ['production', 'quality', 'reports'],
        },
        {
          id: '3',
          username: 'operator1',
          email: 'operator@xoohoox.com',
          full_name: 'Production Operator',
          role: 'operator',
          status: 'active',
          last_login: '2024-01-15 08:15:00',
          created_at: '2024-01-10',
          permissions: ['production', 'quality'],
        },
        {
          id: '4',
          username: 'viewer1',
          email: 'viewer@xoohoox.com',
          full_name: 'Quality Inspector',
          role: 'viewer',
          status: 'inactive',
          last_login: '2024-01-12 14:20:00',
          created_at: '2024-01-08',
          permissions: ['quality', 'reports'],
        },
      ];
      setUsers(mockUsers);
    } catch (err: any) {
      setError('Failed to fetch users');
      console.error('Error fetching users:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSaveUser = async () => {
    try {
      if (editingUser) {
        // Update existing user
        const updatedUsers = users.map(user =>
          user.id === editingUser.id ? { ...editingUser, ...newUser } : user
        );
        setUsers(updatedUsers);
      } else {
        // Add new user
        const newUserItem: User = {
          ...newUser as User,
          id: Date.now().toString(),
          created_at: new Date().toISOString().split('T')[0],
        };
        setUsers([...users, newUserItem]);
      }
      setOpenDialog(false);
      setEditingUser(null);
      setNewUser({
        username: '',
        email: '',
        full_name: '',
        role: 'operator',
        status: 'active',
        permissions: [],
      });
    } catch (err: any) {
      setError('Failed to save user');
      console.error('Error saving user:', err);
    }
  };

  const handleEditUser = (user: User) => {
    setEditingUser(user);
    setNewUser(user);
    setOpenDialog(true);
  };

  const handleDeleteUser = (userId: string) => {
    if (window.confirm('Are you sure you want to delete this user?')) {
      setUsers(users.filter(user => user.id !== userId));
    }
  };

  const handleToggleStatus = (userId: string) => {
    setUsers(users.map(user =>
      user.id === userId
        ? { ...user, status: user.status === 'active' ? 'inactive' : 'active' }
        : user
    ));
  };

  const getRoleColor = (role: string) => {
    switch (role) {
      case 'admin': return 'error';
      case 'manager': return 'warning';
      case 'operator': return 'primary';
      case 'viewer': return 'default';
      default: return 'default';
    }
  };

  const getRoleIcon = (role: string) => {
    switch (role) {
      case 'admin': return <AdminIcon />;
      case 'manager': return <SecurityIcon />;
      case 'operator': return <PersonIcon />;
      case 'viewer': return <PersonIcon />;
      default: return <PersonIcon />;
    }
  };

  const availablePermissions = [
    'production',
    'quality',
    'inventory',
    'equipment',
    'reports',
    'analytics',
    'settings',
    'users',
  ];

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
        <Typography variant="h4">User Management</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setOpenDialog(true)}
        >
          Add User
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>
      )}

      {/* User Summary */}
      <Box sx={{ display: 'flex', gap: 3, mb: 4 }}>
        <Paper sx={{ p: 3, textAlign: 'center', flex: 1 }}>
          <Typography variant="h6" gutterBottom>Total Users</Typography>
          <Typography variant="h3" color="primary">{users.length}</Typography>
        </Paper>
        <Paper sx={{ p: 3, textAlign: 'center', flex: 1 }}>
          <Typography variant="h6" gutterBottom>Active Users</Typography>
          <Typography variant="h3" color="success.main">
            {users.filter(user => user.status === 'active').length}
          </Typography>
        </Paper>
        <Paper sx={{ p: 3, textAlign: 'center', flex: 1 }}>
          <Typography variant="h6" gutterBottom>Admins</Typography>
          <Typography variant="h3" color="error.main">
            {users.filter(user => user.role === 'admin').length}
          </Typography>
        </Paper>
        <Paper sx={{ p: 3, textAlign: 'center', flex: 1 }}>
          <Typography variant="h6" gutterBottom>Managers</Typography>
          <Typography variant="h3" color="warning.main">
            {users.filter(user => user.role === 'manager').length}
          </Typography>
        </Paper>
      </Box>

      {/* Users Table */}
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>User</TableCell>
              <TableCell>Role</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Permissions</TableCell>
              <TableCell>Last Login</TableCell>
              <TableCell>Created</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {users.map((user) => (
              <TableRow key={user.id}>
                <TableCell>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                    <Avatar sx={{ width: 32, height: 32 }}>
                      {user.avatar ? (
                        <img src={user.avatar} alt={user.full_name} />
                      ) : (
                        getRoleIcon(user.role)
                      )}
                    </Avatar>
                    <Box>
                      <Typography variant="subtitle2" fontWeight="bold">
                        {user.full_name}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        {user.email}
                      </Typography>
                    </Box>
                  </Box>
                </TableCell>
                <TableCell>
                  <Chip
                    icon={getRoleIcon(user.role)}
                    label={user.role}
                    color={getRoleColor(user.role)}
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  <Chip
                    label={user.status}
                    color={user.status === 'active' ? 'success' : 'default'}
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                    {user.permissions.map((permission) => (
                      <Chip
                        key={permission}
                        label={permission}
                        size="small"
                        variant="outlined"
                      />
                    ))}
                  </Box>
                </TableCell>
                <TableCell>
                  {user.last_login ? (
                    <Typography variant="body2">
                      {new Date(user.last_login).toLocaleDateString()}
                    </Typography>
                  ) : (
                    <Typography variant="body2" color="text.secondary">
                      Never
                    </Typography>
                  )}
                </TableCell>
                <TableCell>
                  <Typography variant="body2">
                    {new Date(user.created_at).toLocaleDateString()}
                  </Typography>
                </TableCell>
                <TableCell>
                  <Box sx={{ display: 'flex', gap: 1 }}>
                    <Tooltip title="Edit">
                      <IconButton size="small" onClick={() => handleEditUser(user)}>
                        <EditIcon />
                      </IconButton>
                    </Tooltip>
                    <Tooltip title="Toggle Status">
                      <Switch
                        size="small"
                        checked={user.status === 'active'}
                        onChange={() => handleToggleStatus(user.id)}
                      />
                    </Tooltip>
                    <Tooltip title="Delete">
                      <IconButton 
                        size="small" 
                        color="error" 
                        onClick={() => handleDeleteUser(user.id)}
                        disabled={user.role === 'admin'}
                      >
                        <DeleteIcon />
                      </IconButton>
                    </Tooltip>
                  </Box>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Add/Edit Dialog */}
      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>
          {editingUser ? 'Edit User' : 'Add New User'}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ mt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
            <TextField
              fullWidth
              label="Username"
              value={newUser.username}
              onChange={(e) => setNewUser({ ...newUser, username: e.target.value })}
            />
            <TextField
              fullWidth
              label="Email"
              type="email"
              value={newUser.email}
              onChange={(e) => setNewUser({ ...newUser, email: e.target.value })}
            />
            <TextField
              fullWidth
              label="Full Name"
              value={newUser.full_name}
              onChange={(e) => setNewUser({ ...newUser, full_name: e.target.value })}
            />
            <FormControl fullWidth>
              <InputLabel>Role</InputLabel>
              <Select
                value={newUser.role}
                label="Role"
                onChange={(e) => setNewUser({ ...newUser, role: e.target.value as User['role'] })}
              >
                <MenuItem value="admin">Admin</MenuItem>
                <MenuItem value="manager">Manager</MenuItem>
                <MenuItem value="operator">Operator</MenuItem>
                <MenuItem value="viewer">Viewer</MenuItem>
              </Select>
            </FormControl>
            <FormControl fullWidth>
              <InputLabel>Status</InputLabel>
              <Select
                value={newUser.status}
                label="Status"
                onChange={(e) => setNewUser({ ...newUser, status: e.target.value as User['status'] })}
              >
                <MenuItem value="active">Active</MenuItem>
                <MenuItem value="inactive">Inactive</MenuItem>
              </Select>
            </FormControl>
            <FormControl fullWidth>
              <InputLabel>Permissions</InputLabel>
              <Select
                multiple
                value={newUser.permissions || []}
                label="Permissions"
                onChange={(e) => setNewUser({ 
                  ...newUser, 
                  permissions: typeof e.target.value === 'string' ? e.target.value.split(',') : e.target.value 
                })}
              >
                {availablePermissions.map((permission) => (
                  <MenuItem key={permission} value={permission}>
                    {permission}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
          <Button onClick={handleSaveUser} variant="contained">
            {editingUser ? 'Update' : 'Add'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default UserManagement; 