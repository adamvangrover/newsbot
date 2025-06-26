import React from 'react';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
// import SearchIcon from '@mui/icons-material/Search'; // Example Icon
// import { Box } from '@mui/material';

const drawerWidth = 240; // Should be consistent with Sidebar

interface HeaderProps {
  // onSearchSubmit?: (ticker: string) => void; // Optional: if search is in header
  handleDrawerToggle?: () => void; // For mobile sidebar
}

const Header: React.FC<HeaderProps> = ({ handleDrawerToggle }) => {
  return (
    <AppBar
      position="fixed" // Changed to fixed to work with persistent drawer
      sx={{
        width: { sm: `calc(100% - ${drawerWidth}px)` }, // Adjust width for desktop drawer
        ml: { sm: `${drawerWidth}px` }, // Margin left for desktop drawer
      }}
    >
      <Toolbar>
        <IconButton
          color="inherit"
          aria-label="open drawer"
          edge="start"
          onClick={handleDrawerToggle}
          sx={{ mr: 2, display: { sm: 'none' } }} // Only display on mobile (sm and up will hide)
        >
          <MenuIcon />
        </IconButton>
        <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
          NewsBot Dashboard
        </Typography>
        {/* Search functionality can be added here if needed */}
      </Toolbar>
    </AppBar>
  );
};

export default Header;
