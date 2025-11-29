import React, { useEffect, useState } from 'react';
import { Grid, Typography, Box, CircularProgress, Alert } from '@mui/material';
import { useApiClient } from '../api/apiClient';
import { MarketData, SocialSentiment } from '../api/types';
import { PriceAnomalyChart } from '../components/Charts/PriceAnomalyChart';
import { SentimentPriceChart } from '../components/Charts/SentimentPriceChart';
import { ClusterScatterPlot } from '../components/Charts/ClusterScatterPlot';

export const PerformanceDashboard: React.FC = () => {
  const provider = useApiClient();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [marketData, setMarketData] = useState<MarketData[]>([]);
  const [sentimentData, setSentimentData] = useState<SocialSentiment[]>([]);

  // Hardcoded ticker for demo
  const TICKER = 'AAPL';

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        // Fetch data in parallel
        const [mDat, sDat] = await Promise.all([
          provider.getMarketData(TICKER),
          provider.getSocialSentiment(TICKER)
        ]);

        setMarketData(mDat);
        setSentimentData(sDat);
      } catch (err) {
        console.error(err);
        setError('Failed to load performance data.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [provider]);

  if (loading) {
    return (
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
            <CircularProgress />
        </Box>
    );
  }

  if (error) {
    return <Alert severity="error">{error}</Alert>;
  }

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Typography variant="h4" gutterBottom>
        Analyst Playbook: {TICKER}
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <PriceAnomalyChart data={marketData} ticker={TICKER} />
        </Grid>
        <Grid item xs={12} md={4}>
           {/* Placeholder for stats or another chart */}
           <ClusterScatterPlot />
        </Grid>
        <Grid item xs={12}>
          <SentimentPriceChart marketData={marketData} sentimentData={sentimentData} ticker={TICKER} />
        </Grid>
      </Grid>
    </Box>
  );
};
