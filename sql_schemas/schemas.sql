-- SQL Schemas for News-Driven Market Prediction Dataset (Mock Data Simulation)

-- #############################################################################
-- Phase 1: Foundational Setup & Core Market Data
-- #############################################################################

CREATE TABLE asset_universe (
    universe_id SERIAL PRIMARY KEY,
    universe_name VARCHAR(255) UNIQUE NOT NULL, -- e.g., 'S&P 500', 'NASDAQ 100'
    description TEXT
);

CREATE TABLE assets (
    asset_id SERIAL PRIMARY KEY,
    ticker_symbol VARCHAR(20) UNIQUE NOT NULL,
    company_name VARCHAR(255),
    asset_class VARCHAR(50) DEFAULT 'Equity', -- Equity, Forex, Crypto, etc.
    exchange VARCHAR(100), -- e.g., 'NASDAQ', 'NYSE'
    -- Add other relevant static asset information if needed
    first_seen_date DATE, -- For internal tracking
    last_seen_date DATE   -- For internal tracking
);

CREATE TABLE asset_constituents (
    constituent_id SERIAL PRIMARY KEY,
    universe_id INT NOT NULL REFERENCES asset_universe(universe_id),
    asset_id INT NOT NULL REFERENCES assets(asset_id),
    start_date DATE NOT NULL,
    end_date DATE, -- NULL if currently active
    ingestion_timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    source VARCHAR(100), -- e.g., 'EODHD_mock', 'Algoseek_mock'
    UNIQUE (universe_id, asset_id, start_date) -- Ensures a ticker is not added multiple times to the same universe on the same start_date
);

-- For TimescaleDB, equity_daily_prices would be a hypertable
CREATE TABLE equity_daily_prices (
    asset_id INT NOT NULL REFERENCES assets(asset_id),
    trade_date DATE NOT NULL,
    open_price NUMERIC(19, 4),
    high_price NUMERIC(19, 4),
    low_price NUMERIC(19, 4),
    close_price NUMERIC(19, 4),
    adjusted_close_price NUMERIC(19, 4),
    volume BIGINT,
    vwap NUMERIC(19,4), -- Volume Weighted Average Price
    ingestion_timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    source VARCHAR(100), -- e.g., 'PolygonIO_mock'
    PRIMARY KEY (asset_id, trade_date)
);
-- For TimescaleDB: SELECT create_hypertable('equity_daily_prices', 'trade_date');

-- Example for intraday, if needed (can be very large)
-- CREATE TABLE equity_intraday_bars (
--     asset_id INT NOT NULL REFERENCES assets(asset_id),
--     bar_timestamp TIMESTAMPTZ NOT NULL,
--     time_granularity VARCHAR(10) NOT NULL, -- e.g., '1min', '5min'
--     open_price NUMERIC(19, 4),
--     high_price NUMERIC(19, 4),
--     low_price NUMERIC(19, 4),
--     close_price NUMERIC(19, 4),
--     volume BIGINT,
--     vwap NUMERIC(19,4),
--     ingestion_timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
--     source VARCHAR(100),
--     PRIMARY KEY (asset_id, bar_timestamp, time_granularity)
-- );
-- For TimescaleDB: SELECT create_hypertable('equity_intraday_bars', 'bar_timestamp');

CREATE TABLE corporate_actions (
    action_id SERIAL PRIMARY KEY,
    asset_id INT NOT NULL REFERENCES assets(asset_id),
    action_type VARCHAR(50) NOT NULL, -- e.g., 'Dividend', 'Split', 'Merger', 'Spinoff'
    ex_date DATE, -- Ex-dividend date for dividends
    record_date DATE,
    payable_date DATE,
    declaration_date DATE,
    value_ratio NUMERIC(19, 8), -- For splits (e.g., 2 for a 2-for-1 split), or dividend amount
    value_currency VARCHAR(10), -- e.g., USD for dividend amount
    notes TEXT,
    ingestion_timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    source VARCHAR(100) -- e.g., 'PolygonIO_mock', 'Refinitiv_mock'
);

-- #############################################################################
-- Phase 2: Macroeconomic, Corporate Filings & News Data
-- #############################################################################

CREATE TABLE economic_event_types (
    event_type_id SERIAL PRIMARY KEY,
    event_name VARCHAR(255) UNIQUE NOT NULL, -- e.g., 'US Non-Farm Payrolls', 'ECB Interest Rate Decision'
    country_region VARCHAR(100), -- e.g., 'USA', 'Eurozone', 'DEU'
    release_frequency VARCHAR(50), -- e.g., 'Monthly', 'Quarterly'
    description TEXT,
    source_identifier VARCHAR(255) -- Identifier from the source like Econoday
);

CREATE TABLE economic_events (
    event_id SERIAL PRIMARY KEY,
    event_type_id INT NOT NULL REFERENCES economic_event_types(event_type_id),
    release_datetime_utc TIMESTAMPTZ NOT NULL, -- Official release time
    period_covered VARCHAR(100), -- e.g., 'March 2023', 'Q1 2023'
    actual_value NUMERIC(19, 4),
    consensus_value_pit NUMERIC(19, 4), -- Point-in-time consensus just before release
    previous_value NUMERIC(19, 4),
    revised_previous_value NUMERIC(19, 4), -- If the previous value was revised at this release
    unit VARCHAR(50), -- e.g., 'K', '%', 'Index'
    notes TEXT,
    ingestion_timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    source VARCHAR(100) -- e.g., 'Econoday_mock'
);

CREATE TABLE sec_filing_types (
    filing_type_id SERIAL PRIMARY KEY,
    form_type VARCHAR(20) UNIQUE NOT NULL, -- e.g., '10-K', '10-Q', '8-K'
    description TEXT
);

CREATE TABLE sec_filings_metadata (
    filing_id SERIAL PRIMARY KEY,
    asset_id INT REFERENCES assets(asset_id), -- Link to asset if identifiable (e.g. via CIK)
    cik VARCHAR(20), -- Central Index Key
    filing_type_id INT NOT NULL REFERENCES sec_filing_types(filing_type_id),
    filing_date DATE NOT NULL,
    period_of_report DATE,
    accession_number VARCHAR(50) UNIQUE, -- Unique identifier for the filing
    raw_text_s3_path VARCHAR(512), -- Path to raw text file in S3 data lake
    structured_json_s3_path VARCHAR(512), -- Path to parsed JSON in S3
    ingestion_timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    source VARCHAR(100) -- e.g., 'SECApi_mock'
);

CREATE TABLE news_sources (
    news_source_id SERIAL PRIMARY KEY,
    source_name VARCHAR(255) UNIQUE NOT NULL, -- e.g., 'Benzinga', 'Reuters', 'WSJ'
    website VARCHAR(255)
);

CREATE TABLE news_articles_metadata (
    article_id SERIAL PRIMARY KEY,
    news_source_id INT REFERENCES news_sources(news_source_id),
    article_url VARCHAR(1024) UNIQUE,
    headline TEXT NOT NULL,
    publish_timestamp_utc TIMESTAMPTZ NOT NULL,
    tickers_mentioned TEXT[], -- Array of ticker symbols
    raw_text_s3_path VARCHAR(512), -- Path to article body in S3
    ingestion_timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    source_api VARCHAR(100) -- e.g., 'PolygonIO_Benzinga_mock'
);

CREATE TABLE central_bank_document_types (
    doc_type_id SERIAL PRIMARY KEY,
    doc_type_name VARCHAR(255) UNIQUE NOT NULL, -- e.g., 'FOMC Minutes', 'ECB Press Conference Statement', 'Speech'
    issuing_body VARCHAR(100) -- e.g., 'Federal Reserve', 'ECB'
);

CREATE TABLE central_bank_documents (
    document_id SERIAL PRIMARY KEY,
    doc_type_id INT NOT NULL REFERENCES central_bank_document_types(doc_type_id),
    publish_timestamp_utc TIMESTAMPTZ NOT NULL,
    title TEXT,
    speaker_author VARCHAR(255),
    raw_text_s3_path VARCHAR(512),
    document_url VARCHAR(1024),
    ingestion_timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    source VARCHAR(100) -- e.g., 'FedScraper_mock', 'ECBScraper_mock'
);

-- #############################################################################
-- Phase 3: Feature Engineering & NLP Development
-- #############################################################################

-- This data might be stored in Parquet files or a feature store,
-- but we can define a schema for how it *could* look in SQL.
CREATE TABLE derived_market_features (
    asset_id INT NOT NULL REFERENCES assets(asset_id),
    feature_date DATE NOT NULL,
    return_1d NUMERIC(19, 8),
    return_5d NUMERIC(19, 8),
    volatility_30d_atr NUMERIC(19, 8), -- Example: Average True Range
    sma_20d NUMERIC(19, 4), -- 20-day simple moving average
    -- Add many other features
    PRIMARY KEY (asset_id, feature_date)
);

CREATE TABLE economic_surprise_features (
    event_id INT NOT NULL REFERENCES economic_events(event_id),
    surprise_value NUMERIC(19, 4), -- actual - consensus
    surprise_zscore NUMERIC(19, 8), -- Normalized surprise
    PRIMARY KEY (event_id)
);

CREATE TABLE nlp_features_news (
    article_id INT NOT NULL REFERENCES news_articles_metadata(article_id),
    model_name VARCHAR(100), -- e.g., 'FinBERT_sentiment', 'FinBERT_uncertainty'
    sentiment_score NUMERIC(5, 4), -- e.g., from -1 to 1
    sentiment_label VARCHAR(20), -- e.g., 'Positive', 'Negative', 'Neutral'
    uncertainty_score NUMERIC(5, 4),
    litigiousness_score NUMERIC(5, 4),
    -- Other NLP derived features (e.g., topic IDs, key entities with their sentiment)
    processed_timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (article_id, model_name)
);

CREATE TABLE nlp_features_sec_filings (
    filing_id INT NOT NULL REFERENCES sec_filings_metadata(filing_id),
    section VARCHAR(100), -- e.g., 'MDA', 'RiskFactors', 'FullText'
    model_name VARCHAR(100),
    sentiment_score NUMERIC(5, 4),
    sentiment_label VARCHAR(20),
    uncertainty_score NUMERIC(5, 4),
    litigiousness_score NUMERIC(5, 4),
    processed_timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (filing_id, section, model_name)
);

CREATE TABLE geopolitical_event_sources (
    geopol_source_id SERIAL PRIMARY KEY,
    source_name VARCHAR(100) UNIQUE NOT NULL -- e.g., 'GDELT_mock', 'ManualCuration'
);

CREATE TABLE geopolitical_events (
    geopol_event_id SERIAL PRIMARY KEY,
    geopol_source_id INT NOT NULL REFERENCES geopolitical_event_sources(geopol_source_id),
    event_timestamp_utc TIMESTAMPTZ NOT NULL,
    country_region_involved VARCHAR(255),
    event_type VARCHAR(255), -- e.g., 'Conflict', 'Election', 'TradeAgreement'
    description TEXT,
    relevance_score NUMERIC(5,4), -- If available from source or curation
    affected_assets_tickers TEXT[], -- Array of tickers
    ingestion_timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- #############################################################################
-- Phase 4: Alternative Data (Social Media - Pilot)
-- #############################################################################

CREATE TABLE social_media_platforms (
    platform_id SERIAL PRIMARY KEY,
    platform_name VARCHAR(100) UNIQUE NOT NULL -- e.g., 'Twitter_X', 'Reddit'
);

CREATE TABLE social_media_posts (
    post_id SERIAL PRIMARY KEY,
    platform_id INT NOT NULL REFERENCES social_media_platforms(platform_id),
    post_guid VARCHAR(255) UNIQUE NOT NULL, -- platform-specific unique ID for the post
    author_guid VARCHAR(255), -- platform-specific unique ID for the author
    publish_timestamp_utc TIMESTAMPTZ NOT NULL,
    post_text TEXT,
    tickers_mentioned TEXT[],
    hashtags TEXT[],
    like_count INT,
    retweet_reply_count INT,
    -- NLP features can be in a separate table or added here if simple
    sentiment_score NUMERIC(5,4),
    sentiment_label VARCHAR(20),
    raw_json_s3_path VARCHAR(512),
    ingestion_timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    source_collection_method VARCHAR(100) -- e.g., 'X_API_mock', 'AcademicDataset_mock'
);

-- Note: For TimescaleDB, remember to convert relevant tables (e.g., those with timestamps)
-- into hypertables using `SELECT create_hypertable('table_name', 'time_column_name');`
-- e.g., SELECT create_hypertable('equity_daily_prices', 'trade_date');
-- e.g., SELECT create_hypertable('economic_events', 'release_datetime_utc');
-- e.g., SELECT create_hypertable('news_articles_metadata', 'publish_timestamp_utc');
-- etc.
-- Indexes on foreign keys, timestamps, and frequently queried columns are also crucial
-- but are omitted here for brevity but should be part of a real implementation.
-- For example:
-- CREATE INDEX ON equity_daily_prices (trade_date DESC);
-- CREATE INDEX ON news_articles_metadata (publish_timestamp_utc DESC);
-- CREATE INDEX ON asset_constituents (asset_id, start_date, end_date);

-- Example of creating a hypertable (run these in Postgres after creating the table)
-- SELECT create_hypertable('equity_daily_prices', 'trade_date');
-- SELECT create_hypertable('economic_events', 'release_datetime_utc');
-- SELECT create_hypertable('news_articles_metadata', 'publish_timestamp_utc');
-- SELECT create_hypertable('central_bank_documents', 'publish_timestamp_utc');
-- SELECT create_hypertable('geopolitical_events', 'event_timestamp_utc');
-- SELECT create_hypertable('social_media_posts', 'publish_timestamp_utc');

-- If using intraday bars:
-- SELECT create_hypertable('equity_intraday_bars', 'bar_timestamp');


-- #############################################################################
-- Phase 5: User-Specific Data (Portfolios)
-- #############################################################################

CREATE TABLE portfolios (
    portfolio_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL, -- In a real system, this would be a foreign key to a users table
    portfolio_name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, portfolio_name) -- A user cannot have two portfolios with the same name
);

CREATE TABLE portfolio_assets (
    portfolio_asset_id SERIAL PRIMARY KEY,
    portfolio_id INT NOT NULL REFERENCES portfolios(portfolio_id) ON DELETE CASCADE,
    asset_id INT NOT NULL REFERENCES assets(asset_id) ON DELETE CASCADE,
    added_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (portfolio_id, asset_id) -- An asset can only be in a portfolio once
);

COMMIT;
