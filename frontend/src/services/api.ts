import axios from 'axios';

const API_BASE_URL = '/api/reasoning';

export interface NewsArticle {
  headline: string;
  source: string;
  timestamp: string;
  signal_strength: 'High Signal' | 'Noise' | 'Context';
}

export interface ImpactNode {
  id: string;
  name: string;
  val: number; // size
  group: number; // color code
}

export interface ImpactLink {
  source: string;
  target: string;
  type: string;
}

export interface ImpactGraphData {
  nodes: ImpactNode[];
  links: ImpactLink[];
}

export const analyzeNews = async (headline: string): Promise<any> => {
    // Determine signal strength using regex heuristics (mirroring backend for immediate feedback)
    // In a real app, this would call the backend.
    const response = await axios.post(`${API_BASE_URL}/analyze`, {
        article_id: 0,
        news_source_id: 1,
        headline: headline,
        publish_timestamp_utc: new Date().toISOString(),
        tickers_mentioned: [], // TODO: extract tickers
        ingestion_timestamp: new Date().toISOString()
    });
    return response.data;
};
