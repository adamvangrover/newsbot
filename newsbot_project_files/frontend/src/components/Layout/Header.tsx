import React from 'react';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import SearchIcon from '@mui/icons-material/Search'; // Example Icon
import { Box } from '@mui/material';

interface HeaderProps {
  onSearchSubmit?: (ticker: string) => void; // Optional: if search is in header
}

const Header: React.FC<HeaderProps> = ({ onSearchSubmit }) => {
  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          NewsBot
        </Typography>
        {/* Basic Search Icon - Actual search bar can be a separate component or integrated here */}
        {/* <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <SearchIcon />
          <Typography variant="body1" sx={{ ml: 1 }}>Search</Typography>
        </Box> */}
      </Toolbar>
    </AppBar>
  );
};

export default Header;
