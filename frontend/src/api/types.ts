export interface MarketData {
  Timestamp: string;
  Ticker: string;
  Open: number;
  High: number;
  Low: number;
  Close: number;
  Volume: number;
}

export interface AnalystRating {
  Rating_ID: string;
  Ticker: string;
  Timestamp: string;
  Analyst_Name: string;
  Brokerage_Name: string;
  Previous_Rating: string;
  New_Rating: string;
  Previous_Price_Target: number;
  New_Price_Target: number;
}

export interface CorporateEarning {
  Earning_ID: string;
  Ticker: string;
  Release_Timestamp: string;
  Fiscal_Quarter: string;
  EPS_Actual: number;
  EPS_Consensus: number;
  Revenue_Actual: number;
  Revenue_Consensus: number;
  Surprise_EPS: number;
  Surprise_Revenue_ZScore: number;
}

export interface SocialSentiment {
  Timestamp: string;
  Ticker: string;
  Social_Media_Volume: number;
  Social_Media_Velocity: string;
  Sentiment_Divergence: number;
}

export interface IDataProvider {
  getMarketData(ticker: string): Promise<MarketData[]>;
  getAnalystRatings(ticker: string): Promise<AnalystRating[]>;
  getCorporateEarnings(ticker: string): Promise<CorporateEarning[]>;
  getSocialSentiment(ticker: string): Promise<SocialSentiment[]>;
}
