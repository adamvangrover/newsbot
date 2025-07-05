import datetime
import logging
import random

# Make sure 'utils' and 'ingestion' are discoverable.
# This can be done by setting PYTHONPATH, or if the script is run from the project root.
import sys
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from ingestion.generic_ingestor import MockApiFetcher, run_ingestion_job, MOCK_DATA_LAKE_BASE_DIR, ensure_dir
from utils.mock_data_generator import (
    generate_mock_asset_list,
    generate_mock_sp500_constituents,
    generate_mock_daily_prices,
    generate_mock_corporate_actions
)

LOG_FORMAT = '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

def ingest_market_data():
    logging.info("Starting mock market data ingestion process...")
    ensure_dir(MOCK_DATA_LAKE_BASE_DIR)

    # --- 0. Generate a base list of assets ---
    # These are all potential assets in our universe, not necessarily S&P 500.
    # The mock S&P 500 constituents will be drawn from this list.
    logging.info("Generating a base list of mock assets...")
    all_mock_assets = generate_mock_asset_list(num_assets=20) # Generate 20 potential assets
    if not all_mock_assets:
        logging.error("Failed to generate base mock assets. Aborting market data ingestion.")
        return

    # Save the full asset list (simulating an asset master)
    # This isn't strictly "market data integration" but foundational.
    asset_master_fetcher = MockApiFetcher(
        api_name="AssetMaster_Mock",
        data_generator_func=lambda: all_mock_assets # Use the already generated list
    )
    run_ingestion_job(
        job_name="Load All Mock Assets Master List",
        fetcher=asset_master_fetcher,
        data_category_path="metadata/assets_master",
        file_name_prefix="all_assets_master_snapshot"
    )
    logging.info(f"Successfully saved master list of {len(all_mock_assets)} assets.")


    # --- 1. Historical Constituents (simulating EODHD for S&P 500) ---
    logging.info("Ingesting mock S&P 500 historical constituents...")
    constituents_fetcher = MockApiFetcher(
        api_name="EODHD_SP500Constituents_Mock",
        # The lambda ensures the generate function gets the up-to-date all_mock_assets
        data_generator_func=lambda num_const: generate_mock_sp500_constituents(all_mock_assets, num_const)
    )
    run_ingestion_job(
        job_name="Load S&P 500 Mock Constituents",
        fetcher=constituents_fetcher,
        data_category_path="market_data/eodhd_constituents_mock", # As per s3_structure.txt
        file_name_prefix="sp500_constituents_snapshot",
        fetch_params={"num_const": 10} # Generate mock constituents for 10 companies from our asset list
    )
    # For subsequent steps, we need the actual list of constituents generated.
    # The run_ingestion_job saves it to a file, but for this script flow, let's regenerate it
    # or ideally, the generic_ingestor could return the data it saved.
    # For simplicity here, we'll fetch it again (which is fine for mock data).
    # In a real scenario, this data would be loaded from where it was saved or passed differently.
    mock_sp500_constituents_data = constituents_fetcher.fetch_data(num_const=10)
    if not mock_sp500_constituents_data:
        logging.error("Failed to generate/fetch mock S&P 500 constituents for price/action generation. Aborting.")
        return

    logging.info(f"Successfully ingested {len(mock_sp500_constituents_data)} mock S&P 500 constituents.")

    # Extract asset details for the constituents to use for price/action generation
    # We need asset_id and ticker_symbol from the *original* all_mock_assets list
    # that correspond to the tickers in mock_sp500_constituents_data.
    constituent_tickers = {c['ticker_symbol'] for c in mock_sp500_constituents_data}
    assets_for_prices_actions = [asset for asset in all_mock_assets if asset['ticker_symbol'] in constituent_tickers]

    if not assets_for_prices_actions:
        logging.warning("No valid constituent assets found to generate prices/actions for. This might happen if constituent generation failed or returned empty.")
        # We can still proceed if other parts of the script don't depend on this.
    else:
        logging.info(f"Will generate prices and actions for {len(assets_for_prices_actions)} constituent assets: {[a['ticker_symbol'] for a in assets_for_prices_actions]}.")


    # --- 2. Price/Volume Data (simulating Polygon.io) ---
    logging.info("Ingesting mock daily OHLCV data for S&P 500 constituents...")
    prices_fetcher = MockApiFetcher(
        api_name="PolygonIO_DailyPrices_Mock",
        data_generator_func=generate_mock_daily_prices # This function is called per asset
    )

    # Define date range for price generation
    # Let's do a shorter period for mock data to keep it manageable
    num_days_history = 30 # Generate 30 days of history
    end_date_prices = datetime.date.today() - datetime.timedelta(days=1)
    start_date_prices = end_date_prices - datetime.timedelta(days=num_days_history -1)

    for asset_info in assets_for_prices_actions:
        asset_id = asset_info["asset_id"]
        ticker = asset_info["ticker_symbol"]

        logging.info(f"Fetching daily prices for {ticker} (ID: {asset_id})...")
        run_ingestion_job(
            job_name=f"Load Daily Prices for {ticker}",
            fetcher=prices_fetcher,
            # Path structure: market_data/polygon_io_mock/equities_daily_bars/ticker=AAPL/
            # The generic_ingestor's save_raw_data will create YYYY/MM/DD subfolders within this
            # if partition_data_by_event_date is True and event_date_field is correct.
            data_category_path=f"market_data/polygon_io_mock/equities_daily_bars/ticker={ticker}",
            file_name_prefix=f"{ticker}_daily_prices_{start_date_prices.strftime('%Y%m%d')}_{end_date_prices.strftime('%Y%m%d')}",
            fetch_params={
                "asset_id": asset_id,
                "ticker": ticker,
                "start_date_str": start_date_prices.isoformat(),
                "end_date_str": end_date_prices.isoformat()
            },
            # The daily prices are a list, each item having a 'trade_date'.
            # We want to partition the *output file's directory structure* based on this date.
            # For this mock, the file itself contains multiple days.
            # A more granular approach would be one file per ticker per day.
            # The current generic_ingestor saves the whole list into one file, using the first item's date for dir partitioning.
            partition_data_by_event_date=True,
            event_date_field='trade_date' # Field in generate_mock_daily_prices output
        )

    logging.info("Finished ingesting mock daily OHLCV data.")

    # --- 3. Corporate Actions (simulating Polygon.io) ---
    logging.info("Ingesting mock corporate actions for S&P 500 constituents...")
    actions_fetcher = MockApiFetcher(
        api_name="PolygonIO_CorporateActions_Mock",
        data_generator_func=generate_mock_corporate_actions # Called per asset
    )

    for asset_info in assets_for_prices_actions:
        asset_id = asset_info["asset_id"]
        ticker = asset_info["ticker_symbol"]

        logging.info(f"Fetching corporate actions for {ticker} (ID: {asset_id})...")
        run_ingestion_job(
            job_name=f"Load Corporate Actions for {ticker}",
            fetcher=actions_fetcher,
            data_category_path=f"market_data/polygon_io_mock/corporate_actions/ticker={ticker}",
            file_name_prefix=f"{ticker}_corporate_actions",
            fetch_params={
                "asset_id": asset_id,
                "ticker": ticker,
                "num_actions": random.randint(0, 3) # Generate 0 to 3 actions per stock
            },
            # Corporate actions are often a list for a ticker.
            # Partitioning by event_date (e.g., ex_date) might mean multiple files if actions have different dates.
            # For simplicity, one file per ticker containing all its mock actions.
            # The current generic_ingestor will use ingestion date for dir if event_date_field is None or not found.
            partition_data_by_event_date=True,
            event_date_field='ex_date' # Field in generate_mock_corporate_actions output
        )
    logging.info("Finished ingesting mock corporate actions.")
    logging.info("Mock market data ingestion process complete. Check the 'mock_s3_data_lake/raw_data' directory.")

if __name__ == "__main__":
    ingest_market_data()
