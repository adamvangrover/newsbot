import React, { useMemo } from 'react';
import {
  ComposedChart,
  Line,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import { MarketData } from '../../api/types';
import { Box, Typography, Paper } from '@mui/material';

interface PriceAnomalyChartProps {
  data: MarketData[];
  ticker: string;
}

export const PriceAnomalyChart: React.FC<PriceAnomalyChartProps> = ({ data, ticker }) => {
  const processedData = useMemo(() => {
    if (!data.length) return [];

    const prices = data.map(d => d.Close);
    const mean = prices.reduce((a, b) => a + b, 0) / prices.length;
    const stdDev = Math.sqrt(prices.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / prices.length);

    return data.map(d => ({
      ...d,
      time: new Date(d.Timestamp).toLocaleTimeString(),
      anomaly: Math.abs(d.Close - mean) > 2 * stdDev ? d.Close : null
    }));
  }, [data]);

  return (
    <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', height: 400 }}>
      <Typography component="h2" variant="h6" color="primary" gutterBottom>
        Early Warning Indicator ({ticker})
      </Typography>
      <Box sx={{ flexGrow: 1 }}>
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart data={processedData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#444" />
            <XAxis dataKey="time" stroke="#888" />
            <YAxis domain={['auto', 'auto']} stroke="#888" />
            <Tooltip
                contentStyle={{ backgroundColor: '#1e1e1e', border: '1px solid #444' }}
                itemStyle={{ color: '#fff' }}
            />
            <Legend />
            <Line
              type="monotone"
              dataKey="Close"
              stroke="#ff9800"
              dot={false}
              strokeWidth={2}
              name="Price"
            />
            <Scatter name="Anomaly" dataKey="anomaly" fill="red" shape="circle" />
          </ComposedChart>
        </ResponsiveContainer>
      </Box>
    </Paper>
  );
};
