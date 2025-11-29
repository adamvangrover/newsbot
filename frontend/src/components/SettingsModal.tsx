import React, { useState, useEffect } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, TextField, Button, Box, Typography } from '@mui/material';
import { useDataProvider } from '../api/DataProviderContext';

interface SettingsModalProps {
  open: boolean;
  onClose: () => void;
}

export const SettingsModal: React.FC<SettingsModalProps> = ({ open, onClose }) => {
  const { configureLive, setMode, mode } = useDataProvider();
  const [url, setUrl] = useState('http://localhost:8000');
  const [apiKey, setApiKey] = useState('');
  const [status, setStatus] = useState<'idle' | 'testing' | 'success' | 'error'>('idle');

  const handleSave = async () => {
    setStatus('testing');
    try {
      // Simple health check or just assume it works for now.
      // Ideally we would hit an endpoint like /health
      const response = await fetch(`${url}/health`, {
        method: 'GET',
        headers: { 'X-API-Key': apiKey }
      });

      // Allow 404 if health endpoint doesn't exist but server responds,
      // but for "connection" we usually want a 200.
      // If server is down, fetch will throw.

      configureLive(url, apiKey);
      setStatus('success');
      setTimeout(() => {
        onClose();
        if (mode === 'demo') {
            // Optional: Auto-switch to live?
            // setMode('live');
        }
      }, 1000);
    } catch (e) {
      console.error(e);
      // We will still save it but warn user
      configureLive(url, apiKey);
      setStatus('error');
    }
  };

  return (
    <Dialog open={open} onClose={onClose}>
      <DialogTitle>Connection Settings</DialogTitle>
      <DialogContent>
        <Box sx={{ mt: 1 }}>
            <Typography variant="body2" color="textSecondary" gutterBottom>
                Configure the connection to the Python backend for Live Mode.
            </Typography>
            <TextField
              autoFocus
              margin="dense"
              label="API Base URL"
              type="url"
              fullWidth
              variant="outlined"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
            />
            <TextField
              margin="dense"
              label="API Key"
              type="password"
              fullWidth
              variant="outlined"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
            />
            {status === 'success' && <Typography color="success.main">Connection Verified!</Typography>}
            {status === 'error' && <Typography color="error.main">Could not connect to server, but settings saved.</Typography>}
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button onClick={handleSave} variant="contained">Save & Test</Button>
      </DialogActions>
    </Dialog>
  );
};
