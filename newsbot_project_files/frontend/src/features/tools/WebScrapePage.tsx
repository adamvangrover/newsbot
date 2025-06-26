import React from 'react';
import { useScrapeData } from '../../hooks/useScrapeData';
import URLInputForm from './URLInputForm';
import ScrapedDataDisplay from './ScrapedDataDisplay';
import Typography from '@mui/material/Typography';
import Alert from '@mui/material/Alert';
import Container from '@mui/material/Container';
import Paper from '@mui/material/Paper';
import Box from '@mui/material/Box';

const WebScrapePage: React.FC = () => {
  const {
    mutate: scrapeUrl,
    data: scrapeResult,
    isLoading,
    isError,
    error
  } = useScrapeData();

  const handleSubmitUrl = (url: string) => {
    scrapeUrl({ url });
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 3, mb: 3 }}>
      <Paper elevation={1} sx={{ p: {xs: 2, md:3}, mb: 3 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Web Scrape & Analyze Tool
        </Typography>
        <Typography variant="body1" color="text.secondary" sx={{mb:2}}>
          Enter a URL to fetch its main content and get an AI-powered analysis including summary, sentiment, and key entities.
        </Typography>
        <URLInputForm onSubmit={handleSubmitUrl} isLoading={isLoading} />
      </Paper>

      {/* Displaying general error from the mutation hook itself, if any */}
      {isError && error && (
        <Alert severity="error" sx={{ my: 2 }}>
          An error occurred: {error instanceof Error ? error.message : String(error)}
        </Alert>
      )}

      {/*
        Displaying specific error from backend if request was successful but processing failed,
        or the actual data if successful.
        The ScrapedDataDisplay component handles its own error display if error_message is in scrapeResult
      */}
      {scrapeResult && (
        <ScrapedDataDisplay data={scrapeResult} />
      )}

      {/* Optional: Could add a more prominent loading indicator here if the form's button isn't enough */}
      {isLoading && !scrapeResult && (
         <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
            <Typography variant="h6">Analyzing URL, please wait...</Typography>
        </Box>
      )}

    </Container>
  );
};

export default WebScrapePage;
