from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List, Union, Dict, Any
import datetime

# Finnhub Models
class CompanyProfileFinnhub(BaseModel):
    country: Optional[str] = None
    currency: Optional[str] = None
    exchange: Optional[str] = None
    ipo: Optional[datetime.date] = None
    marketCapitalization: Optional[float] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    shareOutstanding: Optional[float] = None
    ticker: str
    weburl: Optional[HttpUrl] = None
    logo: Optional[HttpUrl] = None
    finnhubIndustry: Optional[str] = None

class NewsArticleFinnhub(BaseModel):
    category: Optional[str] = None # This field seems to be from Finnhub directly
    datetime: int # Unix timestamp
    headline: str
    id: int
    image: Optional[HttpUrl] = None
    related: Optional[str] = None # Ticker related
    source: str
    summary: str
    url: HttpUrl

    @property
    def news_datetime(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self.datetime, tz=datetime.timezone.utc)

# Alpha Vantage Models
class StockDataPointAlphaVantage(BaseModel):
    date: datetime.date
    open: float
    high: float
    low: float
    close: float
    volume: int

class StockDataAlphaVantage(BaseModel):
    ticker: str
    prices: List[StockDataPointAlphaVantage]


# AI Processing Service Models
class SentimentOutput(BaseModel):
    label: str # e.g., "POSITIVE", "NEGATIVE", "NEUTRAL"
    score: Optional[float] = None # if available from model

class CategoryOutput(BaseModel):
    label: str # e.g., "Earnings", "Partnership", "General News"


# Consolidated API Response Models
class NewsItemWithInsight(NewsArticleFinnhub): # Inherits fields from NewsArticleFinnhub
    sentiment: Optional[SentimentOutput] = None
    # The 'category' field from NewsArticleFinnhub (if it exists directly from Finnhub)
    # might conflict or be different from our AI-generated category.
    # Renaming AI category for clarity if Finnhub provides its own 'category'.
    # For now, assuming NewsArticleFinnhub.category is Finnhub's own, and we add ours:
    ai_category: Optional[CategoryOutput] = None # Our AI-generated category

class CompanyAnalysisResponse(BaseModel):
    ticker: str
    profile: Optional[CompanyProfileFinnhub] = None
    news: List[NewsItemWithInsight] = []
    stock_data: Optional[StockDataAlphaVantage] = None
    retrieved_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    
    # Pydantic V2 uses model_config dict. V1 uses Config class.
    # FastAPI handles datetime serialization well by default for response_model.
    # Explicit encoders usually not needed for basic ISO format with recent FastAPI/Pydantic.
    # If specific formatting is needed, this is where it would go.
    # class Config:
    #     json_encoders = {
    #         datetime.datetime: lambda dt: dt.isoformat(),
    #         datetime.date: lambda d: d.isoformat(),
    #     }
    # For Pydantic V2, it might look like:
    # model_config = {
    #     "json_encoders": {
    #         datetime.datetime: lambda dt: dt.isoformat(),
    #         datetime.date: lambda d: d.isoformat(),
    #     }
    # }
