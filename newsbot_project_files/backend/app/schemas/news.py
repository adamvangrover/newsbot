from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime # Finnhub uses unixtimestamp

class NewsArticle(BaseModel):
    id: str # Finnhub uses a string id
    category: Optional[str] = None # e.g., 'company news', 'technology'
    datetime: int # Unix timestamp
    headline: str
    image: Optional[HttpUrl] = None
    related: Optional[str] = None # Ticker or symbol
    source: str
    summary: str
    url: HttpUrl

    # AI Processed fields
    sentiment_label: Optional[str] = None # e.g., 'positive', 'negative', 'neutral'
    sentiment_score: Optional[float] = None
    analyzed_category: Optional[str] = None # e.g., 'Financial Performance', 'Product Launch'
    ai_summary: Optional[str] = None # Summary generated by AI

class CompanyNews(BaseModel):
    ticker: str
    articles: List[NewsArticle] = []
