import React, { ReactNode } from 'react';
import Container from '@mui/material/Container';
import Box from '@mui/material/Box';

interface MainContentProps {
  children: ReactNode;
}

const MainContent: React.FC<MainContentProps> = ({ children }) => {
  return (
    <Container maxWidth="lg"> {/* Adjust maxWidth as needed */}
      <Box sx={{ my: 4 }}> {/* my: margin top and bottom */}
        {children}
      </Box>
    </Container>
  );
};

export default MainContent;
