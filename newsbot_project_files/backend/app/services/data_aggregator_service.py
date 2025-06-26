import requests
from tenacity import retry, stop_after_attempt, wait_exponential, RetryError # Ensure RetryError is imported
from functools import lru_cache
from typing import Optional, List, Dict, Any


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

        if not self.finnhub_api_key or self.finnhub_api_key == "your_finnhub_api_key_here":
            logger.warning("Finnhub API key is not configured or is using a placeholder.")
        if not self.alpha_vantage_api_key or self.alpha_vantage_api_key == "your_alpha_vantage_api_key_here":
            logger.warning("Alpha Vantage API key is not configured or is using a placeholder.")

    @retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3), reraise=True)
    @lru_cache(maxsize=128)
    async def get_company_profile(self, ticker: str) -> Optional[CompanyProfile]:
        logger.debug(f"Attempting to fetch company profile for {ticker} from Finnhub.")
        if not self.finnhub_api_key or self.finnhub_api_key == "your_finnhub_api_key_here":
            logger.error(f"Finnhub API key missing. Cannot fetch profile for {ticker}.")
            return None # Explicitly return None if key is missing

        params = {"symbol": ticker, "token": self.finnhub_api_key}
        try:
            response = requests.get(f"{self.finnhub_base_url}/stock/profile2", params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if not data or not isinstance(data, dict) or not data.get('name'):
                logger.warning(f"No substantive profile data found for ticker: {ticker} from Finnhub. Response: {data}")
                return None


            if 'ticker' not in data or not data['ticker']:
                data['ticker'] = ticker

            profile = CompanyProfile(**data)
            logger.info(f"Successfully fetched profile for {ticker}: {profile.name}")
            return profile
        except requests.exceptions.HTTPError as http_err:
            # Log HTTP errors, but don't reraise them directly for tenacity if they are client errors (4xx)
            # that won't benefit from retries (like 401, 403, 404).
            # Server errors (5xx) might benefit. raise_for_status() handles this.
            # For tenacity, we want to retry on transient errors, usually RequestException.
            logger.error(f"HTTP error fetching profile for {ticker}: {http_err}. Status: {http_err.response.status_code}. Response: {http_err.response.text[:200]}")
            if http_err.response.status_code in [401, 403]:
                logger.error(f"Finnhub API key may be invalid or lacking permissions for {ticker}.")
            # For 404 or other 4xx, it's likely not a temporary issue, so returning None is appropriate.
            return None # Do not retry on client HTTP errors generally
        except requests.exceptions.RequestException as req_err: # Includes Timeout, ConnectionError etc. These should be retried.
            logger.warning(f"Request error fetching profile for {ticker} (attempt {req_err.retry.attempt_number if hasattr(req_err, 'retry') else 'N/A'}): {req_err}. Will retry if applicable.")
            raise # Reraise to allow tenacity to handle retries
        except Exception as e:

            logger.error(f"Unexpected error (e.g., JSON parsing, Pydantic validation) for profile {ticker}: {e}", exc_info=True)
            return None

    @retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3), reraise=True)
    @lru_cache(maxsize=128)
    async def get_company_news(self, ticker: str, start_date: str, end_date: str) -> List[NewsArticle]:
        logger.debug(f"Attempting to fetch company news for {ticker} from {start_date} to {end_date} from Finnhub.")
        if not self.finnhub_api_key or self.finnhub_api_key == "your_finnhub_api_key_here":
            logger.error(f"Finnhub API key missing. Cannot fetch news for {ticker}.")
            return []

        params = {"symbol": ticker, "from": start_date, "to": end_date, "token": self.finnhub_api_key}
        try:
            response = requests.get(f"{self.finnhub_base_url}/company-news", params=params, timeout=15)
            response.raise_for_status()
            news_data_list = response.json()

            if not isinstance(news_data_list, list):
                logger.warning(f"Finnhub news response for {ticker} was not a list: {type(news_data_list)}. Data: {str(news_data_list)[:200]}")
                return []

            articles: List[NewsArticle] = []
            for article_data in news_data_list:
                if not isinstance(article_data, dict):
                    logger.warning(f"Skipping non-dict item in news data for {ticker}: {str(article_data)[:100]}")
                    continue
                try:
                    fh_id = article_data.get('id')
                    article_url = article_data.get('url') # Keep url for potential use as ID
                    if fh_id is not None and fh_id != 0:
                        article_data['id'] = str(fh_id)
                    elif article_url: # Use URL as ID if actual ID is missing/zero
                         article_data['id'] = article_url
                    else:
                        logger.warning(f"Article for {ticker} has no usable 'id' (numeric and non-zero) or 'url'. Headline: {article_data.get('headline', 'N/A')[:50]}... Skipping.")
                        continue

                    if 'datetime' in article_data and not isinstance(article_data['datetime'], int):
                        try:
                            article_data['datetime'] = int(article_data['datetime'])
                        except (ValueError, TypeError) as ve:
                            logger.error(f"Could not convert datetime '{article_data.get('datetime')}' to int for article {article_data.get('id')}: {ve}")
                            continue # Skip this article if datetime is crucial and invalid

                    articles.append(NewsArticle(**article_data))
                except Exception as p_err:
                    logger.error(f"Error parsing article for {ticker} (ID: {article_data.get('id', 'N/A')} Headline: {article_data.get('headline', 'N/A')[:50]}...): {p_err}", exc_info=False)


            logger.info(f"Successfully fetched and parsed {len(articles)} news articles for {ticker} from Finnhub.")
            return articles
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error fetching news for {ticker}: {http_err}. Status: {http_err.response.status_code}. Response: {http_err.response.text[:200]}")
            if http_err.response.status_code in [401, 403]:
                logger.error(f"Finnhub API key may be invalid or lacking permissions for {ticker}.")
            return []
        except requests.exceptions.RequestException as req_err:
            logger.warning(f"Request error fetching news for {ticker} (attempt N/A): {req_err}. Will retry if applicable.") # Tenacity handles attempt numbers internally if reraised
            raise

        except Exception as e:
            logger.error(f"Unexpected error (e.g., JSON parsing, Pydantic validation) for news {ticker}: {e}", exc_info=True)
            return []

    @retry(wait=wait_exponential(multiplier=1, min=3, max=15), stop=stop_after_attempt(3), reraise=True)
    @lru_cache(maxsize=128)
    async def get_historical_stock_prices(self, ticker: str, outputsize: str = "compact") -> Optional[HistoricalStockData]:
        logger.debug(f"Attempting to fetch stock prices for {ticker} (output: {outputsize}) from Alpha Vantage.")
        if not self.alpha_vantage_api_key or self.alpha_vantage_api_key == "your_alpha_vantage_api_key_here":
            logger.error(f"Alpha Vantage API key missing. Cannot fetch stock prices for {ticker}.")
            return None

        params = {"function": "TIME_SERIES_DAILY_ADJUSTED", "symbol": ticker, "apikey": self.alpha_vantage_api_key, "outputsize": outputsize}
        try:
            response = requests.get(self.alpha_vantage_base_url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()

            if "Error Message" in data:
                logger.error(f"Alpha Vantage API error for {ticker}: {data['Error Message']}")
                return None # Specific error from AV, no retry needed.
            if "Information" in data and "Time Series (Daily)" not in data :

                logger.warning(f"Alpha Vantage API info for {ticker} (and no data returned): {data['Information']}")
                # This could be a rate limit message, which tenacity might help with if it leads to a RequestException on retry.
                # If it's a permanent issue for this ticker, returning None is correct.
                return None


            time_series_key = "Time Series (Daily)"
            if time_series_key not in data or not isinstance(data[time_series_key], dict):
                logger.warning(f"No '{time_series_key}' data or incorrect format for {ticker} in Alpha Vantage response. Note: {data.get('Note', 'No specific note found.')}")
                return None

            daily_data = data[time_series_key]
            prices: List[StockDataPoint] = []
            for date_str, values_dict in daily_data.items():
                try:
                    price_point = StockDataPoint(
                        date=date_str,
                        open=float(values_dict["1. open"]),
                        high=float(values_dict["2. high"]),
                        low=float(values_dict["3. low"]),
                        close=float(values_dict["4. close"]),
                        volume=int(values_dict["6. volume"])
                    )
                    prices.append(price_point)
                except (KeyError, ValueError, TypeError) as val_err:
                    logger.error(f"Error parsing stock data point for {ticker} on date {date_str}: {val_err}. Data: {values_dict}", exc_info=False)
                    # Continue to try parsing other dates

            if not prices:
                logger.warning(f"No valid stock price points parsed for {ticker} from Alpha Vantage data. Initial data had {len(daily_data)} entries.")
                return None

            prices.reverse() # Ensure chronological order

            logger.info(f"Successfully fetched and parsed {len(prices)} stock data points for {ticker} from Alpha Vantage.")
            return HistoricalStockData(ticker=ticker, prices=prices)

        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error fetching stock prices for {ticker} from Alpha Vantage: {http_err}. Status: {http_err.response.status_code}. Response: {http_err.response.text[:200]}")
            if http_err.response.status_code in [401, 403]:
                logger.error(f"Alpha Vantage API key may be invalid for {ticker}.")
            # Specific Alpha Vantage rate limit response might be a JSON with "Information" field,
            # which is handled above. If it's a plain HTTP error like 429, this will catch it.
            # 5xx errors should be retried by tenacity if this exception is reraised.
            # For now, return None on HTTP errors that are not RequestException.
            return None
        except requests.exceptions.RequestException as req_err:
            logger.warning(f"Request error fetching stock prices for {ticker} (attempt N/A): {req_err}. Will retry if applicable.")
            raise # Reraise for tenacity
        except Exception as e:
            logger.error(f"Unexpected error (e.g., JSON parsing, Pydantic validation) for stock prices {ticker}: {e}", exc_info=True)
            return None

    @retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3), reraise=True)
    @lru_cache(maxsize=32) # Cache general news for a while; smaller cache size than per-ticker
    async def get_general_market_news(self, category: str = "general", min_id: Optional[int] = None) -> List[NewsArticle]:
        """
        Fetches general market news from Finnhub.
        :param category: News category (e.g., 'general', 'forex', 'crypto', 'merger').
        :param min_id: (Optional) Use this to get news after a certain ID (for pagination/updates). Finnhub specific.
        """
        logger.debug(f"Attempting to fetch general market news for category '{category}' from Finnhub.")
        if not self.finnhub_api_key or self.finnhub_api_key == "your_finnhub_api_key_here":
            logger.error(f"Finnhub API key missing. Cannot fetch general market news for category '{category}'.")
            return []

        params = {"category": category, "token": self.finnhub_api_key}
        if min_id is not None:
            params["minId"] = min_id

        try:
            response = requests.get(f"{self.finnhub_base_url}/news", params=params, timeout=15)
            response.raise_for_status()
            news_data_list = response.json()

            if not isinstance(news_data_list, list):
                logger.warning(f"Finnhub general news response for category '{category}' was not a list: {type(news_data_list)}. Data: {str(news_data_list)[:200]}")
                return []

            articles: List[NewsArticle] = []
            for article_data in news_data_list:
                if not isinstance(article_data, dict):
                    logger.warning(f"Skipping non-dict item in general news data for category '{category}': {str(article_data)[:100]}")
                    continue
                try:
                    # Adapt ID handling similar to get_company_news
                    fh_id = article_data.get('id')
                    article_url = article_data.get('url')
                    if fh_id is not None and fh_id != 0:
                        article_data['id'] = str(fh_id)
                    elif article_url:
                         article_data['id'] = article_url
                    else:
                        logger.warning(f"General news article for category '{category}' has no usable 'id' or 'url'. Headline: {article_data.get('headline', 'N/A')[:50]}... Skipping.")
                        continue

                    if 'datetime' in article_data and not isinstance(article_data['datetime'], int):
                        try:
                            article_data['datetime'] = int(article_data['datetime'])
                        except (ValueError, TypeError) as ve:
                            logger.error(f"Could not convert datetime '{article_data.get('datetime')}' to int for general news article {article_data.get('id')}: {ve}")
                            continue

                    # 'related' field might be empty or different for general news, Pydantic model handles Optional
                    articles.append(NewsArticle(**article_data))
                except Exception as p_err: # PydanticValidationError or other
                    logger.error(f"Error parsing general news article for category '{category}' (ID: {article_data.get('id', 'N/A')} Headline: {article_data.get('headline', 'N/A')[:50]}...): {p_err}", exc_info=False)

            logger.info(f"Successfully fetched and parsed {len(articles)} general news articles for category '{category}' from Finnhub.")
            return articles
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error fetching general news for category '{category}': {http_err}. Status: {http_err.response.status_code}. Response: {http_err.response.text[:200]}")
            if http_err.response.status_code in [401, 403]:
                logger.error(f"Finnhub API key may be invalid or lacking permissions for general news category '{category}'.")
            return [] # Do not retry on client HTTP errors generally
        except requests.exceptions.RequestException as req_err:
            logger.warning(f"Request error fetching general news for category '{category}': {req_err}. Will retry if applicable.")
            raise # Reraise to allow tenacity to handle retries
        except Exception as e:
            logger.error(f"Unexpected error (e.g., JSON parsing, Pydantic validation) for general news category '{category}': {e}", exc_info=True)
            return []
