import datetime
import random
import uuid
from typing import List, Dict, Any, Tuple, Optional
import json
import os
from typing import List, Dict, Any, Tuple
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
        # Assign industries to assets randomly
        for ticker in self.assets:
            self.asset_industries[ticker] = random.choice(self.industries)
            self.graph.add_node(ticker, type="Company", industry=self.asset_industries[ticker])

        # Create industries nodes
        for industry in self.industries:
            self.graph.add_node(industry, type="Industry")

        # Link Industries to Companies (Industry -> Company) with "contains"
        # This allows: Industry impacted -> Companies in it impacted
        for ticker, industry in self.asset_industries.items():
            self.graph.add_edge(industry, ticker, type="contains")

        # Create Supply Chain Links (randomly for now)
        # e.g. Technology -> Automotive (Chips -> Cars)
        # e.g. Energy -> Consumer Goods (Oil -> Plastic/Transport)

        # Inter-industry dependencies
        self.graph.add_edge("Technology", "Automotive", type="supplies", impact_type="SupplyChainRisk")
        self.graph.add_edge("Energy", "Consumer Goods", type="supplies", impact_type="InputCostRisk")

        # Company to Company dependencies (Supplier -> Consumer)
        tickers = list(self.assets.keys())
        for _ in range(len(tickers)): # Create some random links
            supplier = random.choice(tickers)
            consumer = random.choice(tickers)
            if supplier != consumer and self.asset_industries[supplier] != self.asset_industries[consumer]:
                self.graph.add_edge(supplier, consumer, type="supplies", impact_type="SupplyChainRisk")

    def get_downstream_impacts(self, source_node: str) -> List[str]:
        """Returns a list of nodes directly downstream from the source."""
        if source_node in self.graph:
            return list(self.graph.successors(source_node))
        return []

    def to_knowledge_graph_data(self) -> KnowledgeGraphData:
        """Converts the internal graph to the KnowledgeGraphData format for ImpactAnalyzer."""
        entities = []
        relationships = []

        for node, data in self.graph.nodes(data=True):
            if data.get("type") == "Company":
                entities.append(Company(
                    id=node,
                    name=self.assets[node].company_name if node in self.assets else node,
                    ticker_symbol=node,
                    type="Company",
                    industry_id=data.get("industry")
                ))
            elif data.get("type") == "Industry":
                entities.append(Industry(
                    id=node,
                    name=node,
                    type="Industry"
                ))
            else:
                 entities.append(NarrativeEntity(id=node, name=node, type=data.get("type", "Generic")))

        for u, v, data in self.graph.edges(data=True):
            relationships.append(Relationship(
                id=f"{u}_{v}",
                source_id=u,
                target_id=v,
                type=data.get("type", "related_to"),
                attributes={"impact_type": data.get("impact_type")}
            ))

        return KnowledgeGraphData(entities=entities, relationships=relationships)


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

        # Graph relationships
        self.supply_chain_graph: Dict[str, List[str]] = {} # Supplier -> [Consumers]
        self.competitor_graph: Dict[str, List[str]] = {}   # Company -> [Competitors]

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
        """Initializes assets, initial prices, and relationships."""
        # Generate Assets
        mock_assets = mock_gen.generate_mock_asset_list(self.num_assets)
        self.assets = [Asset(**a) for a in mock_assets]
        self.generated_data["assets"] = self.assets

        # Create Supply Chain Graph
        self.supply_chain = SupplyChainGraph(self.assets)

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

        # Initialize Relationships (Supply Chain & Competitors)
        self._build_graphs()

    def _build_graphs(self):
        """Randomly assigns supply chain and competitor relationships."""
        tickers = [a.ticker_symbol for a in self.assets]

        # Supply Chain: A supplies B
        for ticker in tickers:
            # 30% chance of being a supplier to 1-3 other companies
            if random.random() < 0.3:
                consumers = random.sample([t for t in tickers if t != ticker], k=random.randint(1, 3))
                self.supply_chain_graph[ticker] = consumers

        # Competitors: A competes with B
        for ticker in tickers:
            # 50% chance of having competitors
            if random.random() < 0.5:
                # Ensure reciprocity or just directional? Directional is easier for simple logic
                competitors = random.sample([t for t in tickers if t != ticker], k=random.randint(1, 2))
                self.competitor_graph[ticker] = competitors

    def generate_day(self, current_date: datetime.date):
        """Generates data for a single day, ensuring consistency."""
        is_trading_day = current_date.weekday() < 5

        # Scenarios and Events (News)
        # We generate news even on weekends sometimes, but price impact is realized on trading days or gap open
        day_events = self._generate_daily_scenarios(current_date)

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
        if is_trading_day:
            # Generate Prices
            daily_prices = self._generate_prices(current_date, price_impacts)
            self.generated_data["equity_daily_prices"].extend(daily_prices)

            # Generate Filings (Business days only usually)
            daily_filings = self._generate_filings(current_date)
            self.generated_data["sec_filings_metadata"].extend(daily_filings)

        # Generate Economic Events
        daily_econ_events = self._generate_economic_events(current_date)
        self.generated_data["economic_events"].extend(daily_econ_events)

    def _generate_daily_scenarios(self, current_date: datetime.date) -> List[Dict]:
        """Decides if any major market scenarios happen today."""
        scenarios = []
        # Randomly trigger a "Market Shock" or specific event
        if random.random() < 0.02: # 2% chance of a market-wide event
            event_type = random.choice(["Crash", "Boom", "RateHike", "TechRally"])
            scenarios.append({"type": "MarketEvent", "name": event_type})

        # Trigger Complex Event Chain (Supply Chain Disruption)
        if random.random() < 0.05: # 5% chance
             # Pick a random industry to disrupt
             sector = random.choice(self.supply_chain.industries)
             scenarios.append({"type": "ComplexEvent", "name": "SupplyChainDisruption", "root_sector": sector})

        # 1. Market-wide Events
        if random.random() < 0.02: # 2% chance of a major market event
            event_type = random.choice(["Crash", "Boom", "RateHike", "TechRally"])
            scenarios.append({"type": "MarketEvent", "name": event_type, "scope": "Global"})

        # 2. Idiosyncratic Events (Company specific)
        for asset in self.assets:
            if random.random() < 0.05: # 5% chance of major news per asset
                scenarios.append({
                    "type": "CompanyEvent",
                    "ticker": asset.ticker_symbol,
                    "event_class": random.choice(["Earnings", "Scandal", "ProductLaunch", "Merger"])
                })

        return scenarios

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
        news_items = []
        price_impacts = {a.ticker_symbol: 0.0 for a in self.assets}

        kg_data = self.supply_chain.to_knowledge_graph_data()

        # Apply Scenario Impacts
        for scenario in scenarios:
            impact_factor = 0.0

            if scenario['type'] == "MarketEvent":
                headline = f"Market Alert: {scenario['name']} scenarios unfolding."
                if scenario['name'] == "Crash":
                    impact_factor = -0.05
                    headline = "Market Plunges as Sell-off Intensifies"
                elif scenario['name'] == "Boom":
                    impact_factor = 0.03
                    headline = "Markets Rally to New Highs"
                elif scenario['name'] == "RateHike":
                    impact_factor = -0.02
                    headline = "Central Bank Announces Unexpected Rate Hike"

                # Create a market-wide news item
                source = random.choice(self.news_sources)
                news_items.append(NewsArticleMetadata(
                    article_id=fake.unique.random_int(),
                    news_source_id=source.news_source_id,
                    headline=headline,
                    publish_timestamp_utc=datetime.datetime.combine(current_date, datetime.time(9, 0), tzinfo=datetime.timezone.utc),
                    tickers_mentioned=[],
                    ingestion_timestamp=datetime.datetime.now(datetime.timezone.utc),
                    sentiment_score=impact_factor * 20
                ))

                # Apply to all assets
                for ticker in price_impacts:
                    price_impacts[ticker] += impact_factor + random.uniform(-0.01, 0.01)

            elif scenario['type'] == "ComplexEvent":
                root_sector = scenario.get('root_sector', 'Technology')

                # Use ImpactAnalyzer to trace impacts
                root_event = PoliticalEvent(
                    id=f"evt_shortage_{current_date.strftime('%Y%m%d')}",
                    name=f"Trade Restrictions in {root_sector}",
                    type="PoliticalEvent",
                    event_subtype="TradeRestriction",
                    attributes={"affected_sectors": [root_sector]}
                )

                # Trace impacts
                impacts = self.impact_analyzer.trace_impacts(root_event, kg_data, depth_levels=2)

                # Generate News for Root Event
                source = random.choice(self.news_sources)
                news_items.append(NewsArticleMetadata(
                    article_id=fake.unique.random_int(),
                    news_source_id=source.news_source_id,
                    headline=f"Breaking: New Trade Restrictions hit {root_sector} Sector",
                    publish_timestamp_utc=datetime.datetime.combine(current_date, datetime.time(8, 30), tzinfo=datetime.timezone.utc),
                    tickers_mentioned=[],
                    ingestion_timestamp=datetime.datetime.now(datetime.timezone.utc),
                    sentiment_score=-0.6
                ))

                # Process Impacts from Analyzer
                for impact in impacts:
                    target_id = impact['impacted_entity_id']

                    # If target is a Company (ticker), apply price impact and generate specific news
                    if target_id in self.assets: # It's a ticker

                        mag = impact.get('magnitude', 'Medium')
                        base_impact = -0.03 if mag == 'Medium' else (-0.01 if mag == 'Low' else -0.05)

                        # Apply knock-on effect
                        price_impacts[target_id] += base_impact

                        # Generate specific news for the company
                        headline_templates = [
                            f"{target_id} faces production delays due to supply chain issues.",
                            f"Analysts downgrade {target_id} amid component shortages.",
                            f"{target_id} warns of revenue hit from supplier constraints."
                        ]

                        news_items.append(NewsArticleMetadata(
                            article_id=fake.unique.random_int(),
                            news_source_id=random.choice(self.news_sources).news_source_id,
                            headline=random.choice(headline_templates),
                            publish_timestamp_utc=datetime.datetime.combine(current_date, datetime.time(random.randint(10, 16), 0), tzinfo=datetime.timezone.utc),
                            tickers_mentioned=[target_id],
                            ingestion_timestamp=datetime.datetime.now(datetime.timezone.utc),
                            sentiment_score=base_impact * 20
                        ))

                    elif impact.get("impact_type") == "SupplyChainRisk": # Industry level
                         pass


        # Generate Idiosyncratic News (Company Specific) - Background noise
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
        # Helper to look up company name
        ticker_to_name = {a.ticker_symbol: a.company_name for a in self.assets}

        for scenario in scenarios:
            source = random.choice(self.news_sources)
            pub_time = datetime.datetime.combine(current_date, datetime.time(random.randint(8, 16), random.randint(0, 59)), tzinfo=datetime.timezone.utc)

            if scenario['type'] == "MarketEvent":
                headline, impact_factor = self._process_market_event(scenario)

                news_items.append(NewsArticleMetadata(
                    article_id=fake.unique.random_int(),
                    news_source_id=source.news_source_id,
                    headline=headline,
                    publish_timestamp_utc=pub_time,
                    tickers_mentioned=[],
                    ingestion_timestamp=datetime.datetime.now(datetime.timezone.utc),
                    sentiment_score=impact_factor * 20
                ))
                # Apply to all assets
                for ticker in price_impacts:
                    price_impacts[ticker] += impact_factor + random.uniform(-0.005, 0.005)

            elif scenario['type'] == "CompanyEvent":
                primary_ticker = scenario['ticker']
                headline, impact_factor, sentiment_label = self._process_company_event(scenario, ticker_to_name[primary_ticker])

                # Primary News
                news_items.append(NewsArticleMetadata(
                    article_id=fake.unique.random_int(),
                    news_source_id=source['news_source_id'],
                    headline=headline,
                    publish_timestamp_utc=pub_time,
                    tickers_mentioned=[primary_ticker],
                    ingestion_timestamp=datetime.datetime.now(datetime.timezone.utc),
                    sentiment_score=impact_factor * 20
                ))
                price_impacts[primary_ticker] += impact_factor

                # --- 2nd Order Effects: Supply Chain ---
                # If Supplier (primary) has BAD news (e.g. Scandal/Production Halt), Consumers might suffer.
                # If Supplier has GOOD news (e.g. Breakthrough), Consumers might benefit (better tech) or stay neutral.
                if primary_ticker in self.supply_chain_graph:
                    consumers = self.supply_chain_graph[primary_ticker]
                    for consumer in consumers:
                        # Logic: Supply disruption hurts consumer
                        chain_impact = 0.0
                        chain_headline = ""

                        if sentiment_label == "Negative":
                            # Supplier issue -> Supply Chain Risk
                            chain_impact = -0.02 # Smaller impact
                            chain_headline = f"{ticker_to_name[consumer]} faces potential supply chain delays due to {ticker_to_name[primary_ticker]} issues."
                        elif sentiment_label == "Positive":
                            # Supplier breakthrough -> specific benefit
                            chain_impact = 0.01
                            if scenario['event_class'] == "ProductLaunch":
                                chain_headline = f"{ticker_to_name[consumer]} likely to benefit from {ticker_to_name[primary_ticker]}'s new tech."
                            elif scenario['event_class'] == "Merger":
                                chain_headline = f"{ticker_to_name[consumer]} shares rise on sympathy with {ticker_to_name[primary_ticker]} merger news."
                            elif scenario['event_class'] == "Earnings":
                                chain_headline = f"{ticker_to_name[consumer]} climbs following strong results from supplier {ticker_to_name[primary_ticker]}."
                            else:
                                chain_headline = f"{ticker_to_name[consumer]} sees positive momentum linked to {ticker_to_name[primary_ticker]}."

                        if chain_headline:
                            price_impacts[consumer] += chain_impact
                            # Add separate news item for the knock-on effect? Or just let the model infer?
                            # Phase 1 requirement says "Create a cascade of synthetic news items". So yes.
                            news_items.append(NewsArticleMetadata(
                                article_id=fake.unique.random_int(),
                                news_source_id=source['news_source_id'],
                                headline=chain_headline,
                                publish_timestamp_utc=pub_time + datetime.timedelta(minutes=random.randint(30, 120)),
                                tickers_mentioned=[consumer, primary_ticker],
                                ingestion_timestamp=datetime.datetime.now(datetime.timezone.utc),
                                sentiment_score=chain_impact * 20
                            ))

                # --- 2nd Order Effects: Competitors ---
                # If Company A does well, Competitor B might suffer.
                if primary_ticker in self.competitor_graph:
                    competitors = self.competitor_graph[primary_ticker]
                    for comp in competitors:
                        comp_impact = 0.0
                        comp_headline = ""

                        if sentiment_label == "Positive":
                            comp_impact = -0.015
                            comp_headline = f"{ticker_to_name[comp]} shares slip as {ticker_to_name[primary_ticker]} gains market share."
                        elif sentiment_label == "Negative":
                            comp_impact = 0.01
                            comp_headline = f"{ticker_to_name[comp]} poised to capitalize on {ticker_to_name[primary_ticker]}'s struggles."

                        if comp_headline:
                            price_impacts[comp] += comp_impact
                            news_items.append(NewsArticleMetadata(
                                article_id=fake.unique.random_int(),
                                news_source_id=source['news_source_id'],
                                headline=comp_headline,
                                publish_timestamp_utc=pub_time + datetime.timedelta(minutes=random.randint(15, 60)),
                                tickers_mentioned=[comp, primary_ticker],
                                ingestion_timestamp=datetime.datetime.now(datetime.timezone.utc),
                                sentiment_score=comp_impact * 20
                            ))

        return news_items, price_impacts

    def _process_market_event(self, scenario):
        name = scenario['name']
        if name == "Crash":
            return "Market Plunges as Sell-off Intensifies", -0.05
        elif name == "Boom":
            return "Markets Rally to New Highs", 0.03
        elif name == "RateHike":
            return "Central Bank Announces Surprise Rate Hike", -0.02
        elif name == "TechRally":
            return "Tech Sector Leads Market Gains", 0.025
        return "Market volatility increases", 0.0

    def _process_company_event(self, scenario, company_name):
        event_class = scenario['event_class']
        headline = ""
        impact = 0.0
        sentiment = "Neutral"

        if event_class == "Earnings":
            if random.random() > 0.5:
                headline = f"{company_name} beats earnings expectations."
                impact = 0.05
                sentiment = "Positive"
            else:
                headline = f"{company_name} misses revenue targets."
                impact = -0.05
                sentiment = "Negative"
        elif event_class == "Scandal":
            headline = f"CEO of {company_name} steps down amid controversy."
            impact = -0.08
            sentiment = "Negative"
        elif event_class == "ProductLaunch":
            headline = f"{company_name} announces breakthrough product."
            impact = 0.04
            sentiment = "Positive"
        elif event_class == "Merger":
            headline = f"{company_name} in talks for potential acquisition."
            impact = 0.03
            sentiment = "Positive"

        return headline, impact, sentiment

    def _generate_prices(self, current_date: datetime.date, price_impacts: Dict[str, float]) -> List[EquityDailyPrice]:
        prices = []
        for asset in self.assets:
            prev_close = self.market_state[asset.ticker_symbol]
            impact = impacts.get(asset.ticker_symbol, 0.0)

            # Random drift (market noise) + Systematic Impact
            drift = random.uniform(-0.01, 0.01)
            change_pct = drift + impact

            # Ensure we don't go to zero or negative easily
            # Ensure price doesn't go negative
            if prev_close * (1 + change_pct) <= 0:
                change_pct = 0

            open_price = round(prev_close * (1 + random.uniform(-0.005, 0.005)), 4)
            close_price = round(open_price * (1 + change_pct), 4)

            high_price = max(open_price, close_price) * (1 + random.uniform(0, 0.01))
            low_price = min(open_price, close_price) * (1 - random.uniform(0, 0.01))

            # Simple VWAP approximation
            vwap = round((high_price + low_price + close_price) / 3, 4)

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
                vwap=vwap,
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
                cik=_cik,
                filing_type_id=filing_type.filing_type_id,
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

    def _generate_economic_events(self, current_date: datetime.date) -> List[EconomicEvent]:
        events = []
        # Simulate check if today is a release day for any event type (randomly)
        for etype in self.econ_event_types:
            if random.random() < 0.05: # 5% chance this event releases today

                release_dt = datetime.datetime.combine(current_date, datetime.time(8, 30), tzinfo=datetime.timezone.utc)
                actual = round(random.uniform(-5, 10) if "%" in etype.event_name else random.uniform(100, 10000), 2)
                consensus = round(actual + random.uniform(-abs(actual*0.1), abs(actual*0.1)), 2)
                previous = round(actual * (1 + random.uniform(-0.05, 0.05)), 2)

                events.append(EconomicEvent(
                    event_id=fake.unique.random_int(),
                    event_type_id=etype.event_type_id,
                    release_datetime_utc=release_dt,
                    period_covered="Prior Month",
                    actual_value=actual,
                    consensus_value_pit=consensus,
                    previous_value=previous,
                    unit=random.choice(["K", "%", "Index"]),
                    ingestion_timestamp=datetime.datetime.now(datetime.timezone.utc),
                    source="Econoday_mock"
                ))
        return events

    def run(self):
        self.initialize_market()
        delta = self.end_date - self.start_date
        print(f"Generating synthetic data from {self.start_date} to {self.end_date} ({delta.days} days)...")

        for i in range(delta.days + 1):
            current_date = self.start_date + datetime.timedelta(days=i)
            self.generate_day(current_date)

        return self.generated_data

    def output_to_jsonl(self, output_dir: str):
        """Exports the generated data to JSONL files in the specified directory."""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Assets
        with open(f"{output_dir}/assets.jsonl", "w") as f:
            for item in self.generated_data["assets"]:
                f.write(item.model_dump_json() + "\n")

        # Prices
        with open(f"{output_dir}/equity_daily_prices.jsonl", "w") as f:
            for item in self.generated_data["equity_daily_prices"]:
                f.write(item.model_dump_json() + "\n")

        # News
        with open(f"{output_dir}/news_articles_metadata.jsonl", "w") as f:
            for item in self.generated_data["news_articles_metadata"]:
                f.write(item.model_dump_json() + "\n")

        # Filings
        with open(f"{output_dir}/sec_filings_metadata.jsonl", "w") as f:
            for item in self.generated_data["sec_filings_metadata"]:
                f.write(item.model_dump_json() + "\n")

        print(f"Data exported to {output_dir}")
