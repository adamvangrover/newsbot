import datetime
import random
import uuid
from typing import List, Dict, Any, Tuple, Optional
import pandas as pd
from faker import Faker

from .pydantic_models import (
    Asset, AssetUniverse, AssetConstituent, EquityDailyPrice,
    NewsArticleMetadata, SECFilingMetadata, EconomicEvent,
    CorporateAction, NewsSource, EconomicEventType, SECFilingType,
    CentralBankDocumentType, CentralBankDocument,
    GeopoliticalEventSource, GeopoliticalEvent,
    SocialMediaPlatform, SocialMediaPost
)
from utils import mock_data_generator as mock_gen
from semantic_narrative_library.processing.impact_analysis_engine import ImpactAnalyzer
from semantic_narrative_library.core_models.python.base_types import NarrativeEntity, NewsItem, PoliticalEvent

fake = Faker()

class SyntheticDataEngine:
    def __init__(self, start_date: datetime.date, end_date: datetime.date, num_assets: int = 20):
        self.start_date = start_date
        self.end_date = end_date
        self.num_assets = num_assets

        # Core Data Structures
        self.assets: List[Asset] = []
        self.universe: AssetUniverse = None
        self.constituents: List[AssetConstituent] = []

        # Market State
        self.market_state: Dict[str, float] = {} # Ticker -> Current Price
        self.active_scenarios: List[Dict] = []

        # Generated Data Container
        self.generated_data: Dict[str, List[Any]] = {
            "assets": [],
            "asset_universe": [], # Will contain just one for now
            "asset_constituents": [],
            "equity_daily_prices": [],
            "news_articles_metadata": [],
            "sec_filings_metadata": [],
            "economic_events": [],
            "corporate_actions": [],
            "news_sources": [],
            "economic_event_types": [],
            "sec_filing_types": [],
            "central_bank_documents": [],
            "geopolitical_events": [],
            "social_media_posts": []
        }

        # Metadata / Static Data
        self._initialize_metadata()

        # Engines
        self.impact_analyzer = ImpactAnalyzer()

    def _initialize_metadata(self):
        """Initializes static metadata (sources, types, etc.)"""
        self.news_sources = [NewsSource(**x) for x in mock_gen.generate_mock_news_sources()]
        self.generated_data["news_sources"] = self.news_sources

        self.econ_event_types = [EconomicEventType(**x) for x in mock_gen.generate_mock_economic_event_types(5)]
        self.generated_data["economic_event_types"] = self.econ_event_types

        self.sec_filing_types = [SECFilingType(**x) for x in mock_gen.generate_mock_sec_filing_types()]
        self.generated_data["sec_filing_types"] = self.sec_filing_types

        self.cb_doc_types = [CentralBankDocumentType(**x) for x in mock_gen.generate_mock_cb_doc_types()]
        # No direct table for types in pydantic/sql schema in output dict usually, but useful to keep handy

        self.geopol_sources = [GeopoliticalEventSource(**x) for x in mock_gen.generate_mock_geopol_sources()]

        self.social_platforms = [SocialMediaPlatform(**x) for x in mock_gen.generate_mock_social_platforms()]

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
        self.generated_data["asset_universe"] = [self.universe]

        # Create Constituents
        for asset in self.assets:
            const = AssetConstituent(
                constituent_id=fake.unique.random_int(),
                universe_id=self.universe.universe_id,
                asset_id=asset.asset_id,
                start_date=self.start_date,
                ingestion_timestamp=datetime.datetime.now(datetime.timezone.utc),
                source="SyntheticEngine"
            )
            self.constituents.append(const)
            self.generated_data["asset_constituents"].append(const)

        # Initialize Prices
        for asset in self.assets:
            self.market_state[asset.ticker_symbol] = random.uniform(50, 500)

    def generate_day(self, current_date: datetime.date):
        """Generates data for a single day, ensuring consistency."""
        is_trading_day = current_date.weekday() < 5

        # 1. Update/Generate Active Scenarios (The "Signal")
        daily_scenario_impacts = self._process_scenarios(current_date)

        # 2. Generate Economic Events
        self._generate_economic_events(current_date)

        # 3. Generate Geopolitical Events (External Drivers)
        geopol_events = self._generate_geopolitical_events(current_date)
        self.generated_data["geopolitical_events"].extend(geopol_events)

        # 4. Trace impacts from Geopolitical Events
        geopol_impacts = self._trace_geopol_impacts(geopol_events)

        # Merge Impacts
        combined_impacts = self._merge_impacts(daily_scenario_impacts, geopol_impacts)

        # 5. Generate News (Signal + Noise)
        daily_news, price_sentiment_impacts = self._generate_news(current_date, combined_impacts)
        self.generated_data["news_articles_metadata"].extend(daily_news)

        # 6. Generate Prices
        if is_trading_day:
            daily_prices = self._generate_prices(current_date, price_sentiment_impacts)
            self.generated_data["equity_daily_prices"].extend(daily_prices)

        # 7. Generate Other Data (Filings, Corporate Actions, Social Media, CB Docs)
        self._generate_auxiliary_data(current_date)

    def _process_scenarios(self, current_date: datetime.date) -> Dict[str, float]:
        """
        Manages long-running scenarios and generates daily impacts.
        Returns a dictionary of Ticker -> Price Impact %
        """
        impacts = {}

        # Chance to start a new scenario
        if random.random() < 0.02: # 2% chance per day of a new major narrative
            scenario_type = random.choice(["TechBreakthrough", "SupplyChainCrisis", "InflationSpike"])
            self.active_scenarios.append({
                "type": scenario_type,
                "start_date": current_date,
                "duration": random.randint(5, 20),
                "day_count": 0,
                "intensity": random.uniform(0.5, 1.5)
            })

        # Process active scenarios
        active_to_keep = []
        for scenario in self.active_scenarios:
            scenario["day_count"] += 1
            if scenario["day_count"] > scenario["duration"]:
                continue

            # Calculate impact for this day
            # Decay intensity over time or have a peak
            progress = scenario["day_count"] / scenario["duration"]
            daily_intensity = scenario["intensity"] * (1 - abs(progress - 0.5) * 2) # Peak in middle

            if scenario["type"] == "TechBreakthrough":
                # Impact Tech stocks positively
                for asset in self.assets:
                    if asset.asset_class == "Equity": # Simplified check, ideally check sector
                        # Assume some assets are tech
                        if hash(asset.ticker_symbol) % 3 == 0: # Random subset
                            impacts[asset.ticker_symbol] = impacts.get(asset.ticker_symbol, 0) + (0.02 * daily_intensity)

            elif scenario["type"] == "SupplyChainCrisis":
                # Impact all negatively, some more than others
                for asset in self.assets:
                     impacts[asset.ticker_symbol] = impacts.get(asset.ticker_symbol, 0) - (0.015 * daily_intensity)

            elif scenario["type"] == "InflationSpike":
                # General negative drag
                for asset in self.assets:
                    impacts[asset.ticker_symbol] = impacts.get(asset.ticker_symbol, 0) - (0.01 * daily_intensity)

            active_to_keep.append(scenario)

        self.active_scenarios = active_to_keep
        return impacts

    def _trace_geopol_impacts(self, events: List[GeopoliticalEvent]) -> Dict[str, float]:
        """
        Uses ImpactAnalyzer to trace impacts from geopolitical events to assets.
        """
        impacts = {}
        for event in events:
            # Create a NarrativeEntity for the event to pass to ImpactAnalyzer
            # Using a simplified mapping since we don't have a full KG loaded here
            narrative_event = PoliticalEvent(
                id=f"geopol_{event.geopol_event_id}",
                name=event.event_type or "Unknown Event",
                type="PoliticalEvent",
                event_subtype=event.event_type,
                location=event.country_region_involved,
                attributes={"description": event.description}
            )

            # Trace Impacts
            # In a real system, we'd pass the full KG. Here we pass None or a mock
            # The ImpactAnalyzer is currently simulated, so it works with mock data internally
            chains = self.impact_analyzer.trace_impacts(
                initial_event_entity=narrative_event,
                knowledge_graph=None,
                depth_levels=2
            )

            for chain in chains:
                impact_type = chain.get("impact_type")
                magnitude = chain.get("magnitude") # Low, Medium, High

                # Convert magnitude to float
                mag_score = 0.005 # Low
                if magnitude == "Medium": mag_score = 0.015
                elif magnitude == "High": mag_score = 0.03

                # Determine sign based on impact type (naive heuristic)
                if "Risk" in impact_type or "Delay" in impact_type or "Negative" in impact_type:
                    mag_score *= -1

                # Apply to random assets (since we don't have the real Entity Resolution to Ticker map yet)
                # In a real system, 'impacted_entity_id' would map to an asset_id
                num_affected = random.randint(1, 3)
                affected_assets = random.sample(self.assets, min(num_affected, len(self.assets)))

                for asset in affected_assets:
                    impacts[asset.ticker_symbol] = impacts.get(asset.ticker_symbol, 0) + mag_score

        return impacts

    def _merge_impacts(self, *impact_dicts) -> Dict[str, float]:
        merged = {}
        for d in impact_dicts:
            for k, v in d.items():
                merged[k] = merged.get(k, 0.0) + v
        return merged

    def _generate_news(self, current_date: datetime.date, impacts: Dict[str, float]) -> Tuple[List[NewsArticleMetadata], Dict[str, float]]:
        """
        Generates news articles.
        1. Explains the 'Signal' (Impacts) with generated headlines.
        2. Adds 'Noise' (Random headlines with low/no impact).
        """
        news = []
        final_impacts = impacts.copy() # Start with the calculated impacts

        # 1. Generate Signal News (Explaining the price moves)
        for ticker, impact in impacts.items():
            if abs(impact) < 0.005: continue # Ignore small moves

            asset = next((a for a in self.assets if a.ticker_symbol == ticker), None)
            if not asset: continue

            sentiment = "Positive" if impact > 0 else "Negative"
            headline = ""

            if sentiment == "Positive":
                headline = random.choice([
                    f"{asset.company_name} surges on positive outlook.",
                    f"Analysts predict strong growth for {ticker}.",
                    f"{asset.company_name} announces strategic partnership."
                ])
            else:
                headline = random.choice([
                    f"{asset.company_name} faces headwinds.",
                    f"Regulatory concerns hit {ticker}.",
                    f"{asset.company_name} misses key targets."
                ])

            source = random.choice(self.news_sources)
            news.append(NewsArticleMetadata(
                article_id=fake.unique.random_int(),
                news_source_id=source.news_source_id,
                headline=headline,
                publish_timestamp_utc=datetime.datetime.combine(current_date, datetime.time(random.randint(8, 16), random.randint(0, 59)), tzinfo=datetime.timezone.utc),
                tickers_mentioned=[ticker],
                ingestion_timestamp=datetime.datetime.now(datetime.timezone.utc),
                source_api="SyntheticEngine_Signal",
                sentiment_score=impact * 10 # Scale up for sentiment score
            ))

        # 2. Generate Noise News
        # Random chatter, no real impact
        num_noise = random.randint(2, 5)
        for _ in range(num_noise):
            source = random.choice(self.news_sources)
            noise_type = random.choice(["Repurpose", "Opinion", "Rumor"])

            headline = ""
            ticker = None

            if random.random() < 0.5:
                asset = random.choice(self.assets)
                ticker = asset.ticker_symbol
                headline = f"Opinion: Is {ticker} a buy right now?"
            else:
                headline = "Market stays watchful ahead of data."

            news.append(NewsArticleMetadata(
                article_id=fake.unique.random_int(),
                news_source_id=source.news_source_id,
                headline=headline,
                publish_timestamp_utc=datetime.datetime.combine(current_date, datetime.time(random.randint(6, 20), random.randint(0, 59)), tzinfo=datetime.timezone.utc),
                tickers_mentioned=[ticker] if ticker else [],
                ingestion_timestamp=datetime.datetime.now(datetime.timezone.utc),
                source_api="SyntheticEngine_Noise",
                sentiment_score=random.uniform(-0.1, 0.1) # Low sentiment
            ))

        return news, final_impacts

    def _generate_prices(self, current_date: datetime.date, impacts: Dict[str, float]) -> List[EquityDailyPrice]:
        prices = []
        for asset in self.assets:
            prev_close = self.market_state[asset.ticker_symbol]
            impact = impacts.get(asset.ticker_symbol, 0.0)

            # Random drift (market noise) + Systematic Impact
            drift = random.uniform(-0.01, 0.01)
            change_pct = drift + impact

            # Ensure we don't go to zero or negative easily
            if prev_close * (1 + change_pct) <= 0:
                change_pct = 0

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

    def _generate_economic_events(self, current_date: datetime.date):
        if random.random() < 0.1: # 10% chance
            etype = random.choice(self.econ_event_types)
            self.generated_data["economic_events"].append(EconomicEvent(
                event_id=fake.unique.random_int(),
                event_type_id=etype.event_type_id,
                release_datetime_utc=datetime.datetime.combine(current_date, datetime.time(10, 0), tzinfo=datetime.timezone.utc),
                period_covered="Previous Month",
                actual_value=random.uniform(100, 200),
                consensus_value_pit=random.uniform(100, 200),
                previous_value=random.uniform(100, 200),
                unit="Index",
                ingestion_timestamp=datetime.datetime.now(datetime.timezone.utc),
                source="SyntheticEngine"
            ))

    def _generate_geopolitical_events(self, current_date: datetime.date) -> List[GeopoliticalEvent]:
        events = []
        if random.random() < 0.05: # 5% chance
            source = random.choice(self.geopol_sources)
            events.append(GeopoliticalEvent(
                geopol_event_id=fake.unique.random_int(),
                geopol_source_id=source.geopol_source_id,
                event_timestamp_utc=datetime.datetime.combine(current_date, datetime.time(12, 0), tzinfo=datetime.timezone.utc),
                country_region_involved="Global",
                event_type="TradeRestriction" if random.random() < 0.5 else "Conflict",
                description="Simulated geopolitical event affecting markets.",
                relevance_score=random.uniform(0.5, 0.9),
                affected_assets_tickers=[],
                ingestion_timestamp=datetime.datetime.now(datetime.timezone.utc)
            ))
        return events

    def _generate_auxiliary_data(self, current_date: datetime.date):
        # SEC Filings
        if random.random() < 0.05:
            asset = random.choice(self.assets)
            ftype = random.choice(self.sec_filing_types)
            self.generated_data["sec_filings_metadata"].append(SECFilingMetadata(
                filing_id=fake.unique.random_int(),
                asset_id=asset.asset_id,
                ticker_symbol=asset.ticker_symbol,
                cik="0000000000",
                filing_type_id=ftype.filing_type_id,
                filing_date=current_date,
                ingestion_timestamp=datetime.datetime.now(datetime.timezone.utc),
                source="SyntheticEngine"
            ))

        # Social Media
        if random.random() < 0.3:
            platform = random.choice(self.social_platforms)
            self.generated_data["social_media_posts"].append(SocialMediaPost(
                post_id=fake.unique.random_int(),
                platform_id=platform.platform_id,
                post_guid=str(uuid.uuid4()),
                publish_timestamp_utc=datetime.datetime.combine(current_date, datetime.time(random.randint(0, 23), random.randint(0, 59)), tzinfo=datetime.timezone.utc),
                post_text="Just a random market thought.",
                ingestion_timestamp=datetime.datetime.now(datetime.timezone.utc)
            ))

    def run(self):
        self.initialize_market()
        delta = self.end_date - self.start_date
        print(f"Generating synthetic data from {self.start_date} to {self.end_date} ({delta.days} days)...")

        for i in range(delta.days + 1):
            current_date = self.start_date + datetime.timedelta(days=i)
            self.generate_day(current_date)

        return self.generated_data
