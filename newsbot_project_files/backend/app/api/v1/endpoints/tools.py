from fastapi import APIRouter, HTTPException, Depends, Body
from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict, Any

from newsbot_project_files.backend.app.services.web_scraping_service import WebScrapingService
from newsbot_project_files.backend.app.services.ai_processing_service import AIProcessingService
# Re-use NewsArticle schema parts for AI analysis results, or define a new one
from newsbot_project_files.backend.app.schemas.news import NewsArticle # For AI fields like sentiment, entities, etc.
from newsbot_project_files.backend.app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()

# --- Dependency Injection ---
def get_web_scraping_service():
    return WebScrapingService()

def get_ai_processing_service():
    return AIProcessingService()

# --- Request and Response Models ---
class ScrapeURLRequest(BaseModel):
    url: HttpUrl # Validate that it's a URL

class AIScrapedContentFeatures(BaseModel): # Subset of NewsArticle for AI results
    sentiment_label: Optional[str] = None
    sentiment_score: Optional[float] = None
    analyzed_category: Optional[str] = None # May not be as relevant for general web content
    ai_summary: Optional[str] = None
    entities: Optional[List[Dict[str, Any]]] = None
    detected_events: Optional[List[str]] = None # May not be as relevant

class ScrapeAndAnalyzeResponse(BaseModel):
    requested_url: HttpUrl
    page_title: Optional[str] = None
    scraped_text_snippet: Optional[str] = None # Show a part of the text
    full_text_char_count: Optional[int] = None
    ai_analysis: Optional[AIScrapedContentFeatures] = None
    error_message: Optional[str] = None

@router.post(
    "/scrape-and-analyze",
    response_model=ScrapeAndAnalyzeResponse,
    summary="Scrape text content from a URL and perform AI analysis.",
    description="Fetches text from a given URL, extracts main content, and then applies AI models for summarization, sentiment analysis, entity extraction, and event detection."
)
async def scrape_and_analyze_url(
    request: ScrapeURLRequest,
    scraper: WebScrapingService = Depends(get_web_scraping_service),
    ai_processor: AIProcessingService = Depends(get_ai_processing_service)
):
    logger.info(f"Received request to scrape and analyze URL: {request.url}")

    try:
        text_content, page_title, scrape_error = await scraper.scrape_article_text(str(request.url))

        if scrape_error or not text_content:
            logger.error(f"Scraping failed for {request.url}: {scrape_error}")
            return ScrapeAndAnalyzeResponse(
                requested_url=request.url,
                page_title=page_title,
                error_message=scrape_error or "Failed to extract text content or content was empty."
            )

        logger.info(f"Successfully scraped text from {request.url}. Title: '{page_title}'. Text length: {len(text_content)} chars.")

        # For AI processing, we can treat the scraped content like a single news article's body.
        # We need to construct a temporary structure that AIProcessingService can work with,
        # or adapt AIProcessingService if it's too coupled to NewsArticle schema.
        # For now, let's simulate a single "article" structure.
        # The AIProcessingService expects a list of NewsArticle objects.

        # Create a pseudo-NewsArticle for AI processing.
        # ID and other fields are not strictly necessary for the AI models themselves if they only operate on text.
        pseudo_article_for_ai = NewsArticle(
            id=str(request.url), # Use URL as ID
            headline=page_title or "Scraped Content",
            summary=text_content, # Pass full text as summary for analysis
            # Other fields like datetime, source, url can be set if meaningful
            datetime=0,
            source="WebScrape",
            url=request.url
        )

        processed_ai_results = await ai_processor.process_news_articles([pseudo_article_for_ai])

        ai_features = None
        if processed_ai_results and len(processed_ai_results) > 0:
            # Extract AI analysis from the (single) processed pseudo-article
            pa = processed_ai_results[0]
            ai_features = AIScrapedContentFeatures(
                sentiment_label=pa.sentiment_label,
                sentiment_score=pa.sentiment_score,
                analyzed_category=pa.analyzed_category, # This might be generic for web pages
                ai_summary=pa.ai_summary,
                entities=pa.entities,
                detected_events=pa.detected_events # Also might be less relevant
            )
            logger.info(f"AI analysis complete for {request.url}. Summary: {ai_features.ai_summary[:100] if ai_features.ai_summary else 'N/A'}...")
        else:
            logger.warning(f"AI processing did not return results for scraped content from {request.url}")


        return ScrapeAndAnalyzeResponse(
            requested_url=request.url,
            page_title=page_title,
            scraped_text_snippet=text_content[:1000] + "..." if text_content and len(text_content) > 1000 else text_content, # Max 1000 chars snippet
            full_text_char_count=len(text_content) if text_content else 0,
            ai_analysis=ai_features
        )

    except Exception as e:
        logger.error(f"Unexpected error during scrape and analyze for {request.url}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {str(e)}")

# Need to add this tools router to the main app
# In newsbot_project_files/backend/app/main.py:
# from newsbot_project_files.backend.app.api.v1.endpoints import tools as tools_v1
# app.include_router(tools_v1.router, prefix=f"{settings.API_V1_STR}/tools", tags=["Utility Tools"])
