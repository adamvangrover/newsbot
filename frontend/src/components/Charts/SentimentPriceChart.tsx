import React, { useMemo } from 'react';
import {
  ComposedChart,
  Line,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import { MarketData, SocialSentiment } from '../../api/types';
import { Box, Typography, Paper } from '@mui/material';

interface SentimentPriceChartProps {
  marketData: MarketData[];
  sentimentData: SocialSentiment[];
  ticker: string;
}

export const SentimentPriceChart: React.FC<SentimentPriceChartProps> = ({ marketData, sentimentData, ticker }) => {
  const chartData = useMemo(() => {
    // Merge data by roughly matching timestamps or just using index if data is aligned.
    // For synthetic data, timestamps might not match exactly, so we'll try to align by closest hour or just take a subset.
    // Assuming 1-min market data and hourly sentiment. We can map market data to hourly average or just plot them on same time axis.

    // Simplification: We will just take the market data and try to find a matching sentiment record (or nearest).
    // Or better, let's just plot them independently if timestamps differ significantly.
    // But Recharts wants a single data array.

    // Let's index sentiment by timestamp (hour)
    const sentimentMap = new Map(sentimentData.map(s => {
        const timeKey = new Date(s.Timestamp).toISOString().substring(0, 13); // yyyy-mm-ddThh
        return [timeKey, s];
    }));

    // Downsample market data to hourly to match sentiment or just plot all market data and sparsely populate sentiment
    // Let's filter market data to hourly for clearer visualization
    const hourlyMarketData = marketData.filter((_, i) => i % 60 === 0); // Approx hourly if data is 1 min

    return hourlyMarketData.map(d => {
        const timeKey = new Date(d.Timestamp).toISOString().substring(0, 13);
        const sentiment = sentimentMap.get(timeKey);
        return {
            time: new Date(d.Timestamp).toLocaleString(),
            price: d.Close,
            sentimentVolume: sentiment ? sentiment.Social_Media_Volume : 0,
            sentimentDivergence: sentiment ? sentiment.Sentiment_Divergence : 0
        };
    });
  }, [marketData, sentimentData]);

  return (
    <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', height: 400 }}>
      <Typography component="h2" variant="h6" color="primary" gutterBottom>
        Sentiment Correlation ({ticker})
      </Typography>
      <Box sx={{ flexGrow: 1 }}>
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#444" />
            <XAxis dataKey="time" stroke="#888" />
            <YAxis yAxisId="left" stroke="#ff9800" label={{ value: 'Price', angle: -90, position: 'insideLeft' }} />
            <YAxis yAxisId="right" orientation="right" stroke="#82ca9d" label={{ value: 'Sentiment Volume', angle: 90, position: 'insideRight' }} />
            <Tooltip
                contentStyle={{ backgroundColor: '#1e1e1e', border: '1px solid #444' }}
                itemStyle={{ color: '#fff' }}
            />
            <Legend />
            <Line yAxisId="left" type="monotone" dataKey="price" stroke="#ff9800" dot={false} />
            <Bar yAxisId="right" dataKey="sentimentVolume" barSize={20} fill="#82ca9d" opacity={0.5} />
          </ComposedChart>
        </ResponsiveContainer>
      </Box>
    </Paper>
  );
};
