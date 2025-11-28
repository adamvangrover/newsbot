from typing import List, Dict, Any, Optional
from ..core_models.python.base_types import KnowledgeGraphData, NarrativeEntity, Relationship, Company, Industry

class ImpactAnalyzer:
    """
    Service that analyzes and traces the potential impacts of an event or driver across the knowledge graph.
    """

    def __init__(self):
        print(f"[ImpactAnalyzer] INFO: Initialized ImpactAnalyzer.")
        self.rulesets: Dict[str, List[Dict[str, Any]]] = {
            "rs_standard_financial_impacts_v1": [
                {
                    "rule_id": "rule_positive_news_sentiment_boost_sim",
                    "trigger": {"event_type": "NewsItem", "sentiment_score_gt": 0.7},
                    "impacts": [{
                        "order": 1, "target_entity_type_selector": "Company",
                        "impact_type": "PositiveShortTermOutlook", "probability": 0.6, "magnitude_qualitative": "Low"
                    }]
                },
                {
                    "rule_id": "rule_supply_chain_disruption_sim",
                    "trigger": {"event_type": "PoliticalEvent", "event_subtype_contains": "TradeRestriction"},
                    "impacts": [{
                        "order": 1, "target_entity_type_selector": "Industry",
                        "impact_type": "SupplyChainRisk", "probability": 0.7, "magnitude_qualitative": "Medium"
                    },{
                        "order": 2, "source_impact_type": "SupplyChainRisk", "target_entity_type_selector": "Company",
                        "impact_type": "ProductionDelayRisk", "probability": 0.5, "magnitude_qualitative": "Medium"
                    }]
                }
            ]
        }


    def trace_impacts(
        self,
        initial_event_entity: NarrativeEntity,
        knowledge_graph: KnowledgeGraphData,
        depth_levels: int = 2,
        ruleset_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Tracing multi-order impacts of an initial event across the Knowledge Graph.
        """
        print(f"[ImpactAnalyzer] INFO: Tracing impacts for event: {initial_event_entity.id} ({initial_event_entity.name}).")

        impact_chains: List[Dict[str, Any]] = []
        rules_to_apply = self.rulesets.get(ruleset_id or "rs_standard_financial_impacts_v1", [])

        # (event, current_depth, path_taken)
        current_impacts_to_trace = [(initial_event_entity, 0, [])]

        for _ in range(depth_levels):
            next_level_impacts = []
            for triggering_event, depth, path in current_impacts_to_trace:
                if depth >= depth_levels: continue

                for rule in rules_to_apply:
                    # Trigger Matching
                    trigger_conditions = rule.get("trigger", {})
                    event_matches_trigger = False

                    if trigger_conditions.get("event_type") == triggering_event.type:
                        if "sentiment_score_gt" in trigger_conditions:
                            score = getattr(triggering_event, "sentiment_score", None)
                            if score is not None and score > trigger_conditions["sentiment_score_gt"]:
                                event_matches_trigger = True
                        elif "event_subtype_contains" in trigger_conditions:
                            subtype = getattr(triggering_event, "event_subtype", "")
                            if subtype and trigger_conditions["event_subtype_contains"].lower() in subtype.lower():
                                event_matches_trigger = True
                        elif not any(k for k in trigger_conditions if k != "event_type"):
                             event_matches_trigger = True

                    if event_matches_trigger:
                        for impact_def in rule.get("impacts", []):
                            if impact_def.get("order", 1) == depth + 1 :
                                target_selector = impact_def.get('target_entity_type_selector')
                                targets = []

                                # Logic to find targets in KG based on selector and context
                                if depth == 0:
                                    # 1st Order: Look for entities directly matching the selector
                                    # and potentially filtered by event attributes (e.g., affected_sectors)
                                    affected_sectors = getattr(initial_event_entity, "attributes", {}).get("affected_sectors", [])

                                    for entity in knowledge_graph.entities:
                                        if entity.type == target_selector:
                                            # If specific sectors are mentioned, filter
                                            if target_selector == "Industry" and affected_sectors:
                                                if entity.name in affected_sectors:
                                                    targets.append(entity)
                                            else:
                                                # Broad impact (e.g. global news) or just all of that type
                                                # For now, if no filter, we might impact ALL? Or maybe none to be safe?
                                                # Let's say if affected_sectors is empty, we hit none for Industry rule
                                                # to avoid blowing up the graph, unless it's global.
                                                if target_selector == "Industry":
                                                     pass # Need explicit sector for now
                                                elif target_selector == "Company":
                                                    # Maybe key_entities_mentioned
                                                    mentioned_ids = getattr(initial_event_entity, "key_entities_mentioned_ids", [])
                                                    if entity.id in mentioned_ids:
                                                        targets.append(entity)

                                elif depth > 0:
                                    # 2nd+ Order: Find entities related to the triggering entity (which is a previous impact target)
                                    # E.g. Industry (SupplyChainRisk) -> Company (ProductionDelayRisk)
                                    # We need to find entities of type 'target_selector' connected to 'triggering_event.id'

                                    # Triggering event here is the dummy entity created in the previous loop
                                    source_id = triggering_event.id

                                    # Find relationships where source is the triggering entity
                                    for rel in knowledge_graph.relationships:
                                        if rel.source_id == source_id:
                                             target_entity = next((e for e in knowledge_graph.entities if e.id == rel.target_id), None)
                                             if target_entity and target_entity.type == target_selector:
                                                 targets.append(target_entity)
                                        # Also check reverse relationships if appropriate (e.g. Company "is_in" Industry)
                                        # But here the graph is Industry -> Company ("contains") usually
                                        # If our graph is Industry -> Company, then rel.source=Industry.

                                for target in targets:
                                    # Avoid cycles
                                    if target.id in path: continue

                                    new_path = path + [triggering_event.id]
                                    impact_chain_item = {
                                        "impacted_entity_id": target.id,
                                        "impact_type": impact_def.get("impact_type"),
                                        "order": depth + 1,
                                        "probability": impact_def.get("probability"),
                                        "magnitude": impact_def.get("magnitude_qualitative"),
                                        "justification_rule_id": rule.get("rule_id"),
                                        "path": new_path + [target.id],
                                        "triggering_event_id": triggering_event.id
                                    }
                                    impact_chains.append(impact_chain_item)

                                    # Create dummy entity for next level
                                    next_event_for_tracing = NarrativeEntity(
                                        id=target.id,
                                        name=f"Impacted: {impact_def.get('impact_type')} on {target.name}",
                                        type=target.type,
                                        attributes={"source_impact_type": impact_def.get("impact_type")}
                                    )
                                    next_level_impacts.append( (next_event_for_tracing, depth + 1, new_path + [target.id]) )

            current_impacts_to_trace = next_level_impacts
            if not current_impacts_to_trace: break

        print(f"[ImpactAnalyzer] INFO: Found {len(impact_chains)} impacts.")
        return impact_chains

if __name__ == '__main__':
    pass
