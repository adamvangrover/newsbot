import datetime
import random
import uuid
from typing import List, Dict, Any, Tuple, Optional
import json
import os
import pandas as pd
from faker import Faker
import networkx as nx

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

class SupplyChainGraph:
    """
    Manages the supply chain graph for assets.
    """
    def __init__(self, assets: List[Asset]):
        self.graph = nx.DiGraph()
        self.assets = {a.ticker_symbol: a for a in assets}
        self.industries = ["Technology", "Automotive", "Healthcare", "Financial", "Energy", "Consumer Goods"]
        self.asset_industries = {}
        self._build_graph()

    def _build_graph(self):
        for ticker in self.assets:
            self.asset_industries[ticker] = random.choice(self.industries)
            self.graph.add_node(ticker, type="Company", industry=self.asset_industries[ticker])

        for industry in self.industries:
            self.graph.add_node(industry, type="Industry")

        for ticker, industry in self.asset_industries.items():
            self.graph.add_edge(industry, ticker, type="contains")

        self.graph.add_edge("Technology", "Automotive", type="supplies", impact_type="SupplyChainRisk")
        self.graph.add_edge("Energy", "Consumer Goods", type="supplies", impact_type="InputCostRisk")

        tickers = list(self.assets.keys())
        for _ in range(len(tickers)):
            supplier = random.choice(tickers)
            consumer = random.choice(tickers)
            if supplier != consumer and self.asset_industries[supplier] != self.asset_industries[consumer]:
                self.graph.add_edge(supplier, consumer, type="supplies", impact_type="SupplyChainRisk")

    def to_knowledge_graph_data(self):
        # Simplification for mock usage
        return None

class SyntheticDataEngine:
    def __init__(self, start_date: datetime.date, end_date: datetime.date, num_assets: int = 20):
        self.start_date = start_date
        self.end_date = end_date
        self.num_assets = num_assets
        self.assets: List[Asset] = []
        self.universe: AssetUniverse = None
        self.constituents: List[AssetConstituent] = []
        self.market_state: Dict[str, float] = {}
        self.active_scenarios: List[Dict] = []
        self.supply_chain_graph: Dict[str, List[str]] = {}
        self.competitor_graph: Dict[str, List[str]] = {}

        self.generated_data: Dict[str, List[Any]] = {
            "assets": [],
            "asset_universe": [],
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

        self._initialize_metadata()
        self.impact_analyzer = ImpactAnalyzer()

    def _initialize_metadata(self):
        self.news_sources = [NewsSource(**x) for x in mock_gen.generate_mock_news_sources()]
        self.generated_data["news_sources"] = self.news_sources
        self.econ_event_types = [EconomicEventType(**x) for x in mock_gen.generate_mock_economic_event_types(5)]
        self.generated_data["economic_event_types"] = self.econ_event_types
        self.sec_filing_types = [SECFilingType(**x) for x in mock_gen.generate_mock_sec_filing_types()]
        self.generated_data["sec_filing_types"] = self.sec_filing_types
        self.geopol_sources = [GeopoliticalEventSource(**x) for x in mock_gen.generate_mock_geopol_sources()]
        self.social_platforms = [SocialMediaPlatform(**x) for x in mock_gen.generate_mock_social_platforms()]

    def initialize_market(self):
        mock_assets = mock_gen.generate_mock_asset_list(self.num_assets)
        self.assets = [Asset(**a) for a in mock_assets]
        self.generated_data["assets"] = self.assets
        self.supply_chain = SupplyChainGraph(self.assets)
        self.universe = AssetUniverse(universe_id=1, universe_name="Synthetic Index 20", description="Top 20 Synthetic Assets")
        self.generated_data["asset_universe"] = [self.universe]

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

        for asset in self.assets:
            self.market_state[asset.ticker_symbol] = random.uniform(50, 500)

        self._build_graphs()

    def _build_graphs(self):
        tickers = [a.ticker_symbol for a in self.assets]
        for ticker in tickers:
            if random.random() < 0.3:
                consumers = random.sample([t for t in tickers if t != ticker], k=random.randint(1, 3))
                self.supply_chain_graph[ticker] = consumers
        for ticker in tickers:
            if random.random() < 0.5:
                competitors = random.sample([t for t in tickers if t != ticker], k=random.randint(1, 2))
                self.competitor_graph[ticker] = competitors

    def generate_day(self, current_date: datetime.date):
        is_trading_day = current_date.weekday() < 5
        daily_scenario_impacts = self._process_scenarios(current_date)
        geopol_events = self._generate_geopolitical_events(current_date)
        self.generated_data["geopolitical_events"].extend(geopol_events)
        geopol_impacts = self._trace_geopol_impacts(geopol_events)
        combined_impacts = self._merge_impacts(daily_scenario_impacts, geopol_impacts)
        daily_news, price_impacts = self._generate_news(current_date, combined_impacts)
        self.generated_data["news_articles_metadata"].extend(daily_news)

        if is_trading_day:
            daily_prices = self._generate_prices(current_date, price_impacts)
            self.generated_data["equity_daily_prices"].extend(daily_prices)
            self._generate_auxiliary_data(current_date)

        daily_econ_events = self._generate_economic_events(current_date)
        self.generated_data["economic_events"].extend(daily_econ_events)

    def _process_scenarios(self, current_date: datetime.date) -> Dict[str, float]:
        impacts = {}
        if random.random() < 0.02:
            scenario_type = random.choice(["TechBreakthrough", "SupplyChainCrisis", "InflationSpike"])
            self.active_scenarios.append({
                "type": scenario_type,
                "start_date": current_date,
                "duration": random.randint(5, 20),
                "day_count": 0,
                "intensity": random.uniform(0.5, 1.5)
            })

        active_to_keep = []
        for scenario in self.active_scenarios:
            scenario["day_count"] += 1
            if scenario["day_count"] > scenario["duration"]:
                continue
            progress = scenario["day_count"] / scenario["duration"]
            daily_intensity = scenario["intensity"] * (1 - abs(progress - 0.5) * 2)

            if scenario["type"] == "TechBreakthrough":
                for asset in self.assets:
                    if hash(asset.ticker_symbol) % 3 == 0:
                        impacts[asset.ticker_symbol] = impacts.get(asset.ticker_symbol, 0) + (0.02 * daily_intensity)
            elif scenario["type"] == "SupplyChainCrisis":
                for asset in self.assets:
                     impacts[asset.ticker_symbol] = impacts.get(asset.ticker_symbol, 0) - (0.015 * daily_intensity)
            elif scenario["type"] == "InflationSpike":
                for asset in self.assets:
                    impacts[asset.ticker_symbol] = impacts.get(asset.ticker_symbol, 0) - (0.01 * daily_intensity)
            active_to_keep.append(scenario)

        self.active_scenarios = active_to_keep
        return impacts

    def _trace_geopol_impacts(self, events: List[GeopoliticalEvent]) -> Dict[str, float]:
        impacts = {}
        for event in events:
            narrative_event = PoliticalEvent(
                id=f"geopol_{event.geopol_event_id}",
                name=event.event_type or "Unknown Event",
                type="PoliticalEvent",
                event_subtype=event.event_type,
                location=event.country_region_involved,
                attributes={"description": event.description}
            )

            chains = self.impact_analyzer.trace_impacts(
                initial_event_entity=narrative_event,
                knowledge_graph=None,
                depth_levels=2
            )

            for chain in chains:
                 target_id = chain.get("impacted_entity_id")
                 if target_id == "Market":
                     for asset in self.assets:
                         impacts[asset.ticker_symbol] = impacts.get(asset.ticker_symbol, 0) - 0.01
                 elif target_id in [a.ticker_symbol for a in self.assets]:
                     impacts[target_id] = impacts.get(target_id, 0) - 0.02
        return impacts

    def _merge_impacts(self, *impact_dicts) -> Dict[str, float]:
        merged = {}
        for d in impact_dicts:
            for k, v in d.items():
                merged[k] = merged.get(k, 0.0) + v
        return merged

    def _generate_news(self, current_date: datetime.date, impacts: Dict[str, float]) -> Tuple[List[NewsArticleMetadata], Dict[str, float]]:
        news = []
        final_impacts = impacts.copy()

        # Signal News
        for ticker, impact in impacts.items():
            if abs(impact) < 0.005: continue
            asset = next((a for a in self.assets if a.ticker_symbol == ticker), None)
            if not asset: continue
            sentiment = "Positive" if impact > 0 else "Negative"
            headline = f"{asset.company_name} moves on market sentiment."
            source = random.choice(self.news_sources)
            news.append(NewsArticleMetadata(
                article_id=fake.unique.random_int(),
                news_source_id=source.news_source_id,
                headline=headline,
                publish_timestamp_utc=datetime.datetime.combine(current_date, datetime.time(random.randint(8, 16), 0), tzinfo=datetime.timezone.utc),
                tickers_mentioned=[ticker],
                ingestion_timestamp=datetime.datetime.now(datetime.timezone.utc),
                source_api="SyntheticEngine_Signal",
                sentiment_score=impact * 10
            ))

        # Noise News
        num_noise = random.randint(2, 5)
        for _ in range(num_noise):
            source = random.choice(self.news_sources)
            headline = "Market stays watchful."
            news.append(NewsArticleMetadata(
                article_id=fake.unique.random_int(),
                news_source_id=source.news_source_id,
                headline=headline,
                publish_timestamp_utc=datetime.datetime.combine(current_date, datetime.time(12, 0), tzinfo=datetime.timezone.utc),
                tickers_mentioned=[],
                ingestion_timestamp=datetime.datetime.now(datetime.timezone.utc),
                source_api="SyntheticEngine_Noise",
                sentiment_score=0.0
            ))
        return news, final_impacts

    def _generate_prices(self, current_date: datetime.date, impacts: Dict[str, float]) -> List[EquityDailyPrice]:
        prices = []
        for asset in self.assets:
            prev_close = self.market_state[asset.ticker_symbol]
            impact = impacts.get(asset.ticker_symbol, 0.0)
            drift = random.uniform(-0.01, 0.01)
            change_pct = drift + impact
            if prev_close * (1 + change_pct) <= 0:
                change_pct = 0
            open_price = round(prev_close * (1 + random.uniform(-0.005, 0.005)), 4)
            close_price = round(open_price * (1 + change_pct), 4)
            high_price = max(open_price, close_price) * (1 + random.uniform(0, 0.01))
            low_price = min(open_price, close_price) * (1 - random.uniform(0, 0.01))
            vwap = round((high_price + low_price + close_price) / 3, 4)
            self.market_state[asset.ticker_symbol] = close_price
            prices.append(EquityDailyPrice(
                asset_id=asset.asset_id,
                ticker_symbol=asset.ticker_symbol,
                trade_date=current_date,
                open_price=open_price,
                high_price=high_price,
                low_price=low_price,
                close_price=close_price,
                adjusted_close_price=close_price,
                volume=random.randint(50000, 5000000),
                vwap=vwap,
                ingestion_timestamp=datetime.datetime.now(datetime.timezone.utc),
                source="SyntheticEngine"
            ))
        return prices

    def _generate_geopolitical_events(self, current_date: datetime.date) -> List[GeopoliticalEvent]:
        events = []
        if random.random() < 0.05:
            source = random.choice(self.geopol_sources)
            events.append(GeopoliticalEvent(
                geopol_event_id=fake.unique.random_int(),
                geopol_source_id=source.geopol_source_id,
                event_timestamp_utc=datetime.datetime.combine(current_date, datetime.time(12, 0), tzinfo=datetime.timezone.utc),
                country_region_involved="Global",
                event_type="Conflict",
                description="Simulated event.",
                relevance_score=0.7,
                affected_assets_tickers=[],
                ingestion_timestamp=datetime.datetime.now(datetime.timezone.utc)
            ))
        return events

    def _generate_economic_events(self, current_date: datetime.date) -> List[EconomicEvent]:
        events = []
        for etype in self.econ_event_types:
            if random.random() < 0.05:
                events.append(EconomicEvent(
                    event_id=fake.unique.random_int(),
                    event_type_id=etype.event_type_id,
                    release_datetime_utc=datetime.datetime.combine(current_date, datetime.time(10, 0), tzinfo=datetime.timezone.utc),
                    period_covered="Previous Month",
                    actual_value=100.0,
                    consensus_value_pit=100.0,
                    previous_value=100.0,
                    unit="Index",
                    ingestion_timestamp=datetime.datetime.now(datetime.timezone.utc),
                    source="SyntheticEngine"
                ))
        return events

    def _generate_auxiliary_data(self, current_date: datetime.date):
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

    def run(self):
        self.initialize_market()
        delta = self.end_date - self.start_date
        print(f"Generating data from {self.start_date} to {self.end_date}...")
        for i in range(delta.days + 1):
            self.generate_day(self.start_date + datetime.timedelta(days=i))
        return self.generated_data
