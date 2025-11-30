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
import type { MarketData } from '../../api/types';

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
    <div className="bg-gray-900 border border-gray-800 p-4 rounded-lg flex flex-col h-[400px]">
      <h2 className="text-xl font-semibold text-green-500 mb-4">
        Early Warning Indicator ({ticker})
      </h2>
      <div className="flex-grow">
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
              stroke="#f97316"
              dot={false}
              strokeWidth={2}
              name="Price"
            />
            <Scatter name="Anomaly" dataKey="anomaly" fill="red" shape="circle" />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
