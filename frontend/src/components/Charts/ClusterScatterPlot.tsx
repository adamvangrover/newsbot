import React, { useMemo } from 'react';
import {
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  ZAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell
} from 'recharts';
import { Box, Typography, Paper } from '@mui/material';

// Static topics for simulation
const TOPICS = ['Earnings', 'Geopolitics', 'Mergers', 'Regulations', 'Product Launch'];
const COLORS = ['#8884d8', '#82ca9d', '#ffc658', '#ff7300', '#0088fe'];

export const ClusterScatterPlot: React.FC = () => {
  const data = useMemo(() => {
    // Generate random clusters
    const clusters = [];
    for (let i = 0; i < 50; i++) {
        const topicIndex = Math.floor(Math.random() * TOPICS.length);
        const topic = TOPICS[topicIndex];
        // Create clusters by biasing coordinates based on topic
        const xBias = topicIndex * 100;
        const yBias = (topicIndex % 2) * 100;

        clusters.push({
            x: xBias + Math.random() * 80,
            y: yBias + Math.random() * 80,
            z: Math.random() * 100, // Impact score
            topic
        });
    }
    return clusters;
  }, []);

  return (
    <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', height: 400 }}>
      <Typography component="h2" variant="h6" color="primary" gutterBottom>
        News Clusters (Semantic Grouping)
      </Typography>
      <Box sx={{ flexGrow: 1 }}>
        <ResponsiveContainer width="100%" height="100%">
          <ScatterChart>
            <CartesianGrid strokeDasharray="3 3" stroke="#444" />
            <XAxis type="number" dataKey="x" name="Semantic Dim 1" stroke="#888" />
            <YAxis type="number" dataKey="y" name="Semantic Dim 2" stroke="#888" />
            <ZAxis type="number" dataKey="z" range={[50, 400]} name="Impact" />
            <Tooltip
                cursor={{ strokeDasharray: '3 3' }}
                content={({ active, payload }) => {
                    if (active && payload && payload.length) {
                        const data = payload[0].payload;
                        return (
                            <div style={{ backgroundColor: '#1e1e1e', padding: '10px', border: '1px solid #444' }}>
                                <p style={{color: '#fff'}}>{data.topic}</p>
                                <p style={{color: '#ccc'}}>Impact: {data.z.toFixed(0)}</p>
                            </div>
                        );
                    }
                    return null;
                }}
            />
            <Legend />
            {TOPICS.map((topic, index) => (
                <Scatter
                    key={topic}
                    name={topic}
                    data={data.filter(d => d.topic === topic)}
                    fill={COLORS[index % COLORS.length]}
                />
            ))}
          </ScatterChart>
        </ResponsiveContainer>
      </Box>
    </Paper>
  );
};
