from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import CompanyAnalysisResponse, NewsItemWithInsight, CategoryOutput, SentimentOutput
from app.services.data_aggregator_service import DataAggregatorService
from app.services.ai_processing_service import AIProcessingService
import datetime
from typing import List, Optional

router = APIRouter()

# Simple dependency injection
def get_data_service():
    return DataAggregatorService()

def get_ai_service():
    return AIProcessingService()

@router.post("/analyze/{ticker}", response_model=CompanyAnalysisResponse, tags=["analysis"])
async def analyze_company(
    ticker: str,
    data_service: DataAggregatorService = Depends(get_data_service),
    ai_service: AIProcessingService = Depends(get_ai_service)
):
    # 1. Get Company Profile
    profile = data_service.get_company_profile(ticker)

    # If profile is None, it might be an invalid ticker or API error.
    # For MVP, if we can't find the profile, we treat it as not found.
    if not profile:
        raise HTTPException(status_code=404, detail=f"Company profile not found for ticker {ticker}. Please check the ticker or API key configuration.")

    # 2. Get Stock Data (Optional, don't fail if missing)
    stock_data = data_service.get_stock_prices(ticker)

    # 3. Get News
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=7) # Last 7 days
    news = data_service.get_company_news(ticker, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))

    # 4. Analyze News
    analyzed_news: List[NewsItemWithInsight] = []

    # Limit to top 10 news items to save processing time/resources in this demo
    for article in news[:10]:
        text_to_analyze = f"{article.headline}. {article.summary}"

        sentiment = ai_service.get_sentiment(text_to_analyze)
        # Fallback if sentiment is None
        if not sentiment:
            sentiment = SentimentOutput(label="NEUTRAL", score=0.0)

        category = ai_service.get_category(text_to_analyze)

        # Construct NewsItemWithInsight
        # We need to manually copy fields or use dict unpacking
        # Note: 'category' field in NewsArticleFinnhub might clash with 'ai_category'
        analyzed_article = NewsItemWithInsight(
            **article.model_dump(),
            sentiment=sentiment,
            ai_category=category
        )
        analyzed_news.append(analyzed_article)

    return CompanyAnalysisResponse(
        ticker=ticker,
        profile=profile,
        news=analyzed_news,
        stock_data=stock_data
    )
