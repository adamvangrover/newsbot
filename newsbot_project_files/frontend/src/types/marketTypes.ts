// Corresponds to backend/app/api/v1/endpoints/market.py MarketSentiment
export interface MarketSentimentData {
    overall_sentiment_label: string;
    average_sentiment_score?: number | null;
    positive_articles: number;
    negative_articles: number;
    neutral_articles: number;
}

// Re-using NewsArticleData from useCompanyData.ts for consistency,
// but if it diverges, a specific MarketNewsArticleData might be needed.
// For now, let's assume NewsArticleData is suitable.
// If not, define it here:
// export interface MarketNewsArticleData { ... }

// We need NewsArticleData definition if it's not globally available
// For now, let's copy it here and then consider refactoring to a shared types location
// This is from newsbot_project_files/frontend/src/hooks/useCompanyData.ts

export interface EntityData { // From backend ner.py (simplified)
    text: string;
    label: string;
    score: number;
    start_offset?: number;
    end_offset?: number;
}
export interface NewsArticleData {
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


// Corresponds to backend/app/api/v1/endpoints/market.py MarketOutlookResponse
export interface MarketOutlookResponseData {
    timestamp: string; // ISO datetime string
    market_news_category: string;
    market_sentiment?: MarketSentimentData | null;
    topics?: { top_topics: any[] } | null;
    highlighted_events: string[];
    processed_articles: NewsArticleData[];
}
