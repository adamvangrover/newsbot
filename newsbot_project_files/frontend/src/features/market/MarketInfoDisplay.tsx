import React from 'react';
import { MarketOutlookResponseData, MarketSentimentData } from '../../types/marketTypes';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import Chip from '@mui/material/Chip';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import Divider from '@mui/material/Divider';

interface MarketInfoDisplayProps {
    marketData: MarketOutlookResponseData;
}

const MarketInfoDisplay: React.FC<MarketInfoDisplayProps> = ({ marketData }) => {
    const { market_sentiment, key_themes, highlighted_events, market_news_category, timestamp } = marketData;

    const renderSentiment = (sentiment: MarketSentimentData | null | undefined) => {
        if (!sentiment) return <Typography>Sentiment data unavailable.</Typography>;
        return (
            <Box>
                <Typography variant="h6" gutterBottom>Market Sentiment ({market_news_category})</Typography>
                <Chip
                    label={`Overall: ${sentiment.overall_sentiment_label}`}
                    color={
                        sentiment.overall_sentiment_label === "Positive" ? "success" :
                        sentiment.overall_sentiment_label === "Negative" ? "error" :
                        "default"
                    }
                    sx={{ mr: 1, mb: 1}}
                />
                {sentiment.average_sentiment_score !== null && typeof sentiment.average_sentiment_score !== 'undefined' && (
                     <Chip label={`Avg. Score: ${sentiment.average_sentiment_score.toFixed(3)}`} variant="outlined" sx={{ mr: 1, mb: 1}} />
                )}
                <Chip label={`Positive: ${sentiment.positive_articles}`} color="success" variant="outlined" sx={{ mr: 1, mb: 1}} />
                <Chip label={`Negative: ${sentiment.negative_articles}`} color="error" variant="outlined" sx={{ mr: 1, mb: 1}} />
                <Chip label={`Neutral: ${sentiment.neutral_articles}`} variant="outlined" sx={{ mr: 1, mb: 1}} />
            </Box>
        );
    };

    return (
        <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
            <Typography variant="h5" gutterBottom component="div">
                Market Outlook Analysis
            </Typography>
            <Typography variant="caption" display="block" gutterBottom>
                Category: {market_news_category} | Last Updated: {new Date(timestamp).toLocaleString()}
            </Typography>
            <Divider sx={{ my: 2 }} />

            <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                    {renderSentiment(market_sentiment)}
                </Grid>
                <Grid item xs={12} md={6}>
                    <Typography variant="h6" gutterBottom>Key Themes</Typography>
                    {key_themes && key_themes.length > 0 ? (
                        key_themes.map((theme, index) => (
                            <Chip key={index} label={theme} sx={{ mr: 1, mb: 1 }} />
                        ))
                    ) : (
                        <Typography>No specific themes identified.</Typography>
                    )}
                </Grid>
                <Grid item xs={12}>
                    <Typography variant="h6" gutterBottom>Highlighted Events/News</Typography>
                    {highlighted_events && highlighted_events.length > 0 ? (
                        <List dense>
                            {highlighted_events.map((event, index) => (
                                <ListItem key={index} disableGutters>
                                    <ListItemText primary={event} />
                                </ListItem>
                            ))}
                        </List>
                    ) : (
                        <Typography>No specific highlighted events.</Typography>
                    )}
                </Grid>
            </Grid>
        </Paper>
    );
};

export default MarketInfoDisplay;
