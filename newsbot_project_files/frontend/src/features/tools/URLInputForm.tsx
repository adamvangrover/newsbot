import React, { useState } from 'react';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import CircularProgress from '@mui/material/CircularProgress';

interface URLInputFormProps {
  onSubmit: (url: string) => void;
  isLoading: boolean;
}

const URLInputForm: React.FC<URLInputFormProps> = ({ onSubmit, isLoading }) => {
  const [url, setUrl] = useState<string>('');
  const [error, setError] = useState<string>('');

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!url.trim()) {
      setError('URL cannot be empty.');
      return;
    }
    // Basic URL validation (browser also does some via type="url")
    try {
      new URL(url); // Check if it's a valid URL structure
      setError('');
      onSubmit(url);
    } catch (_) {
      setError('Please enter a valid URL (e.g., http://example.com).');
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 3 }}>
      <TextField
        label="Enter URL to Scrape and Analyze"
        variant="outlined"
        fullWidth
        type="url"
        value={url}
        onChange={(e) => {
            setUrl(e.target.value);
            if (error) setError(''); // Clear error when user types
        }}
        error={!!error}
        helperText={error}
        disabled={isLoading}
        required
      />
      <Button
        type="submit"
        variant="contained"
        color="primary"
        disabled={isLoading}
        sx={{ minWidth: 120, height: 56 }} // Match TextField height
      >
        {isLoading ? <CircularProgress size={24} color="inherit" /> : 'Analyze'}
      </Button>
    </Box>
  );
};

export default URLInputForm;
