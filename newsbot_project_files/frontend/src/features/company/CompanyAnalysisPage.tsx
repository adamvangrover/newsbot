import React, { useState } from 'react';
import CompanySearch from './CompanySearch';
import CompanyProfileDisplay from './CompanyProfileDisplay';
import StockPriceChart from './StockPriceChart';
import NewsList from './NewsList';
import TopicDisplay from '../../components/TopicDisplay';
import { useCompanyData } from '../../hooks/useCompanyData';
import { usePortfolios } from '../../hooks/usePortfolios';
import { PortfolioData } from '../../types/portfolioTypes';
import Typography from '@mui/material/Typography';
import CircularProgress from '@mui/material/CircularProgress';
import Alert from '@mui/material/Alert';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';

const CompanyAnalysisPage: React.FC = () => {
  const [currentTicker, setCurrentTicker] = useState<string>('');
  const [newsDays, setNewsDays] = useState<number>(7);
  const [selectedPortfolio, setSelectedPortfolio] = useState<PortfolioData | null>(null);

  const { data: companyData, error, isLoading, isFetching, isError } = useCompanyData(currentTicker, newsDays);
  const { data: portfolios } = usePortfolios();

  const handleSearch = (ticker: string, days?: number) => {
    setSelectedPortfolio(null); // Clear portfolio selection
    setCurrentTicker(ticker);
    if (days) {
      setNewsDays(days);
    } else {
      setNewsDays(7);
    }
  };

  const handlePortfolioChange = (event: SelectChangeEvent<string>) => {
    const portfolioId = parseInt(event.target.value, 10);
    const portfolio = portfolios?.find(p => p.id === portfolioId) || null;
    setSelectedPortfolio(portfolio);
    if (portfolio) {
        setCurrentTicker(''); // Clear ticker search
        // TODO: Implement portfolio analysis fetching
        // This would likely involve a new hook `usePortfolioAnalysis(portfolio.id)`
        // and a new API endpoint like `/portfolio-analysis/{portfolio_id}`
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 2, mb: 3 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Company & Portfolio Analysis
      </Typography>

      <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
        <CompanySearch onSearch={handleSearch} isLoading={isLoading || isFetching} initialDays={newsDays} disabled={!!selectedPortfolio} />

        <FormControl sx={{ minWidth: 200 }}>
          <InputLabel id="portfolio-select-label">Or Select Portfolio</InputLabel>
          <Select
            labelId="portfolio-select-label"
            value={selectedPortfolio?.id?.toString() || ''}
            onChange={handlePortfolioChange}
            label="Or Select Portfolio"
            disabled={!portfolios || portfolios.length === 0}
          >
            <MenuItem value="">
              <em>None</em>
            </MenuItem>
            {portfolios?.map(p => (
              <MenuItem key={p.id} value={p.id}>{p.name}</MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>

      {(isLoading || isFetching) && (
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', my: 3, flexDirection: 'column' }}>
          <CircularProgress />
          <Typography sx={{mt:1}}>Loading data for {currentTicker || selectedPortfolio?.name}...</Typography>
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
          {companyData.topics && <TopicDisplay topicsData={companyData.topics} />}
          {companyData.stock_data && <StockPriceChart stockData={companyData.stock_data} />}
          {companyData.news && <NewsList newsData={companyData.news} />}
        </>
      )}
    </Container>
  );
};

export default CompanyAnalysisPage;
