import type { IDataProvider, MarketData, AnalystRating, CorporateEarning, SocialSentiment } from './types';
import axios, { type AxiosInstance } from 'axios';

export class LiveProvider implements IDataProvider {
  private client: AxiosInstance;

  constructor(baseURL: string = 'http://localhost:8000', apiKey: string = '') {
    this.client = axios.create({
      baseURL,
      headers: {
        'X-API-Key': apiKey,
      },
    });
  }

  async getMarketData(ticker: string): Promise<MarketData[]> {
    try {
      const response = await this.client.get(`/api/v1/market-data/${ticker}`);
      return response.data;
    } catch (error) {
      console.error('Failed to fetch market data from backend', error);
      return [];
    }
  }

  async getAnalystRatings(ticker: string): Promise<AnalystRating[]> {
    try {
      const response = await this.client.get(`/api/v1/analyst-ratings/${ticker}`);
      return response.data;
    } catch (error) {
      console.error('Failed to fetch analyst ratings from backend', error);
      return [];
    }
  }

  async getCorporateEarnings(ticker: string): Promise<CorporateEarning[]> {
    try {
      const response = await this.client.get(`/api/v1/corporate-earnings/${ticker}`);
      return response.data;
    } catch (error) {
      console.error('Failed to fetch corporate earnings from backend', error);
      return [];
    }
  }

  async getSocialSentiment(ticker: string): Promise<SocialSentiment[]> {
    try {
        // Adjust endpoint as necessary based on actual backend implementation
      const response = await this.client.get(`/api/v1/sentiment/${ticker}`);
      return response.data;
    } catch (error) {
      console.error('Failed to fetch sentiment data from backend', error);
      return [];
    }
  }
}
