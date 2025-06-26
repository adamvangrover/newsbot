import React, { useState } from 'react';
import CompanySearch from './CompanySearch';
import CompanyProfileDisplay from './CompanyProfileDisplay';
import StockPriceChart from './StockPriceChart';
import NewsList from './NewsList';
import { useCompanyData } from '../../hooks/useCompanyData';
import Typography from '@mui/material/Typography';
import CircularProgress from '@mui/material/CircularProgress';
import Alert from '@mui/material/Alert';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container'; // Added for consistent padding

const CompanyAnalysisPage: React.FC = () => {
  const [currentTicker, setCurrentTicker] = useState<string>('');
  const [newsDays, setNewsDays] = useState<number>(7); // Default to 7 days of news

  const { data: companyData, error, isLoading, isFetching, isError } = useCompanyData(currentTicker, newsDays);

  const handleSearch = (ticker: string, days?: number) => {
    setCurrentTicker(ticker);
    if (days) {
      setNewsDays(days);
    } else {
      setNewsDays(7); // Reset to default if not provided
    }
  };

  return (
    // Container can be part of MainContent in App.tsx or here for page-specific padding
    <Container maxWidth="lg" sx={{ mt: 2, mb: 3 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Company Analysis
      </Typography>
      <CompanySearch onSearch={handleSearch} isLoading={isLoading || isFetching} initialDays={newsDays} />

      {(isLoading || isFetching) && (
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', my: 3, flexDirection: 'column' }}>
          <CircularProgress />
          <Typography sx={{mt:1}}>Loading data for {currentTicker}...</Typography>
        </Box>
      )}

      {isError && error && (
        <Alert severity="error" sx={{ my: 2 }}>
          Error fetching data: {error.message}
        </Alert>
      )}

      {!isLoading && !isFetching && !isError && !companyData && currentTicker && (
         <Alert severity="warning" sx={{my: 2}}>No data found for {currentTicker}. It might be an invalid ticker or an issue with the data provider.</Alert>
      )}

      {companyData && (
        <>
          {companyData.profile && <CompanyProfileDisplay profile={companyData.profile} />}
          {companyData.stock_data && <StockPriceChart stockData={companyData.stock_data} />}
          {companyData.news && <NewsList newsData={companyData.news} />}
        </>
      )}
    </Container>
  );
};

export default CompanyAnalysisPage;
