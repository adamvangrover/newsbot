import { useQuery, UseQueryResult } from 'react-query';
import apiClient from '../api/apiClient';

// Define response types based on backend schemas
// CompanyProfile from backend/app/schemas/company.py
interface CompanyProfileData {
    country?: string | null;
    currency?: string | null;
    exchange?: string | null;
    name?: string | null;
    ticker: string;
    ipo?: string | null;
    marketCapitalization?: number | null;
    shareOutstanding?: number | null;
    logo?: string | null;
    phone?: string | null;
    weburl?: string | null;
    finnhubIndustry?: string | null;
}

// StockDataPoint & HistoricalStockData from backend/app/schemas/company.py
interface StockDataPoint {
    date: string;
    open: number;
    high: number;
    low: number;
    close: number;
    volume: number;
}
interface HistoricalStockData {
    ticker: string;
    prices: StockDataPoint[];
}

// NewsArticle & CompanyNews from backend/app/schemas/news.py
interface NewsArticleData {
    id: string;
    category?: string | null;
    datetime: number;
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
interface CompanyNewsData {
    ticker: string;
    articles: NewsArticleData[];
}

// Combined API Response (matches backend/app/api/v1/endpoints/company.py CompanyAnalysisResponse)
interface CompanyAnalysisResponse {
    ticker: string;
    profile?: CompanyProfileData | null;
    news?: CompanyNewsData | null;
    stock_data?: HistoricalStockData | null;
    topics?: { top_topics: any[] } | null;
}

const fetchCompanyAnalysis = async (ticker: string, newsDaysAgo: number = 7): Promise<CompanyAnalysisResponse> => {
  if (!ticker) {
    // react-query's enabled option is better for conditional fetching
    throw new Error("Ticker symbol cannot be empty.");
  }
  const { data } = await apiClient.get<CompanyAnalysisResponse>(
    `/company-analysis/${ticker}`,
    { params: { news_days_ago: newsDaysAgo } }
  );
  return data;
};

export const useCompanyData = (ticker: string, newsDaysAgo: number = 7): UseQueryResult<CompanyAnalysisResponse, Error> => {
  return useQuery<CompanyAnalysisResponse, Error>(
    ['companyAnalysis', ticker, newsDaysAgo], // Query key
    () => fetchCompanyAnalysis(ticker, newsDaysAgo),
    {
      enabled: !!ticker, // Only run query if ticker is truthy
      // Add other react-query options here, e.g., staleTime, cacheTime, refetchOnWindowFocus: false
      // staleTime: 5 * 60 * 1000, // 5 minutes
      // cacheTime: 15 * 60 * 1000, // 15 minutes
    }
  );
};
