import React, { useState } from 'react';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import SearchIcon from '@mui/icons-material/Search';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';


interface CompanySearchProps {
  onSearch: (ticker: string, days: number) => void; // Updated to include days
  isLoading?: boolean;
  initialDays?: number;
}

const CompanySearch: React.FC<CompanySearchProps> = ({ onSearch, isLoading, initialDays = 7 }) => {
  const [ticker, setTicker] = useState<string>('');
  const [days, setDays] = useState<number>(initialDays);

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    if (ticker.trim()) {
      onSearch(ticker.trim().toUpperCase(), days);
    }
  };

  const handleDaysChange = (event: SelectChangeEvent<number>) => {
    setDays(event.target.value as number);
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
      <FormControl sx={{ minWidth: 120 }} size="small">
        <InputLabel id="news-days-select-label">News Days</InputLabel>
        <Select
          labelId="news-days-select-label"
          id="news-days-select"
          value={days}
          label="News Days"
          onChange={handleDaysChange}
          disabled={isLoading}
          size="medium" // Match TextField height a bit better
        >
          <MenuItem value={3}>Last 3 Days</MenuItem>
          <MenuItem value={7}>Last 7 Days</MenuItem>
          <MenuItem value={14}>Last 14 Days</MenuItem>
          <MenuItem value={30}>Last 30 Days</MenuItem>
        </Select>
      </FormControl>
      <Button
        type="submit"
        variant="contained"
        startIcon={<SearchIcon />}
        disabled={isLoading || !ticker.trim()}
        sx={{ height: 56 }} // Match TextField height for consistency
      >
        {isLoading ? 'Searching...' : 'Search'}
      </Button>
    </Box>
  );
};

export default CompanySearch;
