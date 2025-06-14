# Placeholder for Data Aggregation Service
# This service will fetch data from Finnhub, Alpha Vantage, etc.

import requests
from tenacity import retry, stop_after_attempt, wait_exponential
from functools import lru_cache
from typing import Optional, List, Dict

from newsbot_project_files.backend.app.core.config import settings
from newsbot_project_files.backend.app.schemas.company import CompanyProfile, HistoricalStockData, StockDataPoint
from newsbot_project_files.backend.app.schemas.news import NewsArticle
from newsbot_project_files.backend.app.core.logging import get_logger

logger = get_logger(__name__)

class DataAggregatorService:

    def __init__(self):
        self.finnhub_api_key = settings.FINNHUB_API_KEY
        self.alpha_vantage_api_key = settings.ALPHA_VANTAGE_API_KEY
        self.finnhub_base_url = "https://finnhub.io/api/v1"
        self.alpha_vantage_base_url = "https://www.alphavantage.co/query"

    @retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
    @lru_cache(maxsize=128)
    async def get_company_profile(self, ticker: str) -> Optional[CompanyProfile]:
        logger.info(f"Fetching company profile for {ticker} from Finnhub.")
        # Placeholder - actual implementation needed
        # params = {"symbol": ticker, "token": self.finnhub_api_key}
        # response = requests.get(f"{self.finnhub_base_url}/stock/profile2", params=params)
        # response.raise_for_status() # Raise HTTPError for bad responses (4XX or 5XX)
        # data = response.json()
        # if not data: # Finnhub returns empty dict if symbol not found
        #     logger.warning(f"No profile data found for ticker: {ticker}")
        #     return None
        # return CompanyProfile(**data, ticker=ticker) # ticker might not be in response, ensure it's set
        logger.warning(f"DataAggregatorService.get_company_profile for {ticker} is a placeholder.")
        return CompanyProfile(ticker=ticker, name=f"{ticker} Name Placeholder", finnhubIndustry="Tech Placeholder")


    @retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
    @lru_cache(maxsize=128)
    async def get_company_news(self, ticker: str, start_date: str, end_date: str) -> List[NewsArticle]:
        logger.info(f"Fetching company news for {ticker} from {start_date} to {end_date} from Finnhub.")
        # Placeholder - actual implementation needed
        # params = {
        #     "symbol": ticker,
        #     "from": start_date, # YYYY-MM-DD
        #     "to": end_date,     # YYYY-MM-DD
        #     "token": self.finnhub_api_key
        # }
        # response = requests.get(f"{self.finnhub_base_url}/company-news", params=params)
        # response.raise_for_status()
        # news_data = response.json()
        # articles = [NewsArticle(**article, id=str(article.get('id', article.get('url')))) for article in news_data] # Ensure ID is string
        # return articles
        logger.warning(f"DataAggregatorService.get_company_news for {ticker} is a placeholder.")
        # Return dummy data that matches NewsArticle schema
        dummy_articles = [
            NewsArticle(id="1", headline="Headline 1", datetime=1672531200, source="Source A", summary="Summary 1", url="http://example.com/news1", related=ticker),
            NewsArticle(id="2", headline="Headline 2", datetime=1672617600, source="Source B", summary="Summary 2", url="http://example.com/news2", related=ticker),
        ]
        return dummy_articles


    @retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
    @lru_cache(maxsize=128)
    async def get_historical_stock_prices(self, ticker: str) -> Optional[HistoricalStockData]:
        logger.info(f"Fetching historical stock prices for {ticker} from Alpha Vantage.")
        # Placeholder - actual implementation needed
        # params = {
        #     "function": "TIME_SERIES_DAILY_ADJUSTED",
        #     "symbol": ticker,
        #     "apikey": self.alpha_vantage_api_key,
        #     "outputsize": "compact" # 'compact' for last 100 days, 'full' for full history
        # }
        # response = requests.get(self.alpha_vantage_base_url, params=params)
        # response.raise_for_status()
        # data = response.json()
        # time_series_key = "Time Series (Daily)"
        # if time_series_key not in data:
        #     logger.warning(f"No historical stock data found for {ticker}: {data.get('Information', data.get('Note', 'Unknown error'))}")
        #     return None
        #
        # prices = []
        # for date_str, values in data[time_series_key].items():
        #     prices.append(StockDataPoint(
        #         date=date_str,
        #         open=float(values["1. open"]),
        #         high=float(values["2. high"]),
        #         low=float(values["3. low"]),
        #         close=float(values["4. close"]),
        #         volume=int(values["6. volume"]) # "5. adjusted close", "6. volume"
        #     ))
        # return HistoricalStockData(ticker=ticker, prices=prices)
        logger.warning(f"DataAggregatorService.get_historical_stock_prices for {ticker} is a placeholder.")
        dummy_prices = [
            StockDataPoint(date="2023-01-01", open=100.0, high=102.0, low=99.0, close=101.0, volume=10000),
            StockDataPoint(date="2023-01-02", open=101.0, high=103.0, low=100.0, close=102.0, volume=12000),
        ]
        return HistoricalStockData(ticker=ticker, prices=dummy_prices)

# Example usage (for testing service logic directly if needed)
# async def main():
#     service = DataAggregatorService()
#     profile = await service.get_company_profile("AAPL")
#     if profile:
#         print(profile.json(indent=2))
#
#     news = await service.get_company_news("AAPL", "2023-01-01", "2023-01-05")
#     for article in news:
#         print(article.json(indent=2))
#
#     stock_data = await service.get_historical_stock_prices("AAPL")
#     if stock_data:
#         print(stock_data.json(indent=2))
#
# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main())
