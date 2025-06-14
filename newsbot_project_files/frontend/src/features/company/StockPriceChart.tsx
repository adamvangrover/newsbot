import React from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

// Define types for stock data points - should match backend schema
interface StockDataPoint {
    date: string;
    open: number;
    high: number;
    low: number;
    close: number;
    volume: number;
}

interface HistoricalStockData {
    ticker: string;
    prices: StockDataPoint[];
}

interface StockPriceChartProps {
  stockData: HistoricalStockData | null | undefined;
}

const StockPriceChart: React.FC<StockPriceChartProps> = ({ stockData }) => {
  if (!stockData || !stockData.prices || stockData.prices.length === 0) {
    return <Typography sx={{mb:3}}>No stock price data available to display chart.</Typography>;
  }

  const chartData = {
    labels: stockData.prices.map(p => p.date).reverse(), // Reverse if data is chronological
    datasets: [
      {
        label: `Closing Price (${stockData.ticker})`,
        data: stockData.prices.map(p => p.close).reverse(),
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: `Stock Price Trend for ${stockData.ticker}`,
      },
    },
  };

  return (
    <Card sx={{ mb: 3 }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>Stock Performance</Typography>
        <Line options={options} data={chartData} />
      </CardContent>
    </Card>
  );
};

export default StockPriceChart;
