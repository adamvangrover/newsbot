// Corresponds to backend/app/api/v1/endpoints/tools.py ScrapeURLRequest
export interface ScrapeURLRequestData {
    url: string;
}

// Corresponds to backend/app/api/v1/endpoints/tools.py AIScrapedContentFeatures
// Re-using EntityData from marketTypes for consistency
import { EntityData } from './marketTypes';

export interface AIScrapedContentFeaturesData {
    sentiment_label?: string | null;
    sentiment_score?: number | null;
    analyzed_category?: string | null;
    ai_summary?: string | null;
    entities?: EntityData[] | null;
    detected_events?: string[] | null;
}

// Corresponds to backend/app/api/v1/endpoints/tools.py ScrapeAndAnalyzeResponse
export interface ScrapeAndAnalyzeResponseData {
    requested_url: string;
    page_title?: string | null;
    scraped_text_snippet?: string | null;
    full_text_char_count?: number | null;
    ai_analysis?: AIScrapedContentFeaturesData | null;
    error_message?: string | null;
}
