import React from 'react';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';
import Chip from '@mui/material/Chip';
import Box from '@mui/material/Box';

interface Topic {
  Topic: number;
  Count: number;
  Name: string;
}

interface TopicDisplayProps {
  topicsData?: { top_topics: Topic[] } | null;
}

const TopicDisplay: React.FC<TopicDisplayProps> = ({ topicsData }) => {
  if (!topicsData || !topicsData.top_topics || topicsData.top_topics.length === 0) {
    return null;
  }

  const topics = topicsData.top_topics;

  return (
    <Paper elevation={2} sx={{ p: 2, my: 2 }}>
      <Typography variant="h6" component="h3" gutterBottom>
        Key News Topics
      </Typography>
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
        {topics.map((topic) => (
          <Chip key={topic.Topic} label={topic.Name.replace(/_/g, ' ')} variant="outlined" />
        ))}
      </Box>
    </Paper>
  );
};

export default TopicDisplay;
