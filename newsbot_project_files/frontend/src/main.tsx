import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.tsx';
import './index.css';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import theme from './lib/theme.ts';
import { QueryClient, QueryClientProvider } from 'react-query';
// Optional: To show loading indicators or devtools for react-query
// import { ReactQueryDevtools } from 'react-query/devtools';

// Create a client
const queryClient = new QueryClient();

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <CssBaseline /> {/* MUI's CSS reset and baseline styles */}
        <App />
      </ThemeProvider>
      {/* Optional: React Query Devtools for debugging cache */}
      {/* <ReactQueryDevtools initialIsOpen={false} /> */}
    </QueryClientProvider>
  </React.StrictMode>,
);
