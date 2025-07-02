from typing import Dict, Any, Optional, List
from ..core_models.python.base_types import NarrativeEntity, NewsItem, PoliticalEvent # etc.

class SignificanceScorer:
    """
    Placeholder for a service that scores the significance or relevance of an event/data point.
    """

    def __init__(self):
        # In a real implementation, might load scoring models, thresholds, or rule sets.
        print(f"[SignificanceScorer] INFO: Initialized SignificanceScorer (simulated).")

    def __init__(self, ruleset_path: Optional[str] = None):
        """
        Initialize the SignificanceScorer.
        Args:
            ruleset_path (Optional[str]): Path to a JSON file containing scoring rules.
                                          (Currently not implemented, rules are hardcoded for simulation)
        """
        print(f"[SignificanceScorer] INFO: Initialized SignificanceScorer (simulated).")
        # In a real version, load rules from ruleset_path or have a default internal set.
        self.source_reputation_scores = {
            "reuters": 0.15, "bloomberg": 0.15, "wall street journal": 0.15, "associated press": 0.1,
            "financial times": 0.15, "new york times": 0.1,
            "localgazette": -0.05, "blogspam": -0.2, "default_source": 0.0
        }
        self.event_type_base_scores = {
            "NewsItem": 0.3,
            "PoliticalEvent": 0.4,
            "FinancialReportItem": 0.5, # e.g., earnings are usually significant
            "MarketSignal": 0.45,
            "RegulatoryChange": 0.55
        }
        self.political_event_subtype_modifiers = {
            "election": 0.2, "trade deal": 0.15, "conflict escalation": 0.3,
            "protest": 0.05, "new sanction": 0.25
        }
        self.regulatory_status_modifiers = {
            "Enacted": 0.2, "Proposed": 0.1, "Repealed": -0.1 # Repeal could be positive or negative contextually
        }


    def score_event_significance(
        self,
        event_data: NarrativeEntity,
        context_entities: Optional[List[NarrativeEntity]] = None,
        # ruleset_id: Optional[str] = None # Replaced by internal simulated rules/modifiers
    ) -> Dict[str, Any]:
        """
        Refined placeholder for scoring the significance of an event.
        Considers more attributes and context.
        """
        print(f"[SignificanceScorer] INFO: Simulating significance scoring for event: {event_data.id} ({event_data.name}).")
        ctx_entity_names = [e.name for e in context_entities] if context_entities else []
        print(f"  Context entities: {ctx_entity_names if ctx_entity_names else 'None'}")

        score = self.event_type_base_scores.get(event_data.type, 0.2) # Base score from event type
        explanation_parts = [f"Significance assessment for '{event_data.name}' (Type: {event_data.type}):"]
        explanation_parts.append(f"Base score for type '{event_data.type}': {score:.2f}.")

        # --- Event-specific attribute scoring ---
        if isinstance(event_data, NewsItem):
            if event_data.sentiment_score is not None:
                sentiment_contribution = event_data.sentiment_score * 0.3 # Sentiment has a stronger impact now
                score += sentiment_contribution
                explanation_parts.append(f"News sentiment ({event_data.sentiment_score:.2f}) contributed {sentiment_contribution:.2f} to score.")

            source_rep_score = self.source_reputation_scores.get(
                event_data.source_name.lower() if event_data.source_name else "default_source",
                self.source_reputation_scores["default_source"]
            )
            score += source_rep_score
            explanation_parts.append(f"Source '{event_data.source_name or 'Unknown'}' reputation contributed {source_rep_score:.2f}.")

        elif isinstance(event_data, PoliticalEvent):
            if event_data.event_subtype:
                # Case-insensitive lookup for subtype modifier
                subtype_key_found = None
                for k_sub, v_sub in self.political_event_subtype_modifiers.items():
                    if k_sub in event_data.event_subtype.lower():
                        subtype_key_found = k_sub
                        break
                subtype_mod = self.political_event_subtype_modifiers.get(subtype_key_found, 0.0) if subtype_key_found else 0.0
                score += subtype_mod
                explanation_parts.append(f"Political event subtype '{event_data.event_subtype}' (matched rule key: {subtype_key_found}) modified score by {subtype_mod:.2f}.")
            if event_data.perceived_impact_area and "geopolitics" in event_data.perceived_impact_area.lower():
                score += 0.1 # Slight bonus for broad geopolitical impact
                explanation_parts.append("Geopolitical impact area noted (+0.1).")

        elif isinstance(event_data, FinancialReportItem):
            if event_data.report_type in ["10-K", "Annual Report"]:
                score += 0.1 # Annual reports often more significant
                explanation_parts.append("Annual report type considered more significant (+0.1).")
            if event_data.key_metrics:
                # Simulate checking for earnings surprise (very simplified)
                if "NetIncome" in event_data.key_metrics and "ExpectedNetIncome" in (event_data.attributes or {}):
                    surprise_factor = (event_data.key_metrics["NetIncome"] / (event_data.attributes["ExpectedNetIncome"] + 1e-6)) - 1
                    surprise_mod = min(max(surprise_factor * 0.5, -0.2), 0.2) # Capped modifier
                    score += surprise_mod
                    explanation_parts.append(f"Simulated earnings surprise factor contributed {surprise_mod:.2f}.")

        elif isinstance(event_data, RegulatoryChange):
            if event_data.status:
                status_mod = self.regulatory_status_modifiers.get(event_data.status, 0.0)
                score += status_mod
                explanation_parts.append(f"Regulatory status '{event_data.status}' modified score by {status_mod:.2f}.")
            if event_data.industries_affected_ids:
                 explanation_parts.append(f"Affects industries: {', '.join(event_data.industries_affected_ids)}.")


        # --- Contextual Scoring ---
        if context_entities:
            relevance_bonus = 0.0
            explanation_parts.append(f"Assessing relevance to {len(context_entities)} context entities: {', '.join(ctx_entity_names)}.")
            for ctx_entity in context_entities:
                # 1. Direct mention in NewsItem
                if isinstance(event_data, NewsItem) and event_data.key_entities_mentioned_ids:
                    if ctx_entity.id in event_data.key_entities_mentioned_ids:
                        relevance_bonus += 0.3
                        explanation_parts.append(f"Direct mention of '{ctx_entity.name}' in news boosted relevance (+0.3).")
                        break # Max bonus for direct mention of one context entity

                # 2. Event is about the context company (FinancialReportItem)
                if isinstance(event_data, FinancialReportItem) and event_data.company_id == ctx_entity.id:
                    relevance_bonus += 0.35 # Report about the company itself is highly relevant
                    explanation_parts.append(f"Financial report is directly for '{ctx_entity.name}' (+0.35).")
                    break

                # 3. Context company's industry is affected by RegulatoryChange
                if isinstance(event_data, RegulatoryChange) and isinstance(ctx_entity, Company):
                    if ctx_entity.industry_id and event_data.industries_affected_ids and ctx_entity.industry_id in event_data.industries_affected_ids:
                        relevance_bonus += 0.25
                        explanation_parts.append(f"'{ctx_entity.name}' (in industry '{ctx_entity.industry_id}') potentially affected by regulatory change (+0.25).")
                        break
            score += relevance_bonus

        # Clamp score to [0, 1]
        final_score = max(0.0, min(1.0, round(score, 3)))

        if final_score > 0.75:
            explanation_parts.append(f"Overall significance assessed as HIGH ({final_score}).")
        elif final_score > 0.45:
            explanation_parts.append(f"Overall significance assessed as MEDIUM ({final_score}).")
        else:
            explanation_parts.append(f"Overall significance assessed as LOW ({final_score}).")

        return {
            "score": final_score,
            "explanation": " ".join(explanation_parts)
        }

if __name__ == '__main__':
    from datetime import datetime
    # Import concrete types for example usage
    from ..core_models.python.base_types import Company, NewsItem, PoliticalEvent, FinancialReportItem, RegulatoryChange

    scorer = SignificanceScorer()

    print("\n--- Simulating Significance Scoring for NewsItem (Refined) ---")
    sample_news_high_impact = NewsItem(
        id="news_high_001", name="Tech Giant Announces Breakthrough, Stock Soars", type="NewsItem",
        sentiment_score=0.9, source_name="Reuters",
        key_entities_mentioned_ids=["comp_alpha_test"]
    )
    context_company = Company(id="comp_alpha_test", name="AlphaTest Corp", type="Company")

    result_news = scorer.score_event_significance(sample_news_high_impact, context_entities=[context_company])
    print(f"News Significance Score: {result_news['score']}")
    print(f"Explanation: {result_news['explanation']}")

    print("\n--- Simulating Significance Scoring for PoliticalEvent ---")
    sample_political_event = PoliticalEvent(
        id="pol_event_001", name="Major Election in Key Region", type="PoliticalEvent",
        event_subtype="National Election", perceived_impact_area="Geopolitics, RegionalEconomy"
    )
    result_political = scorer.score_event_significance(sample_political_event)
    print(f"Political Event Significance Score: {result_political['score']}")
    print(f"Explanation: {result_political['explanation']}")

    print("\n--- Simulating Low Significance News ---")
    sample_news_low_impact = NewsItem(
        id="news_low_001", name="Minor Local Company Update", type="NewsItem",
        sentiment_score=0.1, source_name="LocalGazette",
        key_entities_mentioned_ids=["some_other_entity"]
    )
    result_news_low = scorer.score_event_significance(sample_news_low_impact, context_entities=[context_company])
    print(f"Low Impact News Score: {result_news_low['score']}")
    print(f"Explanation: {result_news_low['explanation']}")
