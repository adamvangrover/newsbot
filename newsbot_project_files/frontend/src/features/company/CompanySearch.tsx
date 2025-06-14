import React, { useState } from 'react';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import SearchIcon from '@mui/icons-material/Search';

interface CompanySearchProps {
  onSearch: (ticker: string) => void;
  isLoading?: boolean;
}

const CompanySearch: React.FC<CompanySearchProps> = ({ onSearch, isLoading }) => {
  const [ticker, setTicker] = useState<string>('');

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    if (ticker.trim()) {
      onSearch(ticker.trim().toUpperCase());
    }
  };

  return (
    <Box
      component="form"
      onSubmit={handleSubmit}
      sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 3 }}
    >
      <TextField
        label="Company Ticker (e.g., AAPL)"
        variant="outlined"
        value={ticker}
        onChange={(e) => setTicker(e.target.value)}
        disabled={isLoading}
        sx={{ flexGrow: 1 }}
      />
      <Button
        type="submit"
        variant="contained"
        startIcon={<SearchIcon />}
        disabled={isLoading || !ticker.trim()}
      >
        {isLoading ? 'Searching...' : 'Search'}
      </Button>
    </Box>
  );
};

export default CompanySearch;
