import { useQuery, UseQueryResult } from 'react-query';
import apiClient from '../api/apiClient';
import { PortfolioData } from '../types/portfolioTypes';

const fetchPortfolios = async (): Promise<PortfolioData[]> => {
  const { data } = await apiClient.get<PortfolioData[]>('/portfolios/');
  return data;
};

export const usePortfolios = (): UseQueryResult<PortfolioData[], Error> => {
  return useQuery<PortfolioData[], Error>(
    'portfolios',
    fetchPortfolios,
    {
      // Add react-query options here if needed
    }
  );
};
