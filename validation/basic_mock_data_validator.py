import json
import logging
import os
from pathlib import Path
from typing import List, Dict, Any, Tuple
import sys # Import sys

# Add project root to sys.path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

# Now imports from other top-level dirs like 'ingestion' should work
from ingestion.generic_ingestor import MOCK_DATA_LAKE_BASE_DIR

LOG_FORMAT = '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

# Define expected key fields for different data types for our mock data
# These would be more extensive in a real system
EXPECTED_KEYS = {
    "assets_master": ["asset_id", "ticker_symbol", "company_name", "asset_class", "exchange"],
    "sp500_constituents": ["constituent_id", "universe_name", "ticker_symbol", "asset_id", "start_date"],
    "daily_prices": ["asset_id", "ticker_symbol", "trade_date", "open_price", "high_price", "low_price", "close_price", "volume"],
    "corporate_actions": ["action_id", "asset_id", "ticker_symbol", "action_type", "ex_date"],
    "economic_event_types": ["event_type_id", "event_name", "country_region", "source_identifier"],
    "economic_events": ["event_id", "event_type_id", "release_datetime_utc", "actual_value", "consensus_value_pit"],
    "sec_filing_types": ["filing_type_id", "form_type"],
    "sec_filings_metadata": ["filing_id", "cik", "filing_type_id", "filing_date", "accession_number", "raw_text_s3_path"],
    "news_sources": ["news_source_id", "source_name", "website"],
    "news_articles_metadata": ["article_id", "news_source_id", "headline", "publish_timestamp_utc", "raw_text_s3_path"],
    "cb_doc_types": ["doc_type_id", "doc_type_name", "issuing_body"],
    "cb_documents": ["document_id", "doc_type_id", "publish_timestamp_utc", "title", "raw_text_s3_path"]
}

import re # Import re module

# Expected data types (very basic check)
# Values are functions that return True if type is valid
ISO_DATETIME_REGEX = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,6})?(Z|[+-]\d{2}:\d{2})?" # More robust ISO datetime

EXPECTED_TYPES = {
    "asset_id": lambda x: isinstance(x, int),
    "ticker_symbol": lambda x: isinstance(x, str) and x, # Non-empty string
    "company_name": lambda x: isinstance(x, str),
    "asset_class": lambda x: isinstance(x, str),
    "exchange": lambda x: isinstance(x, str),
    "constituent_id": lambda x: isinstance(x, int),
    "universe_name": lambda x: isinstance(x, str),
    "start_date": lambda x: isinstance(x, str) and bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", x)),
    "end_date": lambda x: x is None or (isinstance(x, str) and bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", x))),
    "trade_date": lambda x: isinstance(x, str) and bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", x)),
    "open_price": lambda x: isinstance(x, (int, float)),
    "high_price": lambda x: isinstance(x, (int, float)),
    "low_price": lambda x: isinstance(x, (int, float)),
    "close_price": lambda x: isinstance(x, (int, float)),
    "volume": lambda x: isinstance(x, int) and x >= 0,
    "action_id": lambda x: isinstance(x, int),
    "action_type": lambda x: isinstance(x, str),
    "ex_date": lambda x: isinstance(x, str) and bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", x)),

    # Phase 2 types
    "event_type_id": lambda x: isinstance(x, int),
    "event_name": lambda x: isinstance(x, str) and x,
    "country_region": lambda x: isinstance(x, str),
    "source_identifier": lambda x: isinstance(x, str),
    "event_id": lambda x: isinstance(x, int),
    "release_datetime_utc": lambda x: isinstance(x, str) and bool(re.fullmatch(ISO_DATETIME_REGEX, x)),
    "actual_value": lambda x: isinstance(x, (int, float, type(None))), # Can be None if not yet released
    "consensus_value_pit": lambda x: isinstance(x, (int, float, type(None))),
    "filing_type_id": lambda x: isinstance(x, int),
    "form_type": lambda x: isinstance(x, str) and x,
    "filing_id": lambda x: isinstance(x, int),
    "cik": lambda x: isinstance(x, str) and x,
    "filing_date": lambda x: isinstance(x, str) and bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", x)),
    "accession_number": lambda x: isinstance(x, str) and x,
    "raw_text_s3_path": lambda x: isinstance(x, str) and x.startswith("s3://"),
    "news_source_id": lambda x: isinstance(x, int),
    "source_name": lambda x: isinstance(x, str) and x,
    "website": lambda x: isinstance(x, str) and x.startswith("https://"),
    "article_id": lambda x: isinstance(x, int),
    "headline": lambda x: isinstance(x, str) and x,
    "publish_timestamp_utc": lambda x: isinstance(x, str) and bool(re.fullmatch(ISO_DATETIME_REGEX, x)),
    "doc_type_id": lambda x: isinstance(x, int),
    "doc_type_name": lambda x: isinstance(x, str) and x,
    "issuing_body": lambda x: isinstance(x, str) and x,
    "document_id": lambda x: isinstance(x, int),
    "title": lambda x: isinstance(x, str),


    # Fields from _ingestion_details (added by generic_ingestor)
    "_ingestion_details": lambda x: isinstance(x, dict),
    "ingested_at_utc": lambda x: isinstance(x, str) and bool(re.fullmatch(ISO_DATETIME_REGEX, x)),
    "source_api_simulation": lambda x: isinstance(x, str),
}


def validate_json_file(file_path: Path, data_category_key: str) -> Tuple[bool, List[str]]:
    """
    Validates a single JSON file.
    Checks if it's valid JSON, and if its records contain expected keys and basic types.
    """
    errors = []
    is_valid_file = True

    if not file_path.exists():
        errors.append(f"File does not exist: {file_path}")
        return False, errors

    try:
        with open(file_path, 'r') as f:
            data_list = json.load(f)
    except json.JSONDecodeError as e:
        errors.append(f"Invalid JSON in file {file_path}: {e}")
        return False, errors
    except Exception as e:
        errors.append(f"Could not read file {file_path}: {e}")
        return False, errors

    if not isinstance(data_list, list):
        errors.append(f"File {file_path} does not contain a JSON list as expected.")
        # Depending on structure, might not be an error, but for our mock data it is.
        return False, errors

    if not data_list:
        logging.warning(f"File {file_path} is empty or contains an empty list.")
        # Not strictly an error for this validator, but worth noting. Some files might be validly empty.
        # Example: a corporate actions file for a stock that had no actions.

    expected_keys_for_category = EXPECTED_KEYS.get(data_category_key, [])

    for i, record in enumerate(data_list):
        if not isinstance(record, dict):
            errors.append(f"Record {i} in {file_path} is not a dictionary.")
            is_valid_file = False
            continue # Skip key checks for this malformed record

        # Check for expected keys
        for key in expected_keys_for_category:
            if key not in record:
                errors.append(f"Missing key '{key}' in record {i} of {file_path}.")
                is_valid_file = False

        # Check for _ingestion_details (should be added by our generic ingestor)
        if "_ingestion_details" not in record:
            errors.append(f"Missing key '_ingestion_details' in record {i} of {file_path}.")
            is_valid_file = False
        elif not EXPECTED_TYPES["_ingestion_details"](record["_ingestion_details"]):
             errors.append(f"Invalid type for '_ingestion_details' (expected dict) in record {i} of {file_path}.")
             is_valid_file = False
        else: # Check sub-keys of _ingestion_details
            if "ingested_at_utc" not in record["_ingestion_details"] or \
               not EXPECTED_TYPES["ingested_at_utc"](record["_ingestion_details"]["ingested_at_utc"]):
                errors.append(f"Missing or invalid 'ingested_at_utc' in _ingestion_details for record {i} of {file_path}.")
                is_valid_file = False
            if "source_api_simulation" not in record["_ingestion_details"] or \
               not EXPECTED_TYPES["source_api_simulation"](record["_ingestion_details"]["source_api_simulation"]):
                errors.append(f"Missing or invalid 'source_api_simulation' in _ingestion_details for record {i} of {file_path}.")
                is_valid_file = False


        # Check basic data types for known keys
        for key, type_checker_func in EXPECTED_TYPES.items():
            if key in record and record[key] is not None: # Only check if key exists and value is not None
                if not type_checker_func(record[key]):
                    errors.append(f"Invalid type for key '{key}' (value: {record[key]}, type: {type(record[key])}) in record {i} of {file_path}.")
                    is_valid_file = False

    return is_valid_file, errors


def run_basic_validation_on_mock_data():
    """
    Walks through the mock data lake and performs basic validation on found JSON files.
    """
    logging.info(f"Starting basic validation on mock data in: {MOCK_DATA_LAKE_BASE_DIR}")

    # Define paths and corresponding data category keys for validation rules
    # This is a simplified mapping. A real system might have a more robust way to determine data type.
    validation_map = [
        # Phase 1 data
        ("metadata/assets_master", "assets_master"),
        ("market_data/eodhd_constituents_mock", "sp500_constituents"),
        ("market_data/polygon_io_mock/equities_daily_bars", "daily_prices"),
        ("market_data/polygon_io_mock/corporate_actions", "corporate_actions"),
        # Phase 2 data
        ("economic_data/econoday_mock/event_types", "economic_event_types"),
        ("economic_data/econoday_mock/event_releases", "economic_events"),
        ("corporate_filings/sec_api_io_mock/filing_types", "sec_filing_types"),
        ("corporate_filings/sec_api_io_mock/filings_metadata_index", "sec_filings_metadata"),
        ("news_data/generic_news_api_mock/news_sources", "news_sources"),
        ("news_data/generic_news_api_mock/articles_metadata", "news_articles_metadata"),
        ("central_bank_communications/scrapers_mock/doc_types", "cb_doc_types"),
        ("central_bank_communications/scrapers_mock/documents", "cb_documents")
    ]

    total_files_checked = 0
    total_errors_found = 0

    for data_path_suffix, category_key in validation_map:
        current_path = MOCK_DATA_LAKE_BASE_DIR / data_path_suffix
        logging.info(f"Validating data in {current_path} for category '{category_key}'...")

        if not current_path.exists():
            logging.warning(f"Path {current_path} does not exist. Skipping validation for this category.")
            continue

        # Walk through all JSON files in the directory and its subdirectories
        for filepath in current_path.rglob('*.json'):
            if filepath.is_file():
                logging.info(f"  Validating file: {filepath}")
                total_files_checked += 1
                is_valid, errors = validate_json_file(filepath, category_key)
                if not is_valid:
                    total_errors_found += len(errors)
                    for err in errors:
                        logging.error(f"    VALIDATION ERROR: {err}")
                else:
                    logging.info(f"    File {filepath} passed basic validation.")

    logging.info(f"Basic validation complete. Checked {total_files_checked} files. Found {total_errors_found} errors.")
    if total_errors_found > 0:
        logging.warning("Some mock data files failed basic validation. Check logs for details.")
    else:
        logging.info("All checked mock data files passed basic validation.")

def conceptual_monitoring_notes():
    """
    Placeholder to discuss what would be monitored in a real system.
    """
    logging.info("\n--- Conceptual Monitoring Notes for a Real Data Pipeline ---")
    notes = [
        "1. Ingestion Job Status: Track success/failure of each data ingestion job (e.g., from Airflow, cron). Alerts on failures.",
        "2. Data Freshness/Latency: Monitor how up-to-date the data is from each source. E.g., 'Last S&P500 prices received are from YYYY-MM-DD HH:MM:SS'. Alerts if data is stale beyond a threshold.",
        "3. Record Counts: Number of records ingested per source per run. Significant deviations from norm (e.g., 90% drop in news articles) could indicate source-side issues or ingestion bugs.",
        "4. API Error Rates: Monitor HTTP error codes (4xx, 5xx) from vendor APIs. High error rates could mean API key issues, rate limits hit, or vendor outages.",
        "5. Data Quality Metrics (Post-Validation): Track metrics like percentage of records failing validation checks, null rates for key fields, outlier detection (e.g., price spikes).",
        "6. File System / Data Lake Metrics: Monitor storage utilization, number of files/objects, partitioning health (e.g., are files landing in correct date partitions).",
        "7. Database Metrics: For data loaded into SQL (TimescaleDB), monitor insert rates, query performance, disk space, connection counts.",
        "8. Processing Pipeline Status: For feature engineering and NLP tasks, monitor job status, processing times, resource utilization (CPU, memory).",
        "9. End-to-End Latency: Time from when data is available at source to when it's processed and available in the final dataset.",
        "10. Cost Monitoring: Cloud costs associated with storage, compute, API calls (if applicable)."
    ]
    for note in notes:
        logging.info(note)
    logging.info("--- End of Conceptual Monitoring Notes ---")


if __name__ == "__main__":
    # First, ensure some mock data has been generated by running the ingestion script.
    # For a standalone test, you might want to call the ingestion script from here,
    # or ensure it has been run recently.
    # Example:
    # from ingestion_scripts.run_market_data_ingestion import ingest_market_data
    # print("Ensuring some mock market data exists...")
    # ingest_market_data() # This will re-run ingestion, which is fine for mock.
    # print("Mock market data generation/check complete.\n")

    run_basic_validation_on_mock_data()
    conceptual_monitoring_notes()

    # To make this script more useful, you could add more specific checks:
    # - Range checks for numerical values (e.g., prices should be positive).
    # - Referential integrity checks (e.g., does asset_id in prices table exist in assets table - requires loading data).
    # - Uniqueness checks for primary keys within a file or across files.
    # - More sophisticated date/timestamp format validation.
    # - Schema drift detection (unexpected new fields, or fields changing type).
    # These are often handled by more robust data quality tools like Great Expectations, Deequ, or custom Spark jobs.
    # For this mock exercise, the current level is illustrative.
