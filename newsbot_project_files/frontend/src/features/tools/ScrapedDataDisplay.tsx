import React from 'react';
import { ScrapeAndAnalyzeResponseData, AIScrapedContentFeaturesData } from '../../types/toolsTypes';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';
import Box from '@mui/material/Box';
import Chip from '@mui/material/Chip';
import Link from '@mui/material/Link';
import Divider from '@mui/material/Divider';
import Grid from '@mui/material/Grid'; // For layout
import Tooltip from '@mui/material/Tooltip';

interface ScrapedDataDisplayProps {
  data: ScrapeAndAnalyzeResponseData;
}

const ScrapedDataDisplay: React.FC<ScrapedDataDisplayProps> = ({ data }) => {
  const { requested_url, page_title, scraped_text_snippet, full_text_char_count, ai_analysis, error_message } = data;

  const sentimentColor = (label?: string | null): "success" | "error" | "warning" | "info" | "default" => {
    if (!label) return "default";
    const lowerLabel = label.toLowerCase();
    if (lowerLabel === 'positive') return 'success';
    if (lowerLabel === 'negative') return 'error';
    if (lowerLabel === 'neutral') return 'warning';
    return 'default';
  };

  if (error_message) {
    return (
      <Paper elevation={3} sx={{ p: 2, mt: 2, borderColor: 'error.main', borderWidth: 1, borderStyle: 'solid' }}>
        <Typography variant="h6" color="error" gutterBottom>Analysis Failed</Typography>
        <Typography><strong>URL:</strong> {requested_url}</Typography>
        <Typography color="error"><strong>Error:</strong> {error_message}</Typography>
      </Paper>
    );
  }

  if (!ai_analysis && !scraped_text_snippet) {
      return (
        <Paper elevation={3} sx={{p:2, mt:2}}>
            <Typography>No analysis data or scraped content to display for <Link href={requested_url} target="_blank" rel="noopener noreferrer">{requested_url}</Link>.</Typography>
        </Paper>
      )
  }

  return (
    <Paper elevation={3} sx={{ p: {xs: 2, md: 3} , mt: 2 }}>
      <Typography variant="h5" gutterBottom component="div">
        Analysis for: <Link href={requested_url} target="_blank" rel="noopener noreferrer" sx={{wordBreak: 'break-all'}}>{page_title || requested_url}</Link>
      </Typography>
      {page_title && <Typography variant="subtitle1" color="text.secondary">Original Title: {page_title}</Typography>}
      <Divider sx={{ my: 2 }} />

      <Grid container spacing={3}>
        {ai_analysis && (
          <Grid item xs={12} md={ai_analysis.ai_summary ? 7 : 12}> {/* Wider if no summary */}
            <Typography variant="h6" gutterBottom>AI Analysis</Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2, alignItems: 'center' }}>
              {ai_analysis.sentiment_label && (
                <Tooltip title={`Score: ${ai_analysis.sentiment_score?.toFixed(3) ?? 'N/A'}`}>
                  <Chip
                    label={`Sentiment: ${ai_analysis.sentiment_label}`}
                    color={sentimentColor(ai_analysis.sentiment_label)}
                    variant="outlined"
                  />
                </Tooltip>
              )}
              {ai_analysis.analyzed_category && ( // Less prominent for general pages
                <Chip label={`Category: ${ai_analysis.analyzed_category}`} size="small" variant="outlined" />
              )}
            </Box>

            {ai_analysis.entities && ai_analysis.entities.length > 0 && (
              <Box mb={2}>
                <Typography variant="subtitle1" gutterBottom sx={{fontWeight: 'medium'}}>Key Entities:</Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                  {ai_analysis.entities.slice(0, 10).map((entity, index) => ( // Show top 10
                    <Tooltip key={`entity-${index}-${entity.text}`} title={`${entity.label} (Score: ${entity.score.toFixed(3)})`}>
                       <Chip
                        label={entity.text}
                        size="small"
                        variant="filled"
                        sx={{
                            fontSize: '0.75rem',
                            backgroundColor: entity.label === 'ORG' ? 'primary.light'
                                           : entity.label === 'PER' ? 'success.light'
                                           : entity.label === 'LOC' ? 'warning.light'
                                           : 'info.light',
                            color: 'common.black',
                            mb:0.5
                        }}
                      />
                    </Tooltip>
                  ))}
                </Box>
              </Box>
            )}

            {ai_analysis.detected_events && ai_analysis.detected_events.length > 0 && ( // Less prominent
                 <Box mb={2}>
                    <Typography variant="subtitle1" gutterBottom sx={{fontWeight: 'medium'}}>Possible Detected Events:</Typography>
                     <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                        {ai_analysis.detected_events.map((event, index) => (
                            <Chip key={`event-${index}`} label={event} size="small" color="secondary" variant="outlined" sx={{mb:0.5, fontSize: '0.75rem'}} />
                        ))}
                    </Box>
                </Box>
            )}
          </Grid>
        )}

        {ai_analysis?.ai_summary && (
            <Grid item xs={12} md={ai_analysis ? 5 : 12}>
                 <Typography variant="h6" gutterBottom>AI Summary</Typography>
                 <Typography variant="body2" paragraph sx={{whiteSpace: 'pre-line', maxHeight: '400px', overflowY: 'auto', border: '1px solid #eee', p:1, borderRadius: 1}}>
                    {ai_analysis.ai_summary}
                </Typography>
            </Grid>
        )}
      </Grid>

      {scraped_text_snippet && (
        <Box mt={3}>
          <Divider sx={{ my: 2 }} />
          <Typography variant="h6" gutterBottom>Scraped Text Snippet</Typography>
          <Typography variant="caption" display="block" gutterBottom>
            (First ~1000 characters of ~{full_text_char_count} total characters)
          </Typography>
          <Paper variant="outlined" sx={{ p: 2, maxHeight: '300px', overflowY: 'auto', backgroundColor: '#f9f9f9' }}>
            <Typography variant="body2" sx={{ whiteSpace: 'pre-line', fontFamily: 'monospace', fontSize: '0.8rem' }}>
              {scraped_text_snippet}
            </Typography>
          </Paper>
        </Box>
      )}
    </Paper>
  );
};

export default ScrapedDataDisplay;
