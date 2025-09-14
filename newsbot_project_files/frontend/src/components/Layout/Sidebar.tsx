import React from 'react';
import { Link as RouterLink, useLocation } from 'react-router-dom';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Divider from '@mui/material/Divider';
import Toolbar from '@mui/material/Toolbar'; // To offset content below AppBar
import BusinessIcon from '@mui/icons-material/Business'; // Company Analysis
import LanguageIcon from '@mui/icons-material/Language'; // Market Outlook
import TravelExploreIcon from '@mui/icons-material/TravelExplore'; // Web Scrape/Tools
import AssessmentIcon from '@mui/icons-material/Assessment'; // For Portfolios

const drawerWidth = 240;

interface SidebarItem {
  text: string;
  path: string;
  icon: React.ReactElement;
}

const sidebarItems: SidebarItem[] = [
  { text: 'Company Analysis', path: '/', icon: <BusinessIcon /> },
  { text: 'Market Outlook', path: '/market', icon: <LanguageIcon /> },
  { text: 'Portfolios', path: '/portfolios', icon: <AssessmentIcon /> },
  { text: 'Web Scraper', path: '/tools', icon: <TravelExploreIcon /> },
];

interface SidebarProps {
  mobileOpen: boolean;
  handleDrawerToggle: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ mobileOpen, handleDrawerToggle }) => {
  const location = useLocation();

  const drawerContent = (
    <div>
      <Toolbar /> {/* Necessary to ensure content is below the AppBar */}
      <Divider />
      <List>
        {sidebarItems.map((item) => (
          <ListItem key={item.text} disablePadding>
            <ListItemButton
              component={RouterLink}
              to={item.path}
              selected={location.pathname === item.path}
              onClick={mobileOpen ? handleDrawerToggle : undefined} // Close mobile drawer on item click
            >
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
      {/* Optional: Add more sections or a divider here */}
    </div>
  );

  return (
    <Box
      component="nav"
      sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}
      aria-label="mailbox folders"
    >
      {/* Mobile Drawer */}
      <Drawer
        variant="temporary"
        open={mobileOpen}
        onClose={handleDrawerToggle}
        ModalProps={{
          keepMounted: true, // Better open performance on mobile.
        }}
        sx={{
          display: { xs: 'block', sm: 'none' },
          '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
        }}
      >
        {drawerContent}
      </Drawer>
      {/* Desktop Drawer */}
      <Drawer
        variant="permanent"
        sx={{
          display: { xs: 'none', sm: 'block' },
          '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
        }}
        open // Permanent drawer is always open on desktop
      >
        {drawerContent}
      </Drawer>
    </Box>
  );
};

export default Sidebar;
