import datetime
import logging
import random

import sys
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from ingestion.generic_ingestor import MockApiFetcher, run_ingestion_job, MOCK_DATA_LAKE_BASE_DIR, ensure_dir
from utils.mock_data_generator import (
    generate_mock_economic_event_types, generate_mock_economic_events,
    generate_mock_sec_filing_types, generate_mock_sec_filings_metadata,
    generate_mock_news_sources, generate_mock_news_articles,
    generate_mock_cb_doc_types, generate_mock_cb_documents,
    generate_mock_asset_list # Needed for linking filings/news to assets
)

LOG_FORMAT = '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

def ingest_phase2_data():
    logging.info("Starting mock Phase 2 data ingestion process (Economic, Filings, News, Central Banks)...")
    ensure_dir(MOCK_DATA_LAKE_BASE_DIR)

    # --- 0. Prerequisite: Generate some assets if not already done (for linking) ---
    # In a real scenario, this would come from the existing asset master.
    # For this script, we'll generate a small list.
    mock_assets = generate_mock_asset_list(num_assets=10)
    if not mock_assets:
        logging.error("Failed to generate mock assets for Phase 2 data linking. Aborting.")
        return
    logging.info(f"Using {len(mock_assets)} mock assets for linking in Phase 2 data.")

    # --- 1. Economic Calendar Data (simulating Econoday) ---
    logging.info("Ingesting mock Economic Event Types...")
    econ_event_types_fetcher = MockApiFetcher(
        api_name="Econoday_EventTypes_Mock",
        data_generator_func=generate_mock_economic_event_types
    )
    run_ingestion_job(
        job_name="Load Mock Economic Event Types",
        fetcher=econ_event_types_fetcher,
        data_category_path="economic_data/econoday_mock/event_types",
        file_name_prefix="economic_event_types_snapshot",
        fetch_params={"num_types": 10} # Generate 10 types of economic events
    )
    # Fetch the generated types to use for event generation
    mock_econ_event_types = econ_event_types_fetcher.fetch_data(num_types=10)
    if not mock_econ_event_types:
        logging.error("Failed to generate mock economic event types. Aborting economic event ingestion.")
    else:
        logging.info(f"Successfully ingested {len(mock_econ_event_types)} mock economic event types.")
        logging.info("Ingesting mock Economic Events...")
        econ_events_fetcher = MockApiFetcher(
            api_name="Econoday_Events_Mock",
            data_generator_func=generate_mock_economic_events
        )
        run_ingestion_job(
            job_name="Load Mock Economic Events",
            fetcher=econ_events_fetcher,
            data_category_path="economic_data/econoday_mock/event_releases",
            file_name_prefix="economic_events",
            fetch_params={"event_types": mock_econ_event_types, "num_events_per_type": 3}, # 3 events per type
            partition_data_by_event_date=True,
            event_date_field='release_datetime_utc'
        )
        logging.info("Finished ingesting mock Economic Calendar data.")

    # --- 2. SEC Filings Data (simulating sec-api.io) ---
    logging.info("Ingesting mock SEC Filing Types...")
    sec_filing_types_fetcher = MockApiFetcher(
        api_name="SECApi_FilingTypes_Mock",
        data_generator_func=generate_mock_sec_filing_types
    )
    run_ingestion_job(
        job_name="Load Mock SEC Filing Types",
        fetcher=sec_filing_types_fetcher,
        data_category_path="corporate_filings/sec_api_io_mock/filing_types",
        file_name_prefix="sec_filing_types_snapshot"
        # No num_types param, generate_mock_sec_filing_types uses internal MOCK_SEC_FORM_TYPES
    )
    mock_sec_filing_types = sec_filing_types_fetcher.fetch_data()
    if not mock_sec_filing_types:
        logging.error("Failed to generate mock SEC filing types. Aborting SEC filings metadata ingestion.")
    else:
        logging.info(f"Successfully ingested {len(mock_sec_filing_types)} mock SEC filing types.")
        logging.info("Ingesting mock SEC Filings Metadata...")
        sec_filings_meta_fetcher = MockApiFetcher(
            api_name="SECApi_FilingsMeta_Mock",
            data_generator_func=generate_mock_sec_filings_metadata
        )
        run_ingestion_job(
            job_name="Load Mock SEC Filings Metadata",
            fetcher=sec_filings_meta_fetcher,
            data_category_path="corporate_filings/sec_api_io_mock/filings_metadata_index",
            file_name_prefix="sec_filings_metadata",
            fetch_params={"assets": mock_assets, "filing_types": mock_sec_filing_types, "num_filings": 15},
            partition_data_by_event_date=True,
            event_date_field='filing_date'
        )
        logging.info("Finished ingesting mock SEC Filings data.")

    # --- 3. News Data Integration (simulating Polygon.io/Benzinga) ---
    logging.info("Ingesting mock News Sources...")
    news_sources_fetcher = MockApiFetcher(
        api_name="NewsAPI_Sources_Mock",
        data_generator_func=generate_mock_news_sources
    )
    run_ingestion_job(
        job_name="Load Mock News Sources",
        fetcher=news_sources_fetcher,
        data_category_path="news_data/generic_news_api_mock/news_sources",
        file_name_prefix="news_sources_snapshot"
    )
    mock_news_sources = news_sources_fetcher.fetch_data()

    if not mock_news_sources or not mock_econ_event_types: # Also need econ_event_types for news gen
         logging.error("Failed to generate mock news sources or econ event types. Aborting news articles ingestion.")
    else:
        logging.info(f"Successfully ingested {len(mock_news_sources)} mock news sources.")
        logging.info("Ingesting mock News Articles Metadata...")
        news_articles_fetcher = MockApiFetcher(
            api_name="NewsAPI_Articles_Mock",
            data_generator_func=generate_mock_news_articles
        )
        run_ingestion_job(
            job_name="Load Mock News Articles Metadata",
            fetcher=news_articles_fetcher,
            data_category_path="news_data/generic_news_api_mock/articles_metadata",
            file_name_prefix="news_articles_metadata",
            fetch_params={
                "assets": mock_assets,
                "news_sources": mock_news_sources,
                "economic_event_types": mock_econ_event_types, # Used by generator for variety
                "num_articles": 20
            },
            partition_data_by_event_date=True,
            event_date_field='publish_timestamp_utc'
        )
        logging.info("Finished ingesting mock News data.")

    # --- 4. Central Bank Communications (simulating Fed/ECB scrapers) ---
    logging.info("Ingesting mock Central Bank Document Types...")
    cb_doc_types_fetcher = MockApiFetcher(
        api_name="CBScraper_DocTypes_Mock",
        data_generator_func=generate_mock_cb_doc_types
    )
    run_ingestion_job(
        job_name="Load Mock Central Bank Document Types",
        fetcher=cb_doc_types_fetcher,
        data_category_path="central_bank_communications/scrapers_mock/doc_types",
        file_name_prefix="cb_doc_types_snapshot"
    )
    mock_cb_doc_types = cb_doc_types_fetcher.fetch_data()
    if not mock_cb_doc_types:
        logging.error("Failed to generate mock CB document types. Aborting CB documents ingestion.")
    else:
        logging.info(f"Successfully ingested {len(mock_cb_doc_types)} mock CB document types.")
        logging.info("Ingesting mock Central Bank Documents...")
        cb_docs_fetcher = MockApiFetcher(
            api_name="CBScraper_Documents_Mock",
            data_generator_func=generate_mock_cb_documents
        )
        run_ingestion_job(
            job_name="Load Mock Central Bank Documents",
            fetcher=cb_docs_fetcher,
            data_category_path="central_bank_communications/scrapers_mock/documents",
            file_name_prefix="cb_documents",
            fetch_params={"doc_types": mock_cb_doc_types, "num_docs": 10},
            partition_data_by_event_date=True,
            event_date_field='publish_timestamp_utc'
        )
        logging.info("Finished ingesting mock Central Bank Communications data.")

    logging.info("Mock Phase 2 data ingestion process complete. Check the 'mock_s3_data_lake/raw_data' directory.")

if __name__ == "__main__":
    ingest_phase2_data()
