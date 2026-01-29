from typing import List, Dict, Any, Optional
import re
from datetime import datetime
from pydantic import BaseModel, Field

# Importing models to ensure type safety
from synthetic.pydantic_models import NewsArticleMetadata

class TraceImpact(BaseModel):
    """
    Represents a single step in an impact chain.
    """
    step_id: str
    description: str
    source_entity: str
    target_entity: str
    impact_type: str # e.g., "PriceDrop", "SupplyChainDelay"
    probability: float
    confidence_score: float # Based on data source reliability
    logic_path: str # e.g. "Rate Hike -> Tech Sector Drop -> Company A Revenue Hit"

class ImpactAnalysisResult(BaseModel):
    original_event: str
    signal_strength: str # "High", "Medium", "Low", "Noise"
    impact_chains: List[TraceImpact] = []

class SignalDetector:
    """
    Filters noise from signal using heuristics or basic NLP.
    """
    def __init__(self):
        # Regex patterns for high signal events
        self.high_signal_patterns = [
            r"earnings", r"revenue", r"profit", r"loss", r"guidance",
            r"merger", r"acquisition", r"buyout",
            r"resigns", r"steps down", r"ceo", r"cfo",
            r"fda approval", r"lawsuit", r"settlement",
            r"dividend", r"stock split",
            r"rate hike", r"inflation", r"fed",
            r"market crash", r"rally", r"plunge"
        ]

        self.noise_patterns = [
            r"top 10", r"why", r"opinion", r"watch", r"could",
            r"maybe", r"rumor", r"speculation", r"penny stocks"
        ]

    def classify(self, text: str) -> str:
        text_lower = text.lower()

        # Check for noise first
        for pattern in self.noise_patterns:
            if re.search(pattern, text_lower):
                return "Noise"

        # Check for high signal
        for pattern in self.high_signal_patterns:
            if re.search(pattern, text_lower):
                return "High Signal"

        return "Context" # Middle ground

class ImpactAnalyzer:
    """
    Analyzes and traces potential impacts of an event.
    """

    def __init__(self):
        self.signal_detector = SignalDetector()

        # Mock Logic Rules (In a real system, these would be loaded from a DB or config)
        self.rules = {
            "Rate Hike": {
                "impact": "Negative",
                "sectors": ["Tech", "Real Estate"],
                "logic": "Higher cost of borrowing reduces growth capital."
            },
            "Earnings Beat": {
                "impact": "Positive",
                "target": "Self",
                "logic": "Better than expected financial performance indicates health."
            },
            "CEO Resigns": {
                "impact": "Negative",
                "target": "Self",
                "logic": "Leadership instability causes uncertainty."
            },
            "Merger": {
                "impact": "Positive",
                "target": "Self",
                "logic": "Potential for synergies and growth."
            }
        }

    def analyze_news(self, news_item: NewsArticleMetadata) -> ImpactAnalysisResult:
        """
        Main entry point for analyzing a news item.
        """
        signal = self.signal_detector.classify(news_item.headline)

        result = ImpactAnalysisResult(
            original_event=news_item.headline,
            signal_strength=signal
        )

        if signal == "Noise":
            return result

        # Logic Tracing
        traces = self._trace_logic(news_item.headline, news_item.tickers_mentioned or [])
        result.impact_chains = traces

        return result

    def trace_impacts(self, initial_event_entity: Any, knowledge_graph: Any = None, depth_levels: int = 2) -> List[Dict[str, Any]]:
        """
        Legacy method to support synthetic generator.
        """
        # Adapt input to new logic
        headline = getattr(initial_event_entity, "name", "Unknown Event")
        # Extract tickers if possible, or just pass empty
        tickers = []

        traces = self._trace_logic(headline, tickers)

        # Convert TraceImpact objects back to dicts expected by synthetic generator
        results = []
        for t in traces:
             results.append({
                 "impacted_entity_id": t.target_entity,
                 "impact_type": t.impact_type,
                 "magnitude": "Medium" if "Surge" in t.impact_type or "Drop" in t.impact_type else "Low",
                 "probability": t.probability
             })

        # If no traces (because _trace_logic expects specific keywords), fallback to mock logic from original file
        if not results and getattr(initial_event_entity, "type", "") == "PoliticalEvent":
             # Restore simple logic for geopolitical events
             results.append({
                 "impacted_entity_id": "Market", # Generic
                 "impact_type": "Risk",
                 "magnitude": "Medium",
                 "probability": 0.6
             })

        return results

    def _trace_logic(self, headline: str, tickers: List[str]) -> List[TraceImpact]:
        traces = []
        headline_lower = headline.lower()

        # 1. Direct Impact
        matched_rule = None
        rule_name = None

        if "rate hike" in headline_lower:
            matched_rule = self.rules["Rate Hike"]
            rule_name = "Rate Hike"
        elif "beats earnings" in headline_lower or "revenue" in headline_lower:
            matched_rule = self.rules["Earnings Beat"]
            rule_name = "Earnings Beat"
        elif "resigns" in headline_lower or "steps down" in headline_lower:
            matched_rule = self.rules["CEO Resigns"]
            rule_name = "CEO Resigns"
        elif "merger" in headline_lower or "acquisition" in headline_lower:
            matched_rule = self.rules["Merger"]
            rule_name = "Merger"

        if matched_rule and tickers:
            for ticker in tickers:
                # First Order
                impact_type = "PriceSurge" if matched_rule["impact"] == "Positive" else "PriceDrop"

                trace = TraceImpact(
                    step_id=f"1st_order_{datetime.now().timestamp()}",
                    description=f"Direct impact on {ticker}",
                    source_entity="NewsEvent",
                    target_entity=ticker,
                    impact_type=impact_type,
                    probability=0.8,
                    confidence_score=0.9,
                    logic_path=f"{rule_name} -> {impact_type} for {ticker}"
                )
                traces.append(trace)

                # Mock Second Order (using 'Synthetic Logic Patterning')
                if rule_name == "Rate Hike":
                     traces.append(TraceImpact(
                        step_id=f"2nd_order_{datetime.now().timestamp()}",
                        description=f"Sector-wide drag on {ticker}'s peers",
                        source_entity=ticker,
                        target_entity="Sector Peers",
                        impact_type="SectorDrag",
                        probability=0.6,
                        confidence_score=0.7,
                        logic_path=f"{rule_name} -> Higher Discount Rate -> Sector Valuation Compression"
                    ))

        return traces
