from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

from newsbot_project_files.backend.app.schemas.news import NewsArticle # Reusing NewsArticle for processed market news
from newsbot_project_files.backend.app.services.data_aggregator_service import DataAggregatorService
from newsbot_project_files.backend.app.services.ai_processing_service import AIProcessingService
from newsbot_project_files.backend.app.core.logging import get_logger
from collections import Counter

logger = get_logger(__name__)
router = APIRouter()

# --- Dependency Injection for Services ---
def get_data_aggregator_service():
    return DataAggregatorService()

def get_ai_processing_service():
    return AIProcessingService()

# --- Response Models ---
class MarketSentiment(BaseModel):
    overall_sentiment_label: str
    average_sentiment_score: Optional[float] = None
    positive_articles: int
    negative_articles: int
    neutral_articles: int

class MarketOutlookResponse(BaseModel):
    timestamp: datetime
    market_news_category: str
    market_sentiment: Optional[MarketSentiment] = None
    topics: Optional[Dict[str, Any]] = None # Replaces key_themes
    highlighted_events: List[str] = []
    processed_articles: List[NewsArticle] = []

@router.get(
    "/outlook",
    response_model=MarketOutlookResponse,
    summary="Get a general market outlook",
    description="Fetches general market news, analyzes it, and provides a synthesized outlook including sentiment, topic modeling, and highlighted articles."
)
async def get_market_outlook(
    news_category: str = Query("general", description="Category of general news to fetch (e.g., 'general', 'forex', 'crypto')."),
    max_articles_to_process: int = Query(50, ge=10, le=100, description="Max number of raw news articles to fetch and process for the outlook."),
    data_aggregator: DataAggregatorService = Depends(get_data_aggregator_service),
    ai_processor: AIProcessingService = Depends(get_ai_processing_service)
):
    logger.info(f"Starting market outlook generation for category: {news_category}")

    try:
        raw_market_news = await data_aggregator.get_general_market_news(category=news_category)

        if not raw_market_news:
            logger.warning(f"No general market news found for category: {news_category}")
            return MarketOutlookResponse(
                timestamp=datetime.now(),
                market_news_category=news_category,
                processed_articles=[],
                market_sentiment=MarketSentiment(overall_sentiment_label="Unavailable", positive_articles=0, negative_articles=0, neutral_articles=0)
            )

        articles_to_process = raw_market_news[:max_articles_to_process]
        logger.info(f"Fetched {len(raw_market_news)} raw articles, processing {len(articles_to_process)} for market outlook.")

        # 2. Process News with AI (now returns a dict)
        ai_results = await ai_processor.process_news_articles(articles_to_process)
        processed_articles = ai_results.get("articles", [])
        main_topics = ai_results.get("topics")

        # 3. Synthesize Market Summary
        positive_count, negative_count, neutral_count = 0, 0, 0
        total_sentiment_score = 0
        valid_sentiment_articles = 0

        for article in processed_articles:
            if article.sentiment_label:
                if article.sentiment_label.upper() == "POSITIVE":
                    positive_count += 1
                elif article.sentiment_label.upper() == "NEGATIVE":
                    negative_count += 1
                else:
                    neutral_count += 1
            if article.sentiment_score is not None and article.sentiment_label and "ERROR" not in article.sentiment_label.upper() and "UNAVAILABLE" not in article.sentiment_label.upper():
                total_sentiment_score += article.sentiment_score
                valid_sentiment_articles += 1

        avg_sentiment_score = None
        overall_label = "Neutral"
        if valid_sentiment_articles > 0:
            avg_sentiment_score = round(total_sentiment_score / valid_sentiment_articles, 4)
            if avg_sentiment_score > 0.15:
                overall_label = "Positive"
            elif avg_sentiment_score < -0.15:
                overall_label = "Negative"
        elif positive_count > negative_count:
            overall_label = "Slightly Positive"
        elif negative_count > positive_count:
            overall_label = "Slightly Negative"

        market_sentiment_obj = MarketSentiment(
            overall_sentiment_label=overall_label,
            average_sentiment_score=avg_sentiment_score,
            positive_articles=positive_count,
            negative_articles=negative_count,
            neutral_articles=neutral_count
        )

        # Highlighted Events
        highlighted_events_list = []
        for article in processed_articles:
            if article.detected_events:
                for event in article.detected_events:
                    event_detail = f"{event}: {article.headline[:60]}..."
                    if event_detail not in highlighted_events_list:
                         highlighted_events_list.append(event_detail)
        highlighted_events_list = highlighted_events_list[:5]

        logger.info(f"Successfully generated market outlook for category: {news_category}")
        return MarketOutlookResponse(
            timestamp=datetime.now(),
            market_news_category=news_category,
            market_sentiment=market_sentiment_obj,
            topics=main_topics,
            highlighted_events=highlighted_events_list,
            processed_articles=processed_articles
        )

    except Exception as e:
        logger.error(f"An unexpected error occurred during market outlook generation for {news_category}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {str(e)}")

# Placeholder for a more advanced summary text generation if needed later
# async def generate_market_summary_text(processed_articles: List[NewsArticle], market_sentiment: MarketSentiment) -> str:
#     # This could involve sending key headlines or summaries to another LLM call for a narrative summary
#     # For MVP, we are using structured data (sentiment, themes, events)
#     return "Market summary text generation not yet implemented."
