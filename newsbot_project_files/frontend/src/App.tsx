import React, { useState } from 'react';
import Header from './components/Layout/Header';
import MainContent from './components/Layout/MainContent';
import CompanySearch from './features/company/CompanySearch';
import CompanyProfileDisplay from './features/company/CompanyProfileDisplay';
import StockPriceChart from './features/company/StockPriceChart';
import NewsList from './features/company/NewsList';
import { useCompanyData } from './hooks/useCompanyData';
import Typography from '@mui/material/Typography';
import CircularProgress from '@mui/material/CircularProgress';
import Alert from '@mui/material/Alert';
import Box from '@mui/material/Box';

function App() {
  const [currentTicker, setCurrentTicker] = useState<string>('');
  const [newsDays, setNewsDays] = useState<number>(7); // Default to 7 days of news

  // Fetch data using the custom hook
  const { data: companyData, error, isLoading, isFetching, isError } = useCompanyData(currentTicker, newsDays);

  const handleSearch = (ticker: string) => {
    setCurrentTicker(ticker);
    // newsDays could also be part of the search form
  };

  return (
    <>
      <Header />
      <MainContent>
        <CompanySearch onSearch={handleSearch} isLoading={isLoading || isFetching} />

        {(isLoading || isFetching) && (
          <Box sx={{ display: 'flex', justifyContent: 'center', my: 3 }}>
            <CircularProgress />
          </Box>
        )}

        {isError && error && (
          <Alert severity="error" sx={{ my: 2 }}>
            Error fetching data: {error.message}
          </Alert>
        )}

        {!isLoading && !isFetching && !isError && !companyData && currentTicker && (
           <Typography sx={{my: 2}}>No data found for {currentTicker}. It might be an invalid ticker or an issue with the data provider.</Typography>
        )}

        {companyData && (
          <>
            <CompanyProfileDisplay profile={companyData.profile} />
            <StockPriceChart stockData={companyData.stock_data} />
            <NewsList newsData={companyData.news} />
          </>
        )}
      </MainContent>
    </>
  );
}

export default App;
