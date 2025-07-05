import datetime
import json
import logging
import os
import random # Add this import
import time
from pathlib import Path
from typing import Callable, Any, List, Dict

# Assuming mock_data_generator is in a reachable path (e.g., PYTHONPATH or same parent dir)
from utils.mock_data_generator import get_utc_now

# --- Configuration ---
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

# Base directory for storing mock raw data, mirroring S3 structure
# This should be created in your project root if it doesn't exist.
MOCK_DATA_LAKE_BASE_DIR = Path(__file__).resolve().parent.parent / "mock_s3_data_lake" / "raw_data"

# --- Core Ingestion Logic ---

def ensure_dir(path: Path) -> None:
    """Ensure directory exists."""
    path.mkdir(parents=True, exist_ok=True)

def save_raw_data(data: Any, base_path: Path, file_name_prefix: str, partition_date: datetime.date = None) -> Path:
    """
    Saves raw data to a file, simulating immutable storage in a data lake.
    Data is typically saved as JSON.
    Includes an ingestion timestamp in the filename or metadata.
    """
    ingestion_ts_str = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f')[:-3] # YYYYMMDDHHMMSSsss

    if partition_date:
        # Example: base_path / YYYY / MM / DD / file_name_prefix_timestamp.json
        # This matches the S3 structure outlined previously for some data types.
        # More complex partitioning (e.g., by ticker) would be added here if needed.
        final_path = base_path / str(partition_date.year) / f"{partition_date.month:02d}" / f"{partition_date.day:02d}"
    else:
        # Example: base_path / YYYYMMDD / file_name_prefix_timestamp.json (ingestion date partitioning)
        today = datetime.date.today()
        final_path = base_path / today.strftime('%Y%m%d')

    ensure_dir(final_path)

    file_name = f"{file_name_prefix}_{ingestion_ts_str}.json"
    file_path = final_path / file_name

    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        logging.info(f"Successfully saved raw data to {file_path}")
        return file_path
    except Exception as e:
        logging.error(f"Failed to save raw data to {file_path}: {e}")
        return None

class MockApiFetcher:
    """
    Simulates fetching data from a vendor API.
    In a real scenario, this would involve HTTP requests, authentication, etc.
    Here, it uses a data generation function.
    """
    def __init__(self, api_name: str, data_generator_func: Callable[..., List[Dict[str, Any]]]):
        self.api_name = api_name
        self.data_generator_func = data_generator_func
        self.request_count = 0
        self.max_requests_per_run = random.randint(2,5) # Simulate API limits or batching

    def fetch_data(self, *args, **kwargs) -> List[Dict[str, Any]]:
        """
        Simulates an API call.
        *args and **kwargs are passed to the underlying data_generator_func.
        """
        logging.info(f"[{self.api_name}] Simulating API call with params: args={args}, kwargs={kwargs}")

        # Simulate API call delay
        time.sleep(random.uniform(0.1, 0.5))

        self.request_count += 1
        if self.request_count > self.max_requests_per_run:
            logging.warning(f"[{self.api_name}] Mock API call limit reached for this run.")
            return [] # Simulate no more data or rate limit hit

        try:
            data = self.data_generator_func(*args, **kwargs)
            logging.info(f"[{self.api_name}] Successfully fetched {len(data)} mock records.")

            # Add ingestion metadata to each record (simulating what a real framework might do)
            for record in data:
                record["_ingestion_details"] = {
                    "ingested_at_utc": get_utc_now(),
                    "source_api_simulation": self.api_name,
                    "original_params": {"args": args, "kwargs": kwargs}
                }
            return data
        except Exception as e:
            logging.error(f"[{self.api_name}] Error generating mock data: {e}")
            return []


# --- Generic Ingestion Job Runner ---

def run_ingestion_job(
    job_name: str,
    fetcher: MockApiFetcher,
    data_category_path: str, # e.g., "market_data/polygon_io_mock/equities_daily_bars"
    file_name_prefix: str,
    fetch_params: dict = None,
    partition_data_by_event_date: bool = False, # If true, use 'trade_date' or 'publish_timestamp_utc' from data for partitioning
    event_date_field: str = None # field in the data that contains the event date e.g. 'trade_date'
  ):
    """
    A generic function to run an ingestion job.
    1. Fetches data using the provided fetcher.
    2. Saves it to the mock data lake.
    """
    logging.info(f"Starting ingestion job: {job_name}")
    if fetch_params is None:
        fetch_params = {}

    # Fetch data
    raw_data_list = fetcher.fetch_data(**fetch_params)

    if not raw_data_list:
        logging.warning(f"[{job_name}] No data fetched or generated. Skipping save.")
        return

    # Determine base path for saving
    # e.g., MOCK_DATA_LAKE_BASE_DIR / market_data / polygon_io_mock / equities_daily_bars
    target_base_path = MOCK_DATA_LAKE_BASE_DIR / data_category_path
    ensure_dir(target_base_path)

    # Save data
    # In this mock setup, we'll save the whole list as one file.
    # A real scenario might save individual records or smaller batches,
    # and partitioning could be more granular (e.g., by ticker within a date).

    # For partitioning by event date, we assume all items in raw_data_list share the same event date
    # or we'd need to group them. For this mock, let's assume the first item's date if applicable.
    partition_date_to_use = None
    if partition_data_by_event_date and event_date_field and raw_data_list:
        date_str = raw_data_list[0].get(event_date_field)
        if date_str:
            try:
                # Handles both date and datetime strings
                if 'T' in date_str:
                    partition_date_to_use = datetime.datetime.fromisoformat(date_str.replace("Z", "")).date()
                else:
                    partition_date_to_use = datetime.date.fromisoformat(date_str)
            except ValueError as ve:
                logging.warning(f"Could not parse event date '{date_str}' from field '{event_date_field}'. Defaulting to ingestion date partitioning. Error: {ve}")
        else:
            logging.warning(f"Event date field '{event_date_field}' not found in data. Defaulting to ingestion date partitioning.")


    saved_path = save_raw_data(raw_data_list, target_base_path, file_name_prefix, partition_date=partition_date_to_use)

    if saved_path:
        logging.info(f"[{job_name}] Ingestion job completed. Data saved to {saved_path}")
    else:
        logging.error(f"[{job_name}] Ingestion job failed to save data.")

# --- Example Usage (Illustrative) ---
if __name__ == "__main__":
    import random
    from utils.mock_data_generator import (
        generate_mock_asset_list,
        generate_mock_daily_prices,
        generate_mock_news_articles,
        generate_mock_news_sources,
        generate_mock_economic_event_types
    )

    logging.info(f"Mock data lake base directory: {MOCK_DATA_LAKE_BASE_DIR}")
    ensure_dir(MOCK_DATA_LAKE_BASE_DIR) # Ensure base data lake dir exists

    # 1. Simulate fetching a list of assets (metadata, not time series)
    # This might be a one-time or infrequent job.
    asset_fetcher = MockApiFetcher(
        api_name="AssetMaster_Mock",
        data_generator_func=generate_mock_asset_list
    )
    run_ingestion_job(
        job_name="Load All Mock Assets",
        fetcher=asset_fetcher,
        data_category_path="metadata/assets", # Different path for non-time-series general metadata
        file_name_prefix="all_assets",
        fetch_params={"num_assets": 5} # Generate 5 mock assets
    )

    # For further examples, we'd need the output of asset_fetcher to get asset_ids/tickers
    # For simplicity, let's re-generate them here or assume they are known.
    mock_assets = generate_mock_asset_list(num_assets=2) # Get a couple of assets for price/news generation
    if not mock_assets:
        logging.error("Could not generate mock assets for price/news ingestion examples. Exiting.")
        exit()

    # 2. Simulate fetching daily prices for a specific asset and date range
    # In a real system, you'd loop through tickers and date ranges.
    selected_asset = mock_assets[0]
    prices_fetcher = MockApiFetcher(
        api_name="PolygonIO_DailyPrices_Mock",
        data_generator_func=generate_mock_daily_prices
    )
    start_date = (datetime.date.today() - datetime.timedelta(days=5)).isoformat()
    end_date = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()

    run_ingestion_job(
        job_name=f"Load Daily Prices for {selected_asset['ticker_symbol']}",
        fetcher=prices_fetcher,
        data_category_path=f"market_data/polygon_io_mock/equities_daily_bars/ticker={selected_asset['ticker_symbol']}", # Example ticker-specific path part
        file_name_prefix=f"{selected_asset['ticker_symbol']}_daily_prices",
        fetch_params={
            "asset_id": selected_asset["asset_id"],
            "ticker": selected_asset["ticker_symbol"],
            "start_date_str": start_date,
            "end_date_str": end_date
        },
        partition_data_by_event_date=True, # Partition by trade_date within the data
        event_date_field='trade_date' # This will use the first trade_date in the list for the YYYY/MM/DD path part
                                      # A real system might save one file per day or smaller chunks.
    )

    # 3. Simulate fetching news articles
    mock_news_sources = generate_mock_news_sources()
    mock_econ_event_types = generate_mock_economic_event_types(num_types=3)

    news_fetcher = MockApiFetcher(
        api_name="BenzingaNews_Mock",
        data_generator_func=generate_mock_news_articles
    )
    run_ingestion_job(
        job_name="Load Recent News Articles",
        fetcher=news_fetcher,
        data_category_path="news_data/benzinga_mock",
        file_name_prefix="recent_news",
        fetch_params={
            "assets": mock_assets,
            "news_sources": mock_news_sources,
            "economic_event_types": mock_econ_event_types,
            "num_articles": 5
        },
        partition_data_by_event_date=True, # Partition by publish_timestamp_utc
        event_date_field='publish_timestamp_utc'
    )

    logging.info("Generic ingestion framework simulation complete. Check mock_s3_data_lake directory.")
