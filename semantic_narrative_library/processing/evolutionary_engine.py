from typing import List, Dict, Any
from datetime import datetime, timedelta
import random
from pydantic import BaseModel
from .impact_analysis_engine import ImpactAnalyzer, TraceImpact, ImpactAnalysisResult
from synthetic.pydantic_models import NewsArticleMetadata

class FutureScenario(BaseModel):
    scenario_id: str
    base_date: datetime
    target_date: datetime
    trigger_event: str
    projected_state: str
    likelihood: float
    key_drivers: List[str]

class EvolutionarySimulator:
    """
    Simulates how current events might evolve over time (T+1 month, T+6 months)
    using probabilistic mutation of impact chains.
    """
    def __init__(self):
        self.impact_analyzer = ImpactAnalyzer()

    def generate_evolutionary_scenarios(self, initial_event: str, iterations: int = 3) -> List[FutureScenario]:
        scenarios = []
        base_date = datetime.now()

        # 1. Get initial impacts
        # We need a dummy news item for the analyzer
        dummy_news = NewsArticleMetadata(
            article_id=random.randint(1000, 9999),
            headline=initial_event,
            article_url="http://synthetic",
            publish_timestamp_utc=base_date,
            ingestion_timestamp=base_date,
            source_api="Simulation",
            tickers_mentioned=["SPY", "QQQ"] # Generic default
        )

        initial_result = self.impact_analyzer.analyze_news(dummy_news)

        if not initial_result.impact_chains:
            # Fallback if no specific rules match
            scenarios.append(FutureScenario(
                scenario_id=f"sim_default_{int(datetime.now().timestamp())}",
                base_date=base_date,
                target_date=base_date + timedelta(days=30),
                trigger_event=initial_event,
                projected_state="Market absorbs the news with neutral impact.",
                likelihood=0.9,
                key_drivers=["Market Resilience"]
            ))
            return scenarios

        # 2. Evolve
        for i in range(iterations):
            mutation_factor = random.random()

            # Pick a random chain to extend
            chain = random.choice(initial_result.impact_chains)

            future_date = base_date + timedelta(days=30 * (i+1))

            # Logic: If Impact is Negative, does it stabilize or worsen?
            if "Drop" in chain.impact_type or "Negative" in chain.impact_type or "Drag" in chain.impact_type:
                outcome = "Recovery Phase" if mutation_factor > 0.6 else "Deepening Correction"
            else:
                outcome = "Growth Continues" if mutation_factor > 0.4 else "Correction due to Overheating"

            scenarios.append(FutureScenario(
                scenario_id=f"sim_{i}_{int(datetime.now().timestamp())}",
                base_date=base_date,
                target_date=future_date,
                trigger_event=initial_event,
                projected_state=f"{outcome} driven by {chain.logic_path}",
                likelihood=round(random.random(), 2),
                key_drivers=[chain.source_entity, chain.target_entity]
            ))

        return scenarios
