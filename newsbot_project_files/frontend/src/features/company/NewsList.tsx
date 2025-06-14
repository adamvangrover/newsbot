import React from 'react';
import List from '@mui/material/List';
import Typography from '@mui/material/Typography';
import NewsListItem from './NewsListItem.tsx'; // Corrected import path
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';

// Define types for news articles - should match backend schema
interface NewsArticleData {
    id: string;
    category?: string | null;
    datetime: number; // Unix timestamp
    headline: string;
    image?: string | null; // HttpUrl
    related?: string | null;
    source: string;
    summary: string;
    url: string; // HttpUrl
    sentiment_label?: string | null;
    sentiment_score?: number | null;
    analyzed_category?: string | null;
    ai_summary?: string | null;
}

interface CompanyNewsData {
    ticker: string;
    articles: NewsArticleData[];
}

interface NewsListProps {
  newsData: CompanyNewsData | null | undefined;
}

const NewsList: React.FC<NewsListProps> = ({ newsData }) => {
  if (!newsData || !newsData.articles || newsData.articles.length === 0) {
    return <Typography sx={{mb:3}}>No news articles available.</Typography>;
  }

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>Recent News</Typography>
        <List sx={{ width: '100%', bgcolor: 'background.paper' }}>
          {newsData.articles.map((article) => (
            <NewsListItem key={article.id} article={article} />
          ))}
        </List>
      </CardContent>
    </Card>
  );
};

export default NewsList;
