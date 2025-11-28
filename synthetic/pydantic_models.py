from typing import List, Optional
from pydantic import BaseModel
from datetime import date, datetime

class AssetUniverse(BaseModel):
    universe_id: int
    universe_name: str
    description: Optional[str] = None

class Asset(BaseModel):
    asset_id: int
    ticker_symbol: str
    company_name: Optional[str] = None
    asset_class: str = "Equity"
    exchange: Optional[str] = None
    first_seen_date: Optional[date] = None
    last_seen_date: Optional[date] = None

class AssetConstituent(BaseModel):
    constituent_id: int
    universe_id: int
    asset_id: int
    start_date: date
    end_date: Optional[date] = None
    ingestion_timestamp: datetime
    source: Optional[str] = None

class EquityDailyPrice(BaseModel):
    asset_id: int
    ticker_symbol: str # Added for convenience in generation, not in SQL PK
    trade_date: date
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    adjusted_close_price: float
    volume: int
    vwap: Optional[float] = None
    ingestion_timestamp: datetime
    source: Optional[str] = None

class NewsSource(BaseModel):
    news_source_id: int
    source_name: str
    website: Optional[str] = None

class NewsArticleMetadata(BaseModel):
    article_id: int
    news_source_id: Optional[int] = None
    article_url: Optional[str] = None
    headline: str
    publish_timestamp_utc: datetime
    tickers_mentioned: Optional[List[str]] = None
    raw_text_s3_path: Optional[str] = None
    ingestion_timestamp: datetime
    source_api: Optional[str] = None
    # derived/helper fields
    sentiment_score: float = 0.0

class SECFilingType(BaseModel):
    filing_type_id: int
    form_type: str
    description: Optional[str] = None

class SECFilingMetadata(BaseModel):
    filing_id: int
    asset_id: Optional[int] = None
    ticker_symbol: Optional[str] = None # Helper
    cik: Optional[str] = None
    filing_type_id: int
    filing_date: date
    period_of_report: Optional[date] = None
    accession_number: Optional[str] = None
    raw_text_s3_path: Optional[str] = None
    structured_json_s3_path: Optional[str] = None
    ingestion_timestamp: datetime
    source: Optional[str] = None

class EconomicEventType(BaseModel):
    event_type_id: int
    event_name: str
    country_region: Optional[str] = None
    release_frequency: Optional[str] = None
    description: Optional[str] = None
    source_identifier: Optional[str] = None

class EconomicEvent(BaseModel):
    event_id: int
    event_type_id: int
    release_datetime_utc: datetime
    period_covered: Optional[str] = None
    actual_value: Optional[float] = None
    consensus_value_pit: Optional[float] = None
    previous_value: Optional[float] = None
    revised_previous_value: Optional[float] = None
    unit: Optional[str] = None
    notes: Optional[str] = None
    ingestion_timestamp: datetime
    source: Optional[str] = None
