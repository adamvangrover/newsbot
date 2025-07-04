import datetime
import random
import uuid
import json
from faker import Faker

fake = Faker()

# --- Configuration for Mock Data ---
MOCK_TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "BRK.A", "JPM", "V", "JNJ"]
MOCK_COMPANY_NAMES = {
    "AAPL": "Apple Inc.", "MSFT": "Microsoft Corp.", "GOOGL": "Alphabet Inc.",
    "AMZN": "Amazon.com Inc.", "TSLA": "Tesla Inc.", "NVDA": "NVIDIA Corporation",
    "BRK.A": "Berkshire Hathaway Inc.", "JPM": "JPMorgan Chase & Co.",
    "V": "Visa Inc.", "JNJ": "Johnson & Johnson"
}
MOCK_EXCHANGES = ["NASDAQ", "NYSE"]
MOCK_ASSET_CLASSES = ["Equity"]
MOCK_CURRENCIES = ["USD"]

MOCK_ECONOMIC_EVENT_NAMES = [
    "US Non-Farm Payrolls", "US CPI YoY", "US GDP Growth Rate QoQ",
    "FOMC Interest Rate Decision", "ECB Main Refinancing Rate",
    "US ISM Manufacturing PMI", "China Manufacturing PMI", "Germany ZEW Economic Sentiment"
]
MOCK_EVENT_COUNTRIES = ["USA", "Eurozone", "China", "Germany"]
MOCK_EVENT_UNITS = ["K", "%", "Index", "bps"]

MOCK_NEWS_SOURCES = ["MockNN Network", "Financial Fables Times", "Economic Echoes Today", "Market Myths Media"]
MOCK_NEWS_HEADLINE_TEMPLATES = [
    "{ticker} stock price {movement} on {reason} news.",
    "Analysts {opinion} on {company_name} following recent announcements.",
    "{event_name} figures released, market reacts with {reaction}.",
    "Breaking: {random_event_summary}"
]
NEWS_MOVEMENTS = ["surges", "dips", "stabilizes", "climbs", "falls", "fluctuates"]
NEWS_REASONS = ["positive earnings", "product launch", "regulatory concerns", "market sentiment", "geopolitical tensions"]
NEWS_OPINIONS = ["bullish", "bearish", "neutral", "cautiously optimistic"]
NEWS_REACTIONS = ["optimism", "caution", "volatility", "surprise"]

MOCK_SEC_FORM_TYPES = ["10-K", "10-Q", "8-K", "4", "S-1"]
MOCK_CB_DOC_TYPES_FED = ["FOMC Statement", "FOMC Minutes", "Chair Speech", "Beige Book"]
MOCK_CB_DOC_TYPES_ECB = ["Monetary Policy Decision", "Press Conference Statement", "Account of Monetary Policy Meeting", "Governing Council Speech"]
MOCK_CB_ISSUING_BODIES = ["Federal Reserve", "ECB"]

MOCK_GEOPOL_EVENT_TYPES = ["Trade Deal Signed", "Sanctions Imposed", "Election Results", "Civil Unrest", "Peace Treaty"]
MOCK_GEOPOL_REGIONS = ["North America", "Europe", "Asia-Pacific", "Middle East", "South America", "Africa"]

MOCK_SOCIAL_PLATFORMS = ["Twixxer", "ThreadBook"]
MOCK_SOCIAL_AUTHOR_PREFIX = ["User", "Trader", "Bot", "Analyst"]

# --- Helper Functions ---

def get_utc_now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')

def generate_random_date(start_date_str="2020-01-01", end_date_str="2023-12-31") -> datetime.date:
    start_date = datetime.date.fromisoformat(start_date_str)
    end_date = datetime.date.fromisoformat(end_date_str)
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return random_date

def generate_random_datetime(start_date_str="2020-01-01T00:00:00", end_date_str="2023-12-31T23:59:59") -> datetime.datetime:
    start_dt = datetime.datetime.fromisoformat(start_date_str)
    end_dt = datetime.datetime.fromisoformat(end_date_str)
    time_between_dts = end_dt - start_dt
    seconds_between_dts = int(time_between_dts.total_seconds())
    random_number_of_seconds = random.randrange(seconds_between_dts)
    random_dt = start_dt + datetime.timedelta(seconds=random_number_of_seconds)
    # Ensure it's timezone-aware UTC and formatted with 'Z'
    if random_dt.tzinfo is None:
        random_dt = random_dt.replace(tzinfo=datetime.timezone.utc)
    else:
        random_dt = random_dt.astimezone(datetime.timezone.utc)
    return random_dt.isoformat(timespec='milliseconds').replace('+00:00', 'Z')

def generate_cik() -> str:
    return str(random.randint(100000, 2000000)).zfill(10)

def generate_accession_number(cik: str) -> str:
    return f"{cik}-{random.randint(20,23)}-{str(random.randint(1,999999)).zfill(6)}"

# --- Mock Data Generation Functions ---

import logging
from faker import Faker # Ensure Faker is imported
from faker.exceptions import UniquenessException # Import the exception

# fake = Faker() # This should be at the module level if used by other functions not shown,
                 # or passed around. Assuming it's defined globally as before.
                 # If 'fake' was defined at the very top of the file, this line isn't needed here.
                 # For safety, ensure 'fake' is accessible. If it was defined as:
                 # from faker import Faker
                 # fake = Faker()
                 # at the top, that's fine.

def generate_mock_asset_list(num_assets: int = 0) -> list[dict]:
    """Generates a list of mock assets. If num_assets is 0, uses MOCK_TICKERS."""
    assets = []
    tickers_to_use = []
    if num_assets == 0:
        tickers_to_use = MOCK_TICKERS
    else:
        generated_tickers = set()
        for i in range(num_assets):
            attempts = 0
            ticker = ""
            while attempts < 50:
                try:
                    if attempts < 10:
                        # These might still exhaust if called many times for many assets
                        # For a robust solution with many assets, a non-Faker unique part might be better
                        part1 = fake.unique.company_suffix().upper()
                        part2 = fake.unique.cryptocurrency_code()
                        ticker = (part1 + part2)[:10]
                    elif attempts < 25:
                        ticker = fake.unique.lexify(text='?????').upper() # Increased lexify length
                    else:
                        ticker = f"GEN{i:03d}{fake.lexify(text='???').upper()}" # Increased lexify length

                    if ticker not in generated_tickers:
                        generated_tickers.add(ticker)
                        tickers_to_use.append(ticker)
                        break
                except UniquenessException:
                    logging.debug(f"UniquenessException for asset {i}, attempt {attempts}. Clearing all unique and retrying.")
                    fake.unique.clear()
                except Exception as e:
                    logging.error(f"Error during ticker generation for asset {i}, attempt {attempts}: {e}")
                    break
                attempts += 1

            if ticker not in generated_tickers:
                fallback_ticker = f"MOCK{i:04d}"
                idx = 0
                while fallback_ticker in generated_tickers:
                    fallback_ticker = f"MOCK{i:04d}_{idx}"
                    idx += 1
                generated_tickers.add(fallback_ticker)
                tickers_to_use.append(fallback_ticker)
                logging.info(f"Used fallback ticker generation for asset index {i}: {fallback_ticker}")

        fake.unique.clear()

    for i, ticker_val in enumerate(tickers_to_use):
        assets.append({
            "asset_id": i + 1,
            "ticker_symbol": ticker_val,
            "company_name": MOCK_COMPANY_NAMES.get(ticker_val, fake.company()),
            "asset_class": random.choice(MOCK_ASSET_CLASSES),
            "exchange": random.choice(MOCK_EXCHANGES),
            "first_seen_date": generate_random_date("2000-01-01", "2010-01-01").isoformat(),
            "last_seen_date": None
        })
    return assets

def generate_mock_sp500_constituents(assets: list[dict], num_constituents: int = 5) -> list[dict]:
    """Generates mock S&P 500 constituents from the provided asset list."""
    constituents = []
    selected_assets = random.sample(assets, min(num_constituents, len(assets)))
    for asset in selected_assets:
        start_date = generate_random_date("2010-01-01", "2018-01-01")
        end_date = None
        if random.random() < 0.2: # 20% chance of not being a current constituent
            end_date = generate_random_date(start_date.isoformat(), "2022-12-31").isoformat()

        constituents.append({
            "constituent_id": fake.unique.random_int(),
            "universe_name": "S&P 500 Mock", # Link to a predefined universe name
            "ticker_symbol": asset["ticker_symbol"], # Link by ticker for simplicity here
            "asset_id": asset["asset_id"],
            "start_date": start_date.isoformat(),
            "end_date": end_date,
            "ingestion_timestamp": get_utc_now(),
            "source": "EODHD_mock"
        })
    return constituents

def generate_mock_daily_prices(asset_id: int, ticker: str, start_date_str: str, end_date_str: str) -> list[dict]:
    """Generates mock daily OHLCV prices for a single asset."""
    prices = []
    current_date = datetime.date.fromisoformat(start_date_str)
    end_date = datetime.date.fromisoformat(end_date_str)

    # Start with a random base price for the period
    base_price = random.uniform(50, 500)

    while current_date <= end_date:
        if current_date.weekday() < 5: # Monday to Friday
            open_price = round(base_price + random.uniform(-base_price * 0.02, base_price * 0.02), 4) # +/- 2%
            high_price = round(open_price + random.uniform(0, base_price * 0.015), 4)
            low_price = round(open_price - random.uniform(0, base_price * 0.015), 4)
            if low_price > open_price : low_price = open_price # ensure low <= open
            if high_price < open_price: high_price = open_price # ensure high >= open

            close_price = round(random.uniform(low_price, high_price), 4)
            volume = random.randint(100000, 10000000)
            vwap = round(random.uniform(low_price, high_price), 4) # simplified VWAP

            prices.append({
                "asset_id": asset_id,
                "ticker_symbol": ticker, # For easier identification in mock data
                "trade_date": current_date.isoformat(),
                "open_price": open_price,
                "high_price": high_price,
                "low_price": low_price,
                "close_price": close_price,
                "adjusted_close_price": close_price, # Simplification: not calculating adjustments
                "volume": volume,
                "vwap": vwap,
                "ingestion_timestamp": get_utc_now(),
                "source": "PolygonIO_mock"
            })
            # Next day's base price is based on today's close
            base_price = close_price * (1 + random.uniform(-0.025, 0.025)) # price drift
            if base_price <=0 : base_price = 0.01 # avoid negative or zero price
        current_date += datetime.timedelta(days=1)
    return prices

def generate_mock_corporate_actions(asset_id: int, ticker: str, num_actions: int = 2) -> list[dict]:
    """Generates mock corporate actions for a single asset."""
    actions = []
    for _ in range(num_actions):
        action_type = random.choice(["Dividend", "Split"])
        declaration_date = generate_random_date("2021-01-01", "2023-06-01")
        ex_date = declaration_date + datetime.timedelta(days=random.randint(5, 20))
        record_date = ex_date + datetime.timedelta(days=random.randint(1, 5))
        payable_date = record_date + datetime.timedelta(days=random.randint(10, 30))

        action = {
            "action_id": fake.unique.random_int(),
            "asset_id": asset_id,
            "ticker_symbol": ticker,
            "action_type": action_type,
            "ex_date": ex_date.isoformat(),
            "record_date": record_date.isoformat(),
            "payable_date": payable_date.isoformat(),
            "declaration_date": declaration_date.isoformat(),
            "ingestion_timestamp": get_utc_now(),
            "source": "PolygonIO_mock"
        }
        if action_type == "Dividend":
            action["value_ratio"] = round(random.uniform(0.1, 2.5), 4)
            action["value_currency"] = "USD"
        elif action_type == "Split":
            split_ratios = [2, 3, 0.5, 1.5] # e.g. 2 for 2-for-1, 0.5 for 1-for-2
            action["value_ratio"] = random.choice(split_ratios)
            action["value_currency"] = None
        actions.append(action)
    return actions

def generate_mock_economic_event_types(num_types: int = 0) -> list[dict]:
    event_types = []
    names_to_use = MOCK_ECONOMIC_EVENT_NAMES if num_types == 0 else [fake.bs().title() + " Indicator" for _ in range(num_types)]
    for i, name in enumerate(names_to_use):
        event_types.append({
            "event_type_id": i + 1,
            "event_name": name,
            "country_region": random.choice(MOCK_EVENT_COUNTRIES),
            "release_frequency": random.choice(["Monthly", "Quarterly", "Ad-hoc"]),
            "description": fake.sentence(),
            "source_identifier": name.upper().replace(" ", "_") + "_MOCKID"
        })
    return event_types

def generate_mock_economic_events(event_types: list[dict], num_events_per_type: int = 5) -> list[dict]:
    events = []
    for etype in event_types:
        for _ in range(num_events_per_type):
            release_dt = generate_random_datetime("2022-01-01T08:00:00", "2023-12-31T17:00:00")
            actual = round(random.uniform(-5, 10) if "%" in etype["event_name"] else random.uniform(100, 10000), 2)
            consensus = round(actual + random.uniform(-abs(actual*0.1), abs(actual*0.1)), 2) # consensus around actual
            previous = round(actual * (1 + random.uniform(-0.05, 0.05)), 2)

            # release_dt is now an ISO string from generate_random_datetime
            dt_object_for_formatting = datetime.datetime.fromisoformat(release_dt.replace('Z','+00:00'))
            events.append({
                "event_id": fake.unique.random_int(),
                "event_type_id": etype["event_type_id"],
                "event_name": etype["event_name"], # for easier identification
                "release_datetime_utc": release_dt, # Use the string directly
                "period_covered": f"{dt_object_for_formatting.strftime('%B %Y')}",
                "actual_value": actual,
                "consensus_value_pit": consensus,
                "previous_value": previous,
                "revised_previous_value": None if random.random() < 0.8 else round(previous * (1 + random.uniform(-0.01, 0.01)), 2),
                "unit": random.choice(MOCK_EVENT_UNITS),
                "ingestion_timestamp": get_utc_now(),
                "source": "Econoday_mock"
            })
    return events

def generate_mock_sec_filing_types() -> list[dict]:
    return [{"filing_type_id": i+1, "form_type": ft, "description": f"SEC Form {ft}"} for i, ft in enumerate(MOCK_SEC_FORM_TYPES)]

def generate_mock_sec_filings_metadata(assets: list[dict], filing_types: list[dict], num_filings: int = 10) -> list[dict]:
    filings = []
    for _ in range(num_filings):
        asset = random.choice(assets)
        filing_type = random.choice(filing_types)
        _cik = generate_cik()
        _acc_num = generate_accession_number(_cik)
        filing_date = generate_random_date("2022-01-01", "2023-12-01")

        filings.append({
            "filing_id": fake.unique.random_int(),
            "asset_id": asset["asset_id"],
            "ticker_symbol": asset["ticker_symbol"], # for easier identification
            "cik": _cik,
            "filing_type_id": filing_type["filing_type_id"],
            "form_type": filing_type["form_type"], # for easier identification
            "filing_date": filing_date.isoformat(),
            "period_of_report": (filing_date - datetime.timedelta(days=random.randint(30,90))).isoformat() if "10-K" in filing_type["form_type"] or "10-Q" in filing_type["form_type"] else None,
            "accession_number": _acc_num,
            "raw_text_s3_path": f"s3://mock-bucket/raw_data/corporate_filings/sec_api_io_mock/raw_text/{_cik}/{filing_type['form_type']}/{_acc_num}.txt",
            "structured_json_s3_path": f"s3://mock-bucket/raw_data/corporate_filings/sec_api_io_mock/structured_json/{_cik}/{filing_type['form_type']}/{_acc_num}.json",
            "ingestion_timestamp": get_utc_now(),
            "source": "SECApi_mock"
        })
    return filings

def generate_mock_news_sources() -> list[dict]:
    return [{"news_source_id": i+1, "source_name": name, "website": f"https://www.{name.lower().replace(' ', '')}.mock"} for i, name in enumerate(MOCK_NEWS_SOURCES)]

def generate_mock_news_articles(assets: list[dict], news_sources: list[dict], economic_event_types: list[dict], num_articles: int = 20) -> list[dict]:
    articles = []
    for _ in range(num_articles):
        source = random.choice(news_sources)
        publish_dt = generate_random_datetime("2022-01-01T00:00:00", "2023-12-31T23:59:59")

        # Make headline relevant
        headline_type = random.choice(["ticker", "event", "general"])
        tickers_mentioned = []
        headline = "Generic Market News Update"

        if headline_type == "ticker" and assets:
            asset = random.choice(assets)
            tickers_mentioned.append(asset["ticker_symbol"])
            headline = random.choice(MOCK_NEWS_HEADLINE_TEMPLATES).format(
                ticker=asset["ticker_symbol"],
                company_name=asset["company_name"],
                movement=random.choice(NEWS_MOVEMENTS),
                reason=random.choice(NEWS_REASONS),
                opinion=random.choice(NEWS_OPINIONS),
                event_name = "", # not used in this branch
                reaction = "", # not used in this branch
                random_event_summary = fake.bs().title()
            )
        elif headline_type == "event" and economic_event_types:
            event_type = random.choice(economic_event_types)
            headline = random.choice(MOCK_NEWS_HEADLINE_TEMPLATES).format(
                ticker="", company_name="", movement="", reason="", opinion="", # not used
                event_name=event_type["event_name"],
                reaction=random.choice(NEWS_REACTIONS),
                random_event_summary = fake.bs().title()
            )
        else: # general
             headline = random.choice(MOCK_NEWS_HEADLINE_TEMPLATES).format(
                ticker="Market", company_name="Economy", movement=random.choice(NEWS_MOVEMENTS), reason=random.choice(NEWS_REASONS), opinion=random.choice(NEWS_OPINIONS),
                event_name="Global Developments", reaction=random.choice(NEWS_REACTIONS),
                random_event_summary = fake.bs().title()
             )


        article_guid = str(uuid.uuid4())
        # publish_dt is now an ISO string
        dt_object_for_formatting = datetime.datetime.fromisoformat(publish_dt.replace('Z','+00:00'))
        articles.append({
            "article_id": fake.unique.random_int(),
            "news_source_id": source["news_source_id"],
            "source_name": source["source_name"], # for easier identification
            "article_url": f"{source['website']}/news/{article_guid}",
            "headline": headline,
            "publish_timestamp_utc": publish_dt, # Use the string directly
            "tickers_mentioned": tickers_mentioned,
            "raw_text_s3_path": f"s3://mock-bucket/raw_data/news_data/{source['source_name'].replace(' ','_').lower()}_mock/{dt_object_for_formatting.strftime('%Y/%m/%d')}/{article_guid}.txt",
            "body_text_sample": "\n".join(fake.paragraphs(nb=3)), # Sample for quick view
            "ingestion_timestamp": get_utc_now(),
            "source_api": f"{source['source_name'].replace(' ','_')}_mock"
        })
    return articles

def generate_mock_cb_doc_types() -> list[dict]:
    doc_types = []
    idx = 1
    for name in MOCK_CB_DOC_TYPES_FED:
        doc_types.append({"doc_type_id": idx, "doc_type_name": name, "issuing_body": "Federal Reserve"})
        idx += 1
    for name in MOCK_CB_DOC_TYPES_ECB:
        doc_types.append({"doc_type_id": idx, "doc_type_name": name, "issuing_body": "ECB"})
        idx += 1
    return doc_types

def generate_mock_cb_documents(doc_types: list[dict], num_docs: int = 10) -> list[dict]:
    docs = []
    for _ in range(num_docs):
        doc_type = random.choice(doc_types)
        publish_dt = generate_random_datetime("2022-01-01T00:00:00", "2023-12-31T23:59:59")
        doc_guid = str(uuid.uuid4())
        # publish_dt is now an ISO string
        dt_object_for_formatting = datetime.datetime.fromisoformat(publish_dt.replace('Z','+00:00'))

        docs.append({
            "document_id": fake.unique.random_int(),
            "doc_type_id": doc_type["doc_type_id"],
            "doc_type_name": doc_type["doc_type_name"], # for easier identification
            "issuing_body": doc_type["issuing_body"], # for easier identification
            "publish_timestamp_utc": publish_dt, # Use the string directly
            "title": f"{doc_type['doc_type_name']}: {fake.bs().title()}",
            "speaker_author": fake.name() if "Speech" in doc_type["doc_type_name"] else None,
            "raw_text_s3_path": f"s3://mock-bucket/raw_data/central_bank_communications/{doc_type['issuing_body'].lower()}_scraper_mock/{dt_object_for_formatting.strftime('%Y/%m/%d')}/{doc_guid}.txt",
            "document_url": f"https://www.{doc_type['issuing_body'].lower()}.mock/releases/{doc_guid}",
            "text_sample": "\n".join(fake.paragraphs(nb=2)), # Sample
            "ingestion_timestamp": get_utc_now(),
            "source": f"{doc_type['issuing_body'].replace(' ','')}Scraper_mock"
        })
    return docs

def generate_mock_geopol_sources() -> list[dict]:
    return [{"geopol_source_id": 1, "source_name": "GDELT_mock"}, {"geopol_source_id": 2, "source_name": "ManualCuration_mock"}]

def generate_mock_geopol_events(sources: list[dict], assets: list[dict], num_events: int = 15) -> list[dict]:
    events = []
    for _ in range(num_events):
        source = random.choice(sources)
        event_dt = generate_random_datetime("2022-01-01T00:00:00", "2023-12-31T23:59:59") # now a string
        affected_tickers = []
        if assets and random.random() < 0.3: # 30% chance of being linked to specific assets
            affected_tickers = [a["ticker_symbol"] for a in random.sample(assets, k=min(len(assets), random.randint(1,3)))]

        events.append({
            "geopol_event_id": fake.unique.random_int(),
            "geopol_source_id": source["geopol_source_id"],
            "source_name": source["source_name"], # for easier identification
            "event_timestamp_utc": event_dt, # Use string directly
            "country_region_involved": random.choice(MOCK_GEOPOL_REGIONS),
            "event_type": random.choice(MOCK_GEOPOL_EVENT_TYPES),
            "description": fake.sentence(nb_words=15),
            "relevance_score": round(random.uniform(0.1, 1.0), 2) if source["source_name"] == "GDELT_mock" else round(random.uniform(0.5,1.0),1),
            "affected_assets_tickers": affected_tickers,
            "ingestion_timestamp": get_utc_now()
        })
    return events

def generate_mock_social_platforms() -> list[dict]:
    return [{"platform_id": i+1, "platform_name": name} for i, name in enumerate(MOCK_SOCIAL_PLATFORMS)]

def generate_mock_social_posts(platforms: list[dict], assets: list[dict], num_posts: int = 50) -> list[dict]:
    posts = []
    for _ in range(num_posts):
        platform = random.choice(platforms)
        publish_dt = generate_random_datetime("2023-01-01T00:00:00", "2023-12-31T23:59:59") # now a string
        dt_object_for_formatting = datetime.datetime.fromisoformat(publish_dt.replace('Z','+00:00'))

        text_content = fake.sentence(nb_words=random.randint(5, 25))
        tickers_mentioned = []
        hashtags = []

        if assets and random.random() < 0.7: # 70% chance of mentioning a ticker
            asset = random.choice(assets)
            tickers_mentioned.append(asset["ticker_symbol"])
            text_content += f" ${asset['ticker_symbol']}"

        if random.random() < 0.5: # 50% chance of having hashtags
            for _ in range(random.randint(1,3)):
                ht = "#" + fake.word().lower()
                hashtags.append(ht)
                text_content += f" {ht}"

        post_guid = str(uuid.uuid4())
        posts.append({
            "post_id": fake.unique.random_int(),
            "platform_id": platform["platform_id"],
            "platform_name": platform["platform_name"], # for easier identification
            "post_guid": post_guid,
            "author_guid": random.choice(MOCK_SOCIAL_AUTHOR_PREFIX) + str(random.randint(1000,99999)),
            "publish_timestamp_utc": publish_dt, # Use string directly
            "post_text": text_content,
            "tickers_mentioned": tickers_mentioned,
            "hashtags": hashtags,
            "like_count": random.randint(0, 1000),
            "retweet_reply_count": random.randint(0, 200),
            "sentiment_score": round(random.uniform(-1,1), 4), # Mock pre-calculated sentiment
            "sentiment_label": random.choice(["Positive", "Negative", "Neutral"]),
            "raw_json_s3_path": f"s3://mock-bucket/raw_data/social_media_data/{platform['platform_name'].lower()}_mock/live_api_stream/{dt_object_for_formatting.strftime('%Y/%m/%d/%H')}/{post_guid}.json",
            "ingestion_timestamp": get_utc_now(),
            "source_collection_method": f"{platform['platform_name']}_API_mock"
        })
    return posts

if __name__ == '__main__':
    # Example usage:
    assets = generate_mock_asset_list()
    print(f"Generated {len(assets)} mock assets.")
    print(json.dumps(assets[:2], indent=2))

    constituents = generate_mock_sp500_constituents(assets, num_constituents=3)
    print(f"\nGenerated {len(constituents)} mock S&P500 constituents.")
    print(json.dumps(constituents, indent=2))

    daily_prices = generate_mock_daily_prices(assets[0]['asset_id'], assets[0]['ticker_symbol'], "2023-10-01", "2023-10-05")
    print(f"\nGenerated {len(daily_prices)} mock daily prices for {assets[0]['ticker_symbol']}.")
    print(json.dumps(daily_prices, indent=2))

    actions = generate_mock_corporate_actions(assets[0]['asset_id'], assets[0]['ticker_symbol'], num_actions=1)
    print(f"\nGenerated {len(actions)} mock corporate actions for {assets[0]['ticker_symbol']}.")
    print(json.dumps(actions, indent=2))

    econ_event_types = generate_mock_economic_event_types()
    print(f"\nGenerated {len(econ_event_types)} mock economic event types.")
    print(json.dumps(econ_event_types[:2], indent=2))

    econ_events = generate_mock_economic_events(econ_event_types, num_events_per_type=1)
    print(f"\nGenerated {len(econ_events)} mock economic events.")
    print(json.dumps(econ_events[:2], indent=2))

    sec_filing_types = generate_mock_sec_filing_types()
    print(f"\nGenerated {len(sec_filing_types)} mock SEC filing types.")
    print(json.dumps(sec_filing_types[:2], indent=2))

    sec_filings = generate_mock_sec_filings_metadata(assets, sec_filing_types, num_filings=2)
    print(f"\nGenerated {len(sec_filings)} mock SEC filings metadata.")
    print(json.dumps(sec_filings, indent=2))

    news_sources = generate_mock_news_sources()
    print(f"\nGenerated {len(news_sources)} mock news sources.")
    print(json.dumps(news_sources[:2], indent=2))

    news_articles = generate_mock_news_articles(assets, news_sources, econ_event_types, num_articles=3)
    print(f"\nGenerated {len(news_articles)} mock news articles.")
    print(json.dumps(news_articles, indent=2))

    cb_doc_types = generate_mock_cb_doc_types()
    print(f"\nGenerated {len(cb_doc_types)} mock CB document types.")
    print(json.dumps(cb_doc_types[:2], indent=2))

    cb_docs = generate_mock_cb_documents(cb_doc_types, num_docs=2)
    print(f"\nGenerated {len(cb_docs)} mock CB documents.")
    print(json.dumps(cb_docs, indent=2))

    geopol_sources = generate_mock_geopol_sources()
    print(f"\nGenerated {len(geopol_sources)} mock geopolitical sources.")
    print(json.dumps(geopol_sources, indent=2))

    geopol_events = generate_mock_geopol_events(geopol_sources, assets, num_events=2)
    print(f"\nGenerated {len(geopol_events)} mock geopolitical events.")
    print(json.dumps(geopol_events, indent=2))

    social_platforms = generate_mock_social_platforms()
    print(f"\nGenerated {len(social_platforms)} mock social media platforms.")
    print(json.dumps(social_platforms, indent=2))

    social_posts = generate_mock_social_posts(social_platforms, assets, num_posts=3)
    print(f"\nGenerated {len(social_posts)} mock social media posts.")
    print(json.dumps(social_posts, indent=2))

    print("\nMock data generator module created and tested.")
