import React from 'react';
import List from '@mui/material/List';
import Typography from '@mui/material/Typography';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import MarketNewsListItem from './MarketNewsListItem'; // Use the new MarketNewsListItem
import { NewsArticleData } from '../../types/marketTypes'; // Use the correct type

interface MarketNewsListProps {
  articles?: NewsArticleData[] | null;
  listTitle?: string;
}

const MarketNewsList: React.FC<MarketNewsListProps> = ({ articles, listTitle = "Market News Articles" }) => {
  if (!articles || articles.length === 0) {
    return (
        <Card sx={{mt: 2}}>
            <CardContent>
                <Typography variant="subtitle1" sx={{textAlign: 'center'}}>No market news articles available.</Typography>
            </CardContent>
        </Card>
    );
  }

  return (
    <Card sx={{mt:2}}>
      <CardContent>
        <Typography variant="h6" gutterBottom>{listTitle}</Typography>
        <List sx={{ width: '100%', bgcolor: 'background.paper', p: 0 }}> {/* Removed padding from List */}
          {articles.map((article) => (
            <MarketNewsListItem key={article.id} article={article} />
          ))}
        </List>
      </CardContent>
    </Card>
  );
};

export default MarketNewsList;
