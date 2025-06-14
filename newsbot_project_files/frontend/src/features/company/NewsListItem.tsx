import React, { useState } from 'react';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import Avatar from '@mui/material/Avatar';
import Typography from '@mui/material/Typography';
import Link from '@mui/material/Link';
import Divider from '@mui/material/Divider';
import Box from '@mui/material/Box';
import Chip from '@mui/material/Chip';
import Button from '@mui/material/Button';
import ArticleIcon from '@mui/icons-material/Article'; // Default icon

// Define type for a single news article - should match backend schema
interface NewsArticleData {
    id: string;
    category?: string | null;
    datetime: number; // Unix timestamp
    headline: string;
    image?: string | null;
    related?: string | null;
    source: string;
    summary: string;
    url: string;
    sentiment_label?: string | null;
    sentiment_score?: number | null;
    analyzed_category?: string | null;
    ai_summary?: string | null;
}

interface NewsListItemProps {
  article: NewsArticleData;
}

const NewsListItem: React.FC<NewsListItemProps> = ({ article }) => {
  const [showAiSummary, setShowAiSummary] = useState(false);

  const sentimentColor = (label: string | null | undefined): ('success' | 'error' | 'warning' | 'default') => {
    if (!label) return 'default';
    if (label.toLowerCase() === 'positive') return 'success';
    if (label.toLowerCase() === 'negative') return 'error';
    if (label.toLowerCase() === 'neutral') return 'warning';
    return 'default';
  };

  return (
    <>
      <ListItem alignItems="flex-start">
        <ListItemAvatar>
          <Avatar alt={article.source} src={article.image || undefined}>
            {!article.image && <ArticleIcon />}
          </Avatar>
        </ListItemAvatar>
        <ListItemText
          primary={
            <Link href={article.url} target="_blank" rel="noopener noreferrer" underline="hover">
              {article.headline}
            </Link>
          }
          secondary={
            <>
              <Typography
                sx={{ display: 'block' }}
                component="span"
                variant="body2"
                color="text.primary"
              >
                {article.source} - {new Date(article.datetime * 1000).toLocaleDateString()}
              </Typography>
              <Typography component="span" variant="body2" sx={{ display: 'block', mt: 0.5 }}>
                {article.summary}
              </Typography>
              {article.ai_summary && (
                <Button size="small" onClick={() => setShowAiSummary(!showAiSummary)} sx={{ mt: 0.5, p:0.2 }}>
                  {showAiSummary ? 'Hide AI Summary' : 'Show AI Summary'}
                </Button>
              )}
              {showAiSummary && article.ai_summary && (
                <Typography component="p" variant="caption" sx={{ display: 'block', mt: 0.5, fontStyle: 'italic', backgroundColor: '#f9f9f9', p:1, borderRadius: 1 }}>
                  <strong>AI:</strong> {article.ai_summary}
                </Typography>
              )}
              <Box sx={{ mt: 1, display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                {article.sentiment_label && (
                  <Chip label={`Sentiment: ${article.sentiment_label} (${article.sentiment_score?.toFixed(2)})`} size="small" color={sentimentColor(article.sentiment_label)} />
                )}
                {article.analyzed_category && (
                  <Chip label={`AI Category: ${article.analyzed_category}`} size="small" variant="outlined" />
                )}
                 {article.category && ( // Original category from Finnhub
                  <Chip label={`Source Category: ${article.category}`} size="small" variant="outlined" />
                )}
              </Box>
            </>
          }
        />
      </ListItem>
      <Divider variant="inset" component="li" />
    </>
  );
};

export default NewsListItem;
