import React, { useState } from 'react';
import { useMarketData } from '../../hooks/useMarketData';
import MarketInfoDisplay from './MarketInfoDisplay';
import MarketNewsList from './MarketNewsList';
import Typography from '@mui/material/Typography';
import CircularProgress from '@mui/material/CircularProgress';
import Alert from '@mui/material/Alert';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import Paper from '@mui/material/Paper';

const MarketOutlookPage: React.FC = () => {
  const [newsCategory, setNewsCategory] = useState<string>("general");
  const maxArticlesToProcess = 30; // Keep it lower for market overview

  const { data: marketData, error, isLoading, isFetching, isError } = useMarketData(newsCategory, maxArticlesToProcess);

  const handleCategoryChange = (event: SelectChangeEvent<string>) => {
    setNewsCategory(event.target.value as string);
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 3, mb: 3 }}>
      <Paper elevation={1} sx={{ p: 2, mb: 2 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h4" component="h1">
                Market Outlook
            </Typography>
            <FormControl sx={{ m: 1, minWidth: 120 }} size="small">
                <InputLabel id="market-category-select-label">Category</InputLabel>
                <Select
                    labelId="market-category-select-label"
                    id="market-category-select"
                    value={newsCategory}
                    label="Category"
                    onChange={handleCategoryChange}
                >
                    <MenuItem value="general">General</MenuItem>
                    <MenuItem value="forex">Forex</MenuItem>
                    <MenuItem value="crypto">Crypto</MenuItem>
                    <MenuItem value="merger">Mergers</MenuItem>
                    {/* Add more categories as supported by Finnhub or your backend */}
                </Select>
            </FormControl>
        </Box>
      </Paper>

      {(isLoading || isFetching) && (
        <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
          <CircularProgress size={50} />
          <Typography sx={{ml: 2}}>Loading market data for '{newsCategory}'...</Typography>
        </Box>
      )}

      {isError && error && (
        <Alert severity="error" sx={{ my: 2 }}>
          Error fetching market data: {error.message}
        </Alert>
      )}

      {!isLoading && !isFetching && !isError && !marketData?.processed_articles?.length && (
         <Alert severity="info" sx={{ my: 2 }}>No market data found for the selected category '{newsCategory}'.</Alert>
      )}

      {marketData && marketData.processed_articles && marketData.processed_articles.length > 0 && (
        <>
          <MarketInfoDisplay marketData={marketData} />
          <MarketNewsList
            articles={marketData.processed_articles}
            listTitle={`Recent Articles for ${marketData.market_news_category} (${marketData.processed_articles.length})`}
          />
        </>
      )}
    </Container>
  );
};

export default MarketOutlookPage;
