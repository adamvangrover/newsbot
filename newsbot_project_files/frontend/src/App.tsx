import React, { useState } from 'react';
import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Box from '@mui/material/Box';
import CssBaseline from '@mui/material/CssBaseline'; // Handles base styling and theme resets
import Toolbar from '@mui/material/Toolbar'; // For spacing content below AppBar

import Header from './components/Layout/Header';
import Sidebar from './components/Layout/Sidebar';
import MainContent from './components/Layout/MainContent'; // This might need adjustment or removal if pages handle their own containers

// Page Components
import CompanyAnalysisPage from './features/company/CompanyAnalysisPage';
import MarketOutlookPage from './features/market/MarketOutlookPage';
import WebScrapePage from './features/tools/WebScrapePage';
import PortfolioPage from './features/portfolio/PortfolioPage'; // Import the new page

const drawerWidth = 240; // Consistent with Sidebar and Header

function App() {
  const [mobileOpen, setMobileOpen] = useState(false);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  return (
    <Router>
      <Box sx={{ display: 'flex' }}>
        <CssBaseline />
        <Header handleDrawerToggle={handleDrawerToggle} />
        <Sidebar mobileOpen={mobileOpen} handleDrawerToggle={handleDrawerToggle} />

        {/* Main content area */}
        <Box
          component="main"
          sx={{
            flexGrow: 1,
            p: 3,
            width: { sm: `calc(100% - ${drawerWidth}px)` },
            overflowX: 'hidden' // Prevent horizontal scroll
          }}
        >
          <Toolbar /> {/* Necessary spacer for content under fixed AppBar */}
          {/* MainContent might not be needed if each page uses its own Container */}
          {/* <MainContent> */}
            <Routes>
              <Route path="/" element={<CompanyAnalysisPage />} />
              <Route path="/market" element={<MarketOutlookPage />} />
              <Route path="/tools" element={<WebScrapePage />} />
              <Route path="/portfolios" element={<PortfolioPage />} />
              {/* Add a 404 Not Found route later if desired */}
              {/* <Route path="*" element={<NotFoundPage />} /> */}
            </Routes>
          {/* </MainContent> */}
        </Box>
      </Box>
    </Router>
  );
}

export default App;
