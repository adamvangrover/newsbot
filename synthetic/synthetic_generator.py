import datetime
import random
import uuid
from typing import List, Dict, Any, Tuple
import pandas as pd
from faker import Faker

from .pydantic_models import (
    Asset, AssetUniverse, AssetConstituent, EquityDailyPrice,
    NewsArticleMetadata, SECFilingMetadata, EconomicEvent
)
from utils import mock_data_generator as mock_gen

fake = Faker()

class SyntheticDataEngine:
    def __init__(self, start_date: datetime.date, end_date: datetime.date, num_assets: int = 20):
        self.start_date = start_date
        self.end_date = end_date
        self.num_assets = num_assets
        self.assets: List[Asset] = []
        self.universe: AssetUniverse = None
        self.constituents: List[AssetConstituent] = []
        self.market_state: Dict[str, float] = {} # Ticker -> Current Price
        self.generated_data: Dict[str, List[Any]] = {
            "assets": [],
            "equity_daily_prices": [],
            "news_articles_metadata": [],
            "sec_filings_metadata": [],
            "economic_events": []
        }
        self.news_sources = mock_gen.generate_mock_news_sources()
        self.econ_event_types = mock_gen.generate_mock_economic_event_types()
        self.sec_filing_types = mock_gen.generate_mock_sec_filing_types()

    def initialize_market(self):
        """Initializes assets and initial prices."""
        # Generate Assets
        mock_assets = mock_gen.generate_mock_asset_list(self.num_assets)
        self.assets = [Asset(**a) for a in mock_assets]
        self.generated_data["assets"] = self.assets

        # Create a Universe
        self.universe = AssetUniverse(
            universe_id=1,
            universe_name="Synthetic Index 20",
            description="Top 20 Synthetic Assets"
        )

        # Create Constituents
        for asset in self.assets:
            self.constituents.append(AssetConstituent(
                constituent_id=fake.unique.random_int(),
                universe_id=self.universe.universe_id,
                asset_id=asset.asset_id,
                start_date=self.start_date,
                ingestion_timestamp=datetime.datetime.now(datetime.timezone.utc)
            ))

        # Initialize Prices
        for asset in self.assets:
            self.market_state[asset.ticker_symbol] = random.uniform(50, 500)

    def generate_day(self, current_date: datetime.date):
        """Generates data for a single day, ensuring consistency."""
        day_events = self._generate_daily_scenarios(current_date)

        # Generate News and determine price impacts
        daily_news, price_impacts = self._generate_news_and_impacts(current_date, day_events)
        self.generated_data["news_articles_metadata"].extend(daily_news)

        # Generate Prices
        daily_prices = self._generate_prices(current_date, price_impacts)
        self.generated_data["equity_daily_prices"].extend(daily_prices)

        # Generate Filings (Independent mostly, but can be linked)
        daily_filings = self._generate_filings(current_date)
        self.generated_data["sec_filings_metadata"].extend(daily_filings)

    def _generate_daily_scenarios(self, current_date: datetime.date) -> List[Dict]:
        """Decides if any major market scenarios happen today."""
        scenarios = []
        # Randomly trigger a "Market Shock" or specific event
        if random.random() < 0.05: # 5% chance of a market-wide event
            event_type = random.choice(["Crash", "Boom", "RateHike", "TechRally"])
            scenarios.append({"type": "MarketEvent", "name": event_type})
        return scenarios

    def _generate_news_and_impacts(self, current_date: datetime.date, scenarios: List[Dict]) -> Tuple[List[NewsArticleMetadata], Dict[str, float]]:
        """
        Generates news articles and calculates their impact on specific tickers.
        Returns (List of NewsArticleMetadata, Dict[Ticker, PctChange])
        """
        news_items = []
        price_impacts = {a.ticker_symbol: 0.0 for a in self.assets}

        # Apply Scenario Impacts
        for scenario in scenarios:
            headline = f"Market Alert: {scenario['name']} scenarios unfolding."
            impact_factor = 0.0
            if scenario['name'] == "Crash":
                impact_factor = -0.05
                headline = "Market Plunges as Sell-off Intensifies"
            elif scenario['name'] == "Boom":
                impact_factor = 0.03
                headline = "Markets Rally to New Highs"

            # Create a market-wide news item
            source = random.choice(self.news_sources)
            news_items.append(NewsArticleMetadata(
                article_id=fake.unique.random_int(),
                news_source_id=source['news_source_id'],
                headline=headline,
                publish_timestamp_utc=datetime.datetime.combine(current_date, datetime.time(9, 0), tzinfo=datetime.timezone.utc),
                tickers_mentioned=[],
                ingestion_timestamp=datetime.datetime.now(datetime.timezone.utc),
                sentiment_score=impact_factor * 20 # Rough scaling
            ))

            # Apply to all assets
            for ticker in price_impacts:
                price_impacts[ticker] += impact_factor + random.uniform(-0.01, 0.01)

        # Generate Idiosyncratic News (Company Specific)
        for asset in self.assets:
            if random.random() < 0.1: # 10% chance of news per asset per day
                sentiment_type = random.choice(["Positive", "Negative"])
                impact = random.uniform(0.02, 0.08) if sentiment_type == "Positive" else random.uniform(-0.08, -0.02)

                headline = f"{asset.company_name} reports {sentiment_type.lower()} outlook."
                if sentiment_type == "Positive":
                    headline = random.choice([
                        f"{asset.company_name} beats earnings expectations.",
                        f"{asset.company_name} announces breakthrough product.",
                        f"Analysts upgrade {asset.ticker_symbol} to Buy."
                    ])
                else:
                    headline = random.choice([
                        f"{asset.company_name} misses revenue targets.",
                        f"CEO of {asset.company_name} steps down amid controversy.",
                        f"{asset.ticker_symbol} faces regulatory scrutiny."
                    ])

                source = random.choice(self.news_sources)
                news_items.append(NewsArticleMetadata(
                    article_id=fake.unique.random_int(),
                    news_source_id=source['news_source_id'],
                    headline=headline,
                    publish_timestamp_utc=datetime.datetime.combine(current_date, datetime.time(random.randint(8, 16), random.randint(0, 59)), tzinfo=datetime.timezone.utc),
                    tickers_mentioned=[asset.ticker_symbol],
                    ingestion_timestamp=datetime.datetime.now(datetime.timezone.utc),
                    sentiment_score=impact * 20
                ))

                price_impacts[asset.ticker_symbol] += impact

        return news_items, price_impacts

    def _generate_prices(self, current_date: datetime.date, price_impacts: Dict[str, float]) -> List[EquityDailyPrice]:
        prices = []
        is_trading_day = current_date.weekday() < 5 # Simple Mon-Fri
        if not is_trading_day:
            return []

        for asset in self.assets:
            prev_close = self.market_state[asset.ticker_symbol]
            impact = price_impacts.get(asset.ticker_symbol, 0.0)

            # Random drift + Impact
            drift = random.uniform(-0.015, 0.015)
            change_pct = drift + impact

            open_price = round(prev_close * (1 + random.uniform(-0.005, 0.005)), 4)
            close_price = round(open_price * (1 + change_pct), 4)

            high_price = max(open_price, close_price) * (1 + random.uniform(0, 0.01))
            low_price = min(open_price, close_price) * (1 - random.uniform(0, 0.01))

            self.market_state[asset.ticker_symbol] = close_price

            prices.append(EquityDailyPrice(
                asset_id=asset.asset_id,
                ticker_symbol=asset.ticker_symbol,
                trade_date=current_date,
                open_price=round(open_price, 4),
                high_price=round(high_price, 4),
                low_price=round(low_price, 4),
                close_price=round(close_price, 4),
                adjusted_close_price=round(close_price, 4),
                volume=random.randint(50000, 5000000),
                ingestion_timestamp=datetime.datetime.now(datetime.timezone.utc),
                source="SyntheticEngine"
            ))

        return prices

    def _generate_filings(self, current_date: datetime.date) -> List[SECFilingMetadata]:
        filings = []
        # Rare event
        if random.random() < 0.05:
            asset = random.choice(self.assets)
            filing_type = random.choice(self.sec_filing_types)
            _cik = mock_gen.generate_cik()
            _acc_num = mock_gen.generate_accession_number(_cik)

            filings.append(SECFilingMetadata(
                filing_id=fake.unique.random_int(),
                asset_id=asset.asset_id,
                ticker_symbol=asset.ticker_symbol,
                cik=_cik,
                filing_type_id=filing_type['filing_type_id'],
                filing_date=current_date,
                accession_number=_acc_num,
                ingestion_timestamp=datetime.datetime.now(datetime.timezone.utc),
                source="SECApi_mock"
            ))
        return filings

    def run(self):
        self.initialize_market()
        delta = self.end_date - self.start_date
        print(f"Generating synthetic data from {self.start_date} to {self.end_date} ({delta.days} days)...")

        for i in range(delta.days + 1):
            current_date = self.start_date + datetime.timedelta(days=i)
            self.generate_day(current_date)

        return self.generated_data
