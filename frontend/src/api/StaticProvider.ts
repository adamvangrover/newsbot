import type { IDataProvider, MarketData, AnalystRating, CorporateEarning, SocialSentiment } from './types';
import axios from 'axios';

export class StaticProvider implements IDataProvider {
  async getMarketData(ticker: string): Promise<MarketData[]> {
    const response = await axios.get('/data/market_data_1min.json');
    const data: MarketData[] = response.data;
    return data.filter(item => item.Ticker === ticker);
  }

  async getAnalystRatings(ticker: string): Promise<AnalystRating[]> {
    const response = await axios.get('/data/analyst_ratings.json');
    const data: AnalystRating[] = response.data;
    return data.filter(item => item.Ticker === ticker);
  }

  async getCorporateEarnings(ticker: string): Promise<CorporateEarning[]> {
    const response = await axios.get('/data/corporate_earnings.json');
    const data: CorporateEarning[] = response.data;
    return data.filter(item => item.Ticker === ticker);
  }

  async getSocialSentiment(ticker: string): Promise<SocialSentiment[]> {
    const response = await axios.get('/data/social_hourly_features.json');
    const data: SocialSentiment[] = response.data;
    return data.filter(item => item.Ticker === ticker);
  }
}
