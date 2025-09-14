import React from 'react';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';

const PortfolioPage: React.FC = () => {
  return (
    <Container maxWidth="lg" sx={{ mt: 2, mb: 3 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Portfolio Management
      </Typography>
      {/* Portfolio management UI will be built here */}
    </Container>
  );
};

export default PortfolioPage;
