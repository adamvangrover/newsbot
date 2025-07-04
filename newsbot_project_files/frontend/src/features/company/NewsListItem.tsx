import React, { useState } from 'react';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import Avatar from '@mui/material/Avatar';
import Typography from '@mui/material/Typography';
import Link from '@mui/material/Link';
import Tooltip from '@mui/material/Tooltip'; // Import Tooltip
import Divider from '@mui/material/Divider';
import Box from '@mui/material/Box';
import Chip from '@mui/material/Chip';
import Button from '@mui/material/Button';
import ArticleIcon from '@mui/icons-material/Article'; // Default icon

// Using a more complete NewsArticleData, similar to marketTypes
// Ideally, this would be a shared type. For now, defining it comprehensively.
import { EntityData } from '../../types/marketTypes'; // Re-use EntityData type

interface NewsArticleData {
    id: string;
    category?: string | null;
    datetime: number; // Unix timestamp
    headline: string;
    image?: string | null;
    related?: string | null; // Ticker or symbol
    source: string;
    summary: string;
    url: string;

    // AI Processed fields
    sentiment_label?: string | null;
    sentiment_score?: number | null;
    analyzed_category?: string | null;
    ai_summary?: string | null;
    entities?: EntityData[] | null;
    detected_events?: string[] | null;
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
                 {article.category && article.category !== article.analyzed_category && (
                  <Chip label={`Src Category: ${article.category}`} size="small" variant="outlined" sx={{fontSize: '0.7rem'}} />
                )}
              </Box>

              {/* Display Detected Events */}
              {article.detected_events && article.detected_events.length > 0 && (
                <Box sx={{ mt: 1, display: 'flex', flexWrap: 'wrap', gap: 0.5, alignItems: 'center' }}>
                  <Typography variant="caption" sx={{fontWeight:'bold', color: 'text.secondary', mr: 0.5}}>Events:</Typography>
                  {article.detected_events.map((event, index) => (
                    <Chip key={`event-${article.id}-${index}`} label={event} size="small" color="secondary" variant="filled" sx={{fontSize: '0.7rem'}}/>
                  ))}
                </Box>
              )}

              {/* Display Entities */}
              {article.entities && article.entities.length > 0 && (
                 <Box sx={{ mt: 1, display: 'flex', flexWrap: 'wrap', gap: 0.5, alignItems: 'center' }}>
                  <Typography variant="caption" sx={{fontWeight:'bold', color: 'text.secondary', mr: 0.5}}>Entities:</Typography>
                  {article.entities.slice(0, 7).map((entity, index) => (
                    <Tooltip key={`entity-${article.id}-${index}-${entity.text}`} title={`${entity.label} (Score: ${entity.score.toFixed(3)})`}>
                      <Chip
                        label={entity.text}
                        size="small"
                        variant="filled"
                        sx={{
                            fontSize: '0.7rem',
                            backgroundColor: entity.label === 'ORG' ? 'primary.light'
                                           : entity.label === 'PER' ? 'success.light'
                                           : entity.label === 'LOC' ? 'warning.light'
                                           : 'info.light',
                            color: 'common.black'
                        }}
                      />
                    </Tooltip>
                  ))}
                </Box>
              )}
            </>
          }
        />
      </ListItem>
      <Divider variant="inset" component="li" />
    </>
  );
};

export default NewsListItem;
