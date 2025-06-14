from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel
import requests
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta

from newsbot_project_files.backend.app.schemas.company import CompanyProfile, HistoricalStockData
from newsbot_project_files.backend.app.schemas.news import CompanyNews, NewsArticle
from newsbot_project_files.backend.app.services.data_aggregator_service import DataAggregatorService
from newsbot_project_files.backend.app.services.ai_processing_service import AIProcessingService
from newsbot_project_files.backend.app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()

# --- Dependency Injection for Services ---
def get_data_aggregator_service():
    return DataAggregatorService()

def get_ai_processing_service():
    return AIProcessingService()

# --- Combined Response Model ---
class CompanyAnalysisResponse(BaseModel):
    ticker: str
    profile: Optional[CompanyProfile] = None
    news: Optional[CompanyNews] = None
    stock_data: Optional[HistoricalStockData] = None
    # You could add more fields here like overall sentiment, key themes, etc.

@router.get(
    "/company-analysis/{ticker_symbol}",
    response_model=CompanyAnalysisResponse,
    summary="Get comprehensive analysis for a company",
    description="Fetches company profile, news, basic stock data, and AI-powered insights."
)
async def get_company_analysis(
    ticker_symbol: str,
    news_days_ago: int = Query(7, ge=1, le=30, description="How many days of news to fetch, max 30."),
    data_aggregator: DataAggregatorService = Depends(get_data_aggregator_service),
    ai_processor: AIProcessingService = Depends(get_ai_processing_service)
):
    logger.info(f"Starting company analysis for ticker: {ticker_symbol}, news days: {news_days_ago}")

    # Validate ticker symbol (basic validation)
    if not ticker_symbol or not ticker_symbol.isalnum(): # Basic check, can be improved
        logger.error(f"Invalid ticker symbol format: {ticker_symbol}")
        raise HTTPException(status_code=400, detail="Invalid ticker symbol format. Use alphanumeric characters.")

    try:
        # 1. Fetch Company Profile
        profile = await data_aggregator.get_company_profile(ticker_symbol)
        if not profile:
            logger.warning(f"No profile found for ticker: {ticker_symbol}. Analysis may be limited.")
            # Depending on strictness, you might raise HTTPException here or proceed
            # raise HTTPException(status_code=404, detail=f"Company profile not found for ticker: {ticker_symbol}")

        # 2. Fetch Company News
        end_date = datetime.now()
        start_date = end_date - timedelta(days=news_days_ago)
        news_articles_raw = await data_aggregator.get_company_news(
            ticker_symbol,
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d")
        )

        # 3. Process News with AI
        processed_news_articles = await ai_processor.process_news_articles(news_articles_raw)
        company_news = CompanyNews(ticker=ticker_symbol, articles=processed_news_articles)

        # 4. Fetch Historical Stock Prices
        stock_data = await data_aggregator.get_historical_stock_prices(ticker_symbol)

        logger.info(f"Successfully completed analysis for ticker: {ticker_symbol}")
        return CompanyAnalysisResponse(
            ticker=ticker_symbol,
            profile=profile,
            news=company_news,
            stock_data=stock_data
        )

    except HTTPException as http_exc:
        # Re-raise HTTPException to let FastAPI handle it
        raise http_exc
    except requests.exceptions.RequestException as req_exc: # Catch HTTP errors from requests library
        logger.error(f"API request error during analysis for {ticker_symbol}: {req_exc}", exc_info=True)
        raise HTTPException(status_code=503, detail=f"External API service unavailable: {req_exc}")
    except Exception as e:
        logger.error(f"An unexpected error occurred during analysis for {ticker_symbol}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {e}")

# Add a simple health check endpoint for the API itself
@router.get("/health", tags=["Health Check"])
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Note: The 'schemas.py' mentioned in the original prompt was split into
# 'company.py' and 'news.py' in the 'backend/app/schemas/' directory during Phase 1.
# Pydantic models are imported from these files.
# The endpoint was 'news_analysis.py' but changed to 'company.py' as per structure.
# Added CompanyAnalysisResponse model directly in this file for simplicity for now,
# but it could also be moved to a schemas file if it grows more complex.

# Need to import BaseModel from Pydantic for CompanyAnalysisResponse
# and requests for the exception handling
# sed -i '1 a from pydantic import BaseModel' newsbot_project_files/backend/app/api/v1/endpoints/company.py
# sed -i '2 a import requests' newsbot_project_files/backend/app/api/v1/endpoints/company.py
