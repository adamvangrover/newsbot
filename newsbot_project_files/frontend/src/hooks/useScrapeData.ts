import { useMutation, UseMutationResult } from 'react-query';
import apiClient from '../api/apiClient';
import { ScrapeURLRequestData, ScrapeAndAnalyzeResponseData } from '../types/toolsTypes';

// Define the function that will perform the mutation (POST request)
const postScrapeUrl = async (requestData: ScrapeURLRequestData): Promise<ScrapeAndAnalyzeResponseData> => {
    const { data } = await apiClient.post<ScrapeAndAnalyzeResponseData>(
        '/tools/scrape-and-analyze', // Endpoint path
        requestData // The body of the POST request
    );
    return data;
};

// Define the custom hook using useMutation
export const useScrapeData = (): UseMutationResult<
    ScrapeAndAnalyzeResponseData, // Type of data returned by the mutation
    Error,                        // Type of error
    ScrapeURLRequestData          // Type of variables passed to the mutate function
> => {
    return useMutation<ScrapeAndAnalyzeResponseData, Error, ScrapeURLRequestData>(
        postScrapeUrl,
        {
            // Optional: Add onSuccess, onError, onSettled callbacks here
            // onSuccess: (data) => {
            //   console.log('Scraping and analysis successful:', data);
            // },
            // onError: (error) => {
            //   console.error('Scraping and analysis error:', error);
            // },
        }
    );
};
