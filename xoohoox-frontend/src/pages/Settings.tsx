import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Switch,
  FormControlLabel,
  TextField,
  Button,
  Stack,
  Divider,
  Alert,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  ListItemSecondaryAction,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Chip,
} from '@mui/material';
import {
  Notifications as NotificationsIcon,
  Security as SecurityIcon,
  Settings as SettingsIcon,
  Language as LanguageIcon,
  Palette as PaletteIcon,
  Save as SaveIcon,
  Refresh as RefreshIcon,
  Email as EmailIcon,
  Phone as PhoneIcon,
} from '@mui/icons-material';

interface SettingsData {
  notifications: {
    email: boolean;
    sms: boolean;
    push: boolean;
    qualityAlerts: boolean;
    productionAlerts: boolean;
    maintenanceReminders: boolean;
  };
  preferences: {
    language: string;
    theme: string;
    timezone: string;
    dateFormat: string;
    temperatureUnit: string;
  };
  system: {
    autoBackup: boolean;
    dataRetention: number;
    sessionTimeout: number;
    maxFileSize: number;
  };
}

const Settings = () => {
  const [data, setData] = useState<SettingsData>({
    notifications: {
      email: true,
      sms: false,
      push: true,
      qualityAlerts: true,
      productionAlerts: true,
      maintenanceReminders: false,
    },
    preferences: {
      language: 'en',
      theme: 'light',
      timezone: 'UTC',
      dateFormat: 'MM/DD/YYYY',
      temperatureUnit: 'celsius',
    },
    system: {
      autoBackup: true,
      dataRetention: 365,
      sessionTimeout: 30,
      maxFileSize: 10,
    },
  });

  const [saved, setSaved] = useState(false);

  const handleNotificationChange = (key: keyof SettingsData['notifications']) => {
    setData(prev => ({
      ...prev,
      notifications: {
        ...prev.notifications,
        [key]: !prev.notifications[key],
      },
    }));
  };

  const handlePreferenceChange = (key: keyof SettingsData['preferences'], value: string) => {
    setData(prev => ({
      ...prev,
      preferences: {
        ...prev.preferences,
        [key]: value,
      },
    }));
  };

  const handleSystemChange = (key: keyof SettingsData['system'], value: boolean | number) => {
    setData(prev => ({
      ...prev,
      system: {
        ...prev.system,
        [key]: value,
      },
    }));
  };

  const handleSave = () => {
    // Mock save functionality
    console.log('Saving settings:', data);
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  const handleReset = () => {
    // Mock reset functionality
    alert('Settings reset to defaults');
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Settings
      </Typography>

      {saved && (
        <Alert severity="success" sx={{ mb: 3 }}>
          Settings saved successfully!
        </Alert>
      )}

      {/* Notification Settings */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <NotificationsIcon sx={{ mr: 1 }} />
          <Typography variant="h6">Notification Settings</Typography>
        </Box>
        
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3 }}>
          <Box sx={{ flex: '1 1 300px', minWidth: 300 }}>
            <Typography variant="subtitle1" gutterBottom>
              Notification Channels
            </Typography>
            <Stack spacing={2}>
              <FormControlLabel
                control={
                  <Switch
                    checked={data.notifications.email}
                    onChange={() => handleNotificationChange('email')}
                  />
                }
                label="Email Notifications"
              />
              <FormControlLabel
                control={
                  <Switch
                    checked={data.notifications.sms}
                    onChange={() => handleNotificationChange('sms')}
                  />
                }
                label="SMS Notifications"
              />
              <FormControlLabel
                control={
                  <Switch
                    checked={data.notifications.push}
                    onChange={() => handleNotificationChange('push')}
                  />
                }
                label="Push Notifications"
              />
            </Stack>
          </Box>
          
          <Box sx={{ flex: '1 1 300px', minWidth: 300 }}>
            <Typography variant="subtitle1" gutterBottom>
              Alert Types
            </Typography>
            <Stack spacing={2}>
              <FormControlLabel
                control={
                  <Switch
                    checked={data.notifications.qualityAlerts}
                    onChange={() => handleNotificationChange('qualityAlerts')}
                  />
                }
                label="Quality Control Alerts"
              />
              <FormControlLabel
                control={
                  <Switch
                    checked={data.notifications.productionAlerts}
                    onChange={() => handleNotificationChange('productionAlerts')}
                  />
                }
                label="Production Alerts"
              />
              <FormControlLabel
                control={
                  <Switch
                    checked={data.notifications.maintenanceReminders}
                    onChange={() => handleNotificationChange('maintenanceReminders')}
                  />
                }
                label="Maintenance Reminders"
              />
            </Stack>
          </Box>
        </Box>
      </Paper>

      {/* User Preferences */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <PaletteIcon sx={{ mr: 1 }} />
          <Typography variant="h6">User Preferences</Typography>
        </Box>
        
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3 }}>
          <FormControl sx={{ minWidth: 200 }}>
            <InputLabel>Language</InputLabel>
            <Select
              value={data.preferences.language}
              label="Language"
              onChange={(e) => handlePreferenceChange('language', e.target.value)}
            >
              <MenuItem value="en">English</MenuItem>
              <MenuItem value="es">Spanish</MenuItem>
              <MenuItem value="fr">French</MenuItem>
              <MenuItem value="de">German</MenuItem>
            </Select>
          </FormControl>

          <FormControl sx={{ minWidth: 200 }}>
            <InputLabel>Theme</InputLabel>
            <Select
              value={data.preferences.theme}
              label="Theme"
              onChange={(e) => handlePreferenceChange('theme', e.target.value)}
            >
              <MenuItem value="light">Light</MenuItem>
              <MenuItem value="dark">Dark</MenuItem>
              <MenuItem value="auto">Auto</MenuItem>
            </Select>
          </FormControl>

          <FormControl sx={{ minWidth: 200 }}>
            <InputLabel>Timezone</InputLabel>
            <Select
              value={data.preferences.timezone}
              label="Timezone"
              onChange={(e) => handlePreferenceChange('timezone', e.target.value)}
            >
              <MenuItem value="UTC">UTC</MenuItem>
              <MenuItem value="EST">Eastern Time</MenuItem>
              <MenuItem value="PST">Pacific Time</MenuItem>
              <MenuItem value="GMT">GMT</MenuItem>
            </Select>
          </FormControl>

          <FormControl sx={{ minWidth: 200 }}>
            <InputLabel>Date Format</InputLabel>
            <Select
              value={data.preferences.dateFormat}
              label="Date Format"
              onChange={(e) => handlePreferenceChange('dateFormat', e.target.value)}
            >
              <MenuItem value="MM/DD/YYYY">MM/DD/YYYY</MenuItem>
              <MenuItem value="DD/MM/YYYY">DD/MM/YYYY</MenuItem>
              <MenuItem value="YYYY-MM-DD">YYYY-MM-DD</MenuItem>
            </Select>
          </FormControl>

          <FormControl sx={{ minWidth: 200 }}>
            <InputLabel>Temperature Unit</InputLabel>
            <Select
              value={data.preferences.temperatureUnit}
              label="Temperature Unit"
              onChange={(e) => handlePreferenceChange('temperatureUnit', e.target.value)}
            >
              <MenuItem value="celsius">Celsius</MenuItem>
              <MenuItem value="fahrenheit">Fahrenheit</MenuItem>
            </Select>
          </FormControl>
        </Box>
      </Paper>

      {/* System Settings */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <SettingsIcon sx={{ mr: 1 }} />
          <Typography variant="h6">System Settings</Typography>
        </Box>
        
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3 }}>
          <Box sx={{ flex: '1 1 300px', minWidth: 300 }}>
            <FormControlLabel
              control={
                <Switch
                  checked={data.system.autoBackup}
                  onChange={() => handleSystemChange('autoBackup', !data.system.autoBackup)}
                />
              }
              label="Automatic Backup"
            />
            <Typography variant="caption" color="text.secondary" display="block">
              Automatically backup data daily
            </Typography>
          </Box>
          
          <Box sx={{ flex: '1 1 300px', minWidth: 300 }}>
            <TextField
              label="Data Retention (days)"
              type="number"
              value={data.system.dataRetention}
              onChange={(e) => handleSystemChange('dataRetention', parseInt(e.target.value))}
              sx={{ width: 200 }}
            />
          </Box>
          
          <Box sx={{ flex: '1 1 300px', minWidth: 300 }}>
            <TextField
              label="Session Timeout (minutes)"
              type="number"
              value={data.system.sessionTimeout}
              onChange={(e) => handleSystemChange('sessionTimeout', parseInt(e.target.value))}
              sx={{ width: 200 }}
            />
          </Box>
          
          <Box sx={{ flex: '1 1 300px', minWidth: 300 }}>
            <TextField
              label="Max File Size (MB)"
              type="number"
              value={data.system.maxFileSize}
              onChange={(e) => handleSystemChange('maxFileSize', parseInt(e.target.value))}
              sx={{ width: 200 }}
            />
          </Box>
        </Box>
      </Paper>

      {/* Security Settings */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <SecurityIcon sx={{ mr: 1 }} />
          <Typography variant="h6">Security Settings</Typography>
        </Box>
        
        <Stack spacing={2}>
          <Button variant="outlined" startIcon={<SecurityIcon />}>
            Change Password
          </Button>
          <Button variant="outlined" startIcon={<SecurityIcon />}>
            Enable Two-Factor Authentication
          </Button>
          <Button variant="outlined" startIcon={<SecurityIcon />}>
            View Login History
          </Button>
        </Stack>
      </Paper>

      {/* Action Buttons */}
      <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
        <Button
          variant="outlined"
          startIcon={<RefreshIcon />}
          onClick={handleReset}
        >
          Reset to Defaults
        </Button>
        <Button
          variant="contained"
          startIcon={<SaveIcon />}
          onClick={handleSave}
        >
          Save Settings
        </Button>
      </Box>
    </Box>
  );
};

export default Settings; 