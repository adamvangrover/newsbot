import requests
import functools
import logging
from typing import Optional, List, Dict, Any
from app.core.config import settings
from app.models.schemas import CompanyProfileFinnhub, NewsArticleFinnhub, StockDataAlphaVantage, StockDataPointAlphaVantage
import datetime

# Configure logging
logger = logging.getLogger(__name__)

class DataAggregatorService:
    FINNHUB_BASE_URL = "https://finnhub.io/api/v1"
    ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query" # Base for Alpha Vantage

    def __init__(self,
                 finnhub_api_key: str = settings.FINNHUB_API_KEY,
                 alpha_vantage_api_key: str = settings.ALPHA_VANTAGE_API_KEY):

        self.finnhub_api_key = finnhub_api_key
        self.alpha_vantage_api_key = alpha_vantage_api_key
        
        keys_missing_or_placeholder = False
        if not self.finnhub_api_key or self.finnhub_api_key == "YOUR_FINNHUB_KEY_HERE":
            logger.warning("FINNHUB_API_KEY not configured or is placeholder.")
            keys_missing_or_placeholder = True
            
        if not self.alpha_vantage_api_key or self.alpha_vantage_api_key == "YOUR_ALPHA_VANTAGE_KEY_HERE":
            logger.warning("ALPHA_VANTAGE_API_KEY not configured or is placeholder.")
            keys_missing_or_placeholder = True

        if keys_missing_or_placeholder:
            logger.critical("One or more API keys (Finnhub, Alpha Vantage) are missing or are placeholders. Service may not function correctly for relevant calls.")
            # Not raising an error here to allow partial service functionality if one key is set.
            # Methods should check their specific keys.

        self.session = requests.Session()

    @functools.lru_cache(maxsize=32)
    def get_company_profile(self, ticker: str) -> Optional[CompanyProfileFinnhub]:
        if not self.finnhub_api_key or self.finnhub_api_key == "YOUR_FINNHUB_KEY_HERE":
            logger.warning(f"Finnhub API key not configured. Returning MOCK profile for {ticker}.")
            # Return Mock Data
            return CompanyProfileFinnhub(
                country="US",
                currency="USD",
                exchange="NASDAQ",
                ipo=datetime.date(1980, 12, 12),
                marketCapitalization=3000000.0,
                name=f"{ticker} Inc.",
                phone="123-456-7890",
                shareOutstanding=16000.0,
                ticker=ticker,
                weburl="https://www.apple.com",
                logo="https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg",
                finnhubIndustry="Technology"
            )
        endpoint = f"{self.FINNHUB_BASE_URL}/stock/profile2"
        params = {"symbol": ticker, "token": self.finnhub_api_key}
        try:
            response = self.session.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            if not data:
                logger.info(f"No profile data found for ticker: {ticker} on Finnhub.")
                return None
            return CompanyProfileFinnhub(**data)
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error fetching Finnhub profile for {ticker}: {e.response.status_code} - {e.response.text}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error fetching Finnhub profile for {ticker}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error parsing Finnhub profile for {ticker}: {e}")
        return None

    @functools.lru_cache(maxsize=64)
    def get_company_news(self, ticker: str, start_date: str, end_date: str) -> List[NewsArticleFinnhub]:
        if not self.finnhub_api_key or self.finnhub_api_key == "YOUR_FINNHUB_KEY_HERE":
            logger.warning(f"Finnhub API key not configured. Returning MOCK news for {ticker}.")
            # Return Mock Data
            return [
                NewsArticleFinnhub(
                    category="technology",
                    datetime=int(datetime.datetime.now().timestamp()),
                    headline=f"{ticker} announces new product line",
                    id=12345,
                    image="https://via.placeholder.com/150",
                    related=ticker,
                    source="TechCrunch",
                    summary=f"In a recent event, {ticker} unveiled its latest innovation, promising to revolutionize the industry.",
                    url="https://techcrunch.com"
                ),
                NewsArticleFinnhub(
                    category="business",
                    datetime=int((datetime.datetime.now() - datetime.timedelta(days=1)).timestamp()),
                    headline=f"Analysts upgrade {ticker} stock",
                    id=12346,
                    image="https://via.placeholder.com/150",
                    related=ticker,
                    source="Bloomberg",
                    summary=f"Market analysts have revised their outlook for {ticker}, citing strong quarterly earnings.",
                    url="https://bloomberg.com"
                ),
                NewsArticleFinnhub(
                    category="business",
                    datetime=int((datetime.datetime.now() - datetime.timedelta(days=2)).timestamp()),
                    headline=f"{ticker} expands partnership",
                    id=12347,
                    image="https://via.placeholder.com/150",
                    related=ticker,
                    source="Reuters",
                    summary=f"{ticker} has signed a strategic partnership with a major logistics provider.",
                    url="https://reuters.com"
                )
            ]
        endpoint = f"{self.FINNHUB_BASE_URL}/company-news"
        params = {"symbol": ticker, "from": start_date, "to": end_date, "token": self.finnhub_api_key}
        try:
            response = self.session.get(endpoint, params=params, timeout=15)
            response.raise_for_status()
            news_data = response.json()
            if not isinstance(news_data, list):
                logger.warning(f"Finnhub news for {ticker} not in expected list format: {news_data}")
                return []
            articles = [NewsArticleFinnhub(**article) for article in news_data if isinstance(article, dict)]
            return articles
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error fetching Finnhub news for {ticker}: {e.response.status_code} - {e.response.text}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error fetching Finnhub news for {ticker}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error parsing Finnhub news for {ticker}: {e}")
        return []

    @functools.lru_cache(maxsize=32)
    def get_stock_prices(self, ticker: str, days: int = 30) -> Optional[StockDataAlphaVantage]:
        if not self.alpha_vantage_api_key or self.alpha_vantage_api_key == "YOUR_ALPHA_VANTAGE_KEY_HERE":
            logger.warning(f"Alpha Vantage API key not configured. Returning MOCK stock prices for {ticker}.")
            # Return Mock Data
            prices = []
            today = datetime.date.today()
            for i in range(days):
                date = today - datetime.timedelta(days=i)
                # Generate some random walk data
                base_price = 150.0 + (i * 0.5)
                prices.append(StockDataPointAlphaVantage(
                    date=date,
                    open=base_price,
                    high=base_price + 2.0,
                    low=base_price - 1.0,
                    close=base_price + 0.5,
                    volume=1000000 + (i * 1000)
                ))
            return StockDataAlphaVantage(ticker=ticker, prices=prices)
            
        endpoint = f"{self.ALPHA_VANTAGE_BASE_URL}" # Using the constant defined in class
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": ticker,
            "apikey": self.alpha_vantage_api_key,
            "outputsize": "compact" 
        }
        try:
            response = self.session.get(endpoint, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()

            if "Error Message" in data:
                logger.error(f"Alpha Vantage API error for {ticker}: {data['Error Message']}")
                return None
            if "Information" in data and "free trial" in data["Information"]: # Adjusted for common AV messages
                 logger.warning(f"Alpha Vantage API Information for {ticker}: {data['Information']}. This might be a demo call.")
                 # If it's a demo call, data might be fixed. Proceed with caution or return None.
                 # For now, let's try to parse it.
            if "Note" in data: 
                logger.warning(f"Alpha Vantage API note for {ticker}: {data['Note']}. (Often about API call frequency limits)")
                # This is a strong indicator that the call might not have real data or is rate-limited.
                # Consider returning None or specific error if this note appears.
                # For now, we will try to proceed but this is a risk.

            time_series = data.get("Time Series (Daily)")
            if not time_series:
                logger.warning(f"No 'Time Series (Daily)' data found for {ticker} from Alpha Vantage. Response: {data}")
                return None

            prices: List[StockDataPointAlphaVantage] = []
            sorted_dates = sorted(time_series.keys(), reverse=True)
            
            count = 0
            for date_str in sorted_dates:
                if count >= days:
                    break
                daily_data = time_series[date_str]
                try:
                    prices.append(StockDataPointAlphaVantage(
                        date=datetime.datetime.strptime(date_str, "%Y-%m-%d").date(),
                        open=float(daily_data["1. open"]),
                        high=float(daily_data["2. high"]),
                        low=float(daily_data["3. low"]),
                        close=float(daily_data["4. close"]),
                        volume=int(daily_data["5. volume"])
                    ))
                    count += 1
                except ValueError as ve:
                    logger.error(f"ValueError parsing Alpha Vantage data for {ticker} on {date_str}: {ve} - Data: {daily_data}")
                    continue 
                except KeyError as ke:
                    logger.error(f"KeyError parsing Alpha Vantage data for {ticker} on {date_str}: Missing key {ke} - Data: {daily_data}")
                    continue
            
            if not prices:
                logger.warning(f"No valid stock price data points processed for {ticker} from Alpha Vantage for the last {days} days.")
                return None

            return StockDataAlphaVantage(ticker=ticker, prices=prices)

        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error fetching Alpha Vantage stock prices for {ticker}: {e.response.status_code} - {e.response.text}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error fetching Alpha Vantage stock prices for {ticker}: {e}")
        except Exception as e: # Catch any other exceptions during parsing or processing
            logger.error(f"Unexpected error processing Alpha Vantage stock prices for {ticker}: {e}", exc_info=True)
        return None

# Example usage part (preserved from previous version, may need updates for Alpha Vantage)
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO)
#     try:
#         print("Attempting to initialize DataAggregatorService...")
#         service = DataAggregatorService()
#         print("Service initialized.")

#         ticker_symbol = "IBM" # Example: IBM (often used in AV examples)
#         print(f"Fetching company profile for {ticker_symbol}...")
#         profile = service.get_company_profile(ticker_symbol)
#         if profile:
#             print(f"Profile for {ticker_symbol}: {{'name': profile.name, 'ticker': profile.ticker, 'exchange': profile.exchange, 'finnhubIndustry': profile.finnhubIndustry}}")
#         else:
#             print(f"Could not fetch profile for {ticker_symbol}.")
        
#         end_dt = datetime.date.today()
#         start_dt = end_dt - datetime.timedelta(days=7)
#         start_date_str = start_dt.strftime("%Y-%m-%d")
#         end_date_str = end_dt.strftime("%Y-%m-%d")
        
#         print(f"Fetching company news for {ticker_symbol} from {start_date_str} to {end_date_str}...")
#         news_articles = service.get_company_news(ticker_symbol, start_date_str, end_date_str)
#         if news_articles:
#             print(f"Found {len(news_articles)} news articles for {ticker_symbol} (first 3):")
#             for article in news_articles[:3]:
#                 print(f"- Headline: {article.headline}, Source: {article.source}, Date: {article.news_datetime.strftime('%Y-%m-%d %H:%M')}")
#         else:
#             print(f"No news articles found for {ticker_symbol} in the last 7 days.")

#         print(f"Fetching stock prices for {ticker_symbol} for the last 5 days...")
#         stock_data = service.get_stock_prices(ticker_symbol, days=5)
#         if stock_data and stock_data.prices:
#             print(f"Found {len(stock_data.prices)} stock data points for {ticker_symbol}:")
#             for price_point in stock_data.prices:
#                 print(f"- Date: {price_point.date}, Close: {price_point.close}, Volume: {price_point.volume}")
#         else:
#             print(f"No stock data found for {ticker_symbol}.")

#     except ValueError as e: # This might catch API key configuration issues from __init__
#         print(f"Configuration or Value Error: {e}.")
#     except Exception as e:
#         print(f"An unexpected error occurred during example execution: {e}")
#         import traceback
#         traceback.print_exc()
