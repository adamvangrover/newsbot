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
import Tooltip from '@mui/material/Tooltip';
import ArticleIcon from '@mui/icons-material/Article'; // Default icon

import { NewsArticleData, EntityData } from '../../types/marketTypes'; // Correct import path

interface MarketNewsListItemProps {
  article: NewsArticleData;
}

const MarketNewsListItem: React.FC<MarketNewsListItemProps> = ({ article }) => {
  const [showAiSummary, setShowAiSummary] = useState(false);

  const sentimentColor = (label: string | null | undefined): ('success' | 'error' | 'warning' | 'default') => {
    if (!label) return 'default';
    const lowerLabel = label.toLowerCase();
    if (lowerLabel === 'positive') return 'success';
    if (lowerLabel === 'negative') return 'error';
    if (lowerLabel === 'neutral') return 'warning'; // Or 'info' based on preference
    return 'default';
  };

  return (
    <>
      <ListItem alignItems="flex-start" sx={{py: 2}}> {/* Added padding top/bottom */}
        <ListItemAvatar>
          <Avatar alt={article.source} src={article.image || undefined} sx={{width: 56, height: 56, mr:1}}>
            {!article.image && <ArticleIcon fontSize="large"/>}
          </Avatar>
        </ListItemAvatar>
        <ListItemText
          primary={
            <Link href={article.url} target="_blank" rel="noopener noreferrer" underline="hover" title={article.headline}>
              <Typography variant="h6" component="span">{article.headline}</Typography>
            </Link>
          }
          secondary={
            <>
              <Typography
                sx={{ display: 'block', mb: 0.5 }}
                component="span"
                variant="body2"
                color="text.secondary"
              >
                {article.source} - {new Date(article.datetime * 1000).toLocaleString()}
              </Typography>
              <Typography component="span" variant="body2" sx={{ display: 'block', mt: 0.5 }}>
                {article.summary}
              </Typography>
              {article.ai_summary && article.ai_summary !== article.summary && (
                <Button size="small" onClick={() => setShowAiSummary(!showAiSummary)} sx={{ mt: 0.5, p:0.2, textTransform: 'none' }}>
                  {showAiSummary ? 'Hide AI Summary' : 'Show AI Summary'}
                </Button>
              )}
              {showAiSummary && article.ai_summary && (
                <Typography component="p" variant="caption" sx={{ display: 'block', mt: 0.5, fontStyle: 'italic', backgroundColor: (theme) => theme.palette.grey[100], p:1, borderRadius: 1 }}>
                  <strong>AI Summary:</strong> {article.ai_summary}
                </Typography>
              )}
              <Box sx={{ mt: 1, display: 'flex', gap: 0.75, flexWrap: 'wrap', alignItems: 'center' }}>
                {article.sentiment_label && (
                  <Tooltip title={`Score: ${article.sentiment_score?.toFixed(3) ?? 'N/A'}`}>
                    <Chip
                        label={`Sentiment: ${article.sentiment_label}`}
                        size="small"
                        color={sentimentColor(article.sentiment_label)}
                        variant="outlined"
                    />
                  </Tooltip>
                )}
                {article.analyzed_category && (
                  <Chip label={`AI Category: ${article.analyzed_category}`} size="small" variant="outlined" />
                )}
                 {article.category && article.category !== article.analyzed_category && (
                  <Chip label={`Src Category: ${article.category}`} size="small" variant="outlined" sx={{fontSize: '0.7rem'}} />
                )}
              </Box>

              {article.detected_events && article.detected_events.length > 0 && (
                <Box sx={{ mt: 1, display: 'flex', flexWrap: 'wrap', gap: 0.5, alignItems: 'center' }}>
                  <Typography variant="caption" sx={{fontWeight:'bold', color: 'text.secondary', mr: 0.5}}>Events:</Typography>
                  {article.detected_events.map((event, index) => (
                    <Chip key={`event-${index}`} label={event} size="small" color="secondary" variant="filled" sx={{fontSize: '0.7rem'}}/>
                  ))}
                </Box>
              )}

              {article.entities && article.entities.length > 0 && (
                 <Box sx={{ mt: 1, display: 'flex', flexWrap: 'wrap', gap: 0.5, alignItems: 'center' }}>
                  <Typography variant="caption" sx={{fontWeight:'bold', color: 'text.secondary', mr: 0.5}}>Entities:</Typography>
                  {article.entities.slice(0, 7).map((entity, index) => ( // Show top 7 entities
                    <Tooltip key={`entity-${index}-${entity.text}`} title={`${entity.label} (Score: ${entity.score.toFixed(3)})`}>
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

export default MarketNewsListItem;
