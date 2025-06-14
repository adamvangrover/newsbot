from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict

class CompanyProfile(BaseModel):
    country: Optional[str] = None
    currency: Optional[str] = None
    exchange: Optional[str] = None
    name: Optional[str] = None
    ticker: str
    ipo: Optional[str] = None # IPO date
    marketCapitalization: Optional[float] = None
    shareOutstanding: Optional[float] = None
    logo: Optional[HttpUrl] = None
    phone: Optional[str] = None
    weburl: Optional[HttpUrl] = None
    finnhubIndustry: Optional[str] = None

class StockDataPoint(BaseModel):
    date: str # Could be date type after validation
    open: float
    high: float
    low: float
    close: float
    volume: int

class HistoricalStockData(BaseModel):
    ticker: str
    prices: List[StockDataPoint] = []
