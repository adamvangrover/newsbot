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
  ResponsiveContainer
} from 'recharts';

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
    <div className="bg-gray-900 border border-gray-800 p-4 rounded-lg flex flex-col h-[400px]">
      <h2 className="text-xl font-semibold text-green-500 mb-4">
        News Clusters (Semantic Grouping)
      </h2>
      <div className="flex-grow">
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
                            <div className="bg-gray-900 p-3 border border-gray-700 rounded shadow-lg text-sm">
                                <p className="text-white font-bold">{data.topic}</p>
                                <p className="text-gray-400">Impact: {data.z.toFixed(0)}</p>
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
      </div>
    </div>
  );
};
