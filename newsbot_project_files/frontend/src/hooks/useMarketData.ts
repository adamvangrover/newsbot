import { useQuery, UseQueryResult } from 'react-query';
import apiClient from '../api/apiClient';
import { MarketOutlookResponseData } from '../types/marketTypes'; // Import the new types

// Define the fetch function for market outlook
const fetchMarketOutlook = async (
    newsCategory: string = "general",
    maxArticlesToProcess: number = 50
): Promise<MarketOutlookResponseData> => {
    const { data } = await apiClient.get<MarketOutlookResponseData>(
        '/market/outlook', // Relative to the baseURL in apiClient
        {
            params: {
                news_category: newsCategory,
                max_articles_to_process: maxArticlesToProcess,
            },
        }
    );
    return data;
};

// Define the custom hook using react-query
export const useMarketData = (
    newsCategory: string = "general",
    maxArticlesToProcess: number = 50
): UseQueryResult<MarketOutlookResponseData, Error> => {
    return useQuery<MarketOutlookResponseData, Error>(
        ['marketOutlook', newsCategory, maxArticlesToProcess], // Query key
        () => fetchMarketOutlook(newsCategory, maxArticlesToProcess),
        {
            // Add react-query options here if needed, e.g.,
            // staleTime: 15 * 60 * 1000, // 15 minutes
            // cacheTime: 60 * 60 * 1000, // 1 hour
            // refetchOnWindowFocus: false, // Consider if data should refresh on window focus
        }
    );
};
