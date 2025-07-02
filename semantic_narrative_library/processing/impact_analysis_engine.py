from typing import List, Dict, Any, Optional, Tuple
import json # For loading rules from file
from pathlib import Path # For path manipulation

from ..core_models.python.base_types import KnowledgeGraphData, NarrativeEntity, Relationship, NewsItem, PoliticalEvent, FinancialReportItem # For example typing
# from ..workflows.rule_template_example import Rule # Conceptual import if rules were Pydantic models

# Path to the example rules, assuming this script is in processing/ and workflows/ is a sibling
EXAMPLE_RULE_FILE_PATH = Path(__file__).parent.parent / "workflows" / "rule_template_example.json"


class ImpactAnalyzer:
    """
    Placeholder for a service that analyzes and traces the potential impacts
    of an event or driver across the knowledge graph.
    """

    def __init__(self, rule_file_path: Optional[str] = None, load_example_rules: bool = True):
        print(f"[ImpactAnalyzer] INFO: Initialized ImpactAnalyzer (simulated).")
        self.rulesets: Dict[str, List[Dict[str, Any]]] = {}

        actual_rule_file_path = Path(rule_file_path) if rule_file_path else EXAMPLE_RULE_FILE_PATH if load_example_rules else None

        if actual_rule_file_path and actual_rule_file_path.exists():
            try:
                with open(actual_rule_file_path, 'r') as f:
                    rules_data = json.load(f)
                # Assuming the JSON file contains a top-level key for the ruleset ID, e.g., "ruleset_id"
                # and a "rules" key for the list of rules.
                ruleset_id = rules_data.get("ruleset_id", "rs_loaded_from_file")
                self.rulesets[ruleset_id] = rules_data.get("rules", [])
                print(f"[ImpactAnalyzer] INFO: Loaded ruleset '{ruleset_id}' from {actual_rule_file_path} with {len(self.rulesets[ruleset_id])} rules.")
            except Exception as e:
                print(f"[ImpactAnalyzer] WARN: Could not load rules from {actual_rule_file_path}: {e}")

        if not self.rulesets: # Fallback if loading failed or no path/example specified
             self.rulesets["rs_standard_financial_impacts_v1"] = [ # Default mock internal rules
                {
                    "rule_id": "internal_fallback_positive_news",
                    "description": "Fallback: Highly positive news can boost short-term outlook.",
                    "trigger": {"event_type": "NewsItem", "conditions": [{"field": "sentiment_score", "operator": "greater_than_or_equal_to", "value": 0.7}]},
                    "impacts": [{"order": 1, "target_entity_type": "Company", "impact_type": "PositiveShortTermOutlook", "probability": 0.6, "magnitude_qualitative": "Low"}]
                },
                {
                    "rule_id": "fallback_rule_supply_chain_disruption_sim",
                    "description": "Fallback: Trade restrictions can cause supply chain risks.",
                    "trigger": {"event_type": "PoliticalEvent", "conditions": [{"field": "event_subtype", "operator": "contains", "value": "TradeRestriction"}]},
                    "impacts": [
                        {"order": 1, "target_entity_type": "Industry", "impact_type": "SupplyChainRisk", "probability": 0.7, "magnitude_qualitative": "Medium"},
                        {"order": 2, "source_impact_type": "SupplyChainRisk", "target_entity_type": "Company", "impact_type": "ProductionDelayRisk", "probability": 0.5, "magnitude_qualitative": "Medium"}
                    ]
                }]
             print(f"[ImpactAnalyzer] INFO: Using fallback internal ruleset for 'rs_standard_financial_impacts_v1'.")

    def _check_condition(self, entity_attribute_value: Any, operator: str, condition_value: Any) -> bool:
        """Helper to check a single condition."""
        if operator == "equals": return entity_attribute_value == condition_value
        if operator == "greater_than_or_equal_to": return entity_attribute_value >= condition_value
        if operator == "greater_than": return entity_attribute_value > condition_value
        if operator == "less_than_or_equal_to": return entity_attribute_value <= condition_value
        if operator == "less_than": return entity_attribute_value < condition_value
        if operator == "contains":
            if isinstance(entity_attribute_value, str) and isinstance(condition_value, str):
                return condition_value.lower() in entity_attribute_value.lower()
            if isinstance(entity_attribute_value, list):
                return condition_value in entity_attribute_value
        if operator == "exists": return entity_attribute_value is not None
        # Add more operators as needed (startswith, endswith, regex, etc.)
        print(f"[ImpactAnalyzer._check_condition] WARN: Unknown operator '{operator}'")
        return False

    def _match_trigger(self, event: NarrativeEntity, trigger_def: Dict[str, Any]) -> bool:
        """Checks if an event matches a rule's trigger definition."""
        if event.type != trigger_def.get("event_type"):
            return False

        conditions = trigger_def.get("conditions", [])
        if not conditions: # If only event_type is specified, it's a match
            return True

        for cond in conditions:
            field_path = cond["field"].split('.') # e.g., "sentiment_score" or "attributes.some_key"

            current_value = event
            try:
                for part in field_path:
                    if isinstance(current_value, dict): # For attributes
                        current_value = current_value.get(part)
                    else: # Pydantic model field
                        current_value = getattr(current_value, part, None)
                    if current_value is None: break # Path not found
            except AttributeError:
                current_value = None # Field does not exist on model

            # If field_path was trying to access an attribute that doesn't exist on the event, current_value would be None.
            # For 'exists' operator, if current_value is None (path not found), it means it doesn't exist.
            # For other operators, if current_value is None, it typically means the condition can't be met unless the operator handles None.

            val_for_condition_check = None
            if cond["operator"] not in ["exists", "not_exists"]: # Operators that don't need a comparison value from the rule
                if "value" not in cond:
                    print(f"[ImpactAnalyzer._match_trigger] WARN: Rule condition {cond} is missing 'value' for operator '{cond['operator']}'. Condition fails.")
                    return False
                val_for_condition_check = cond["value"]

            # If current_value is None (field not found on event) and operator is not 'exists'/'not_exists',
            # it usually means the condition cannot be true unless operator specifically handles None.
            if current_value is None and cond["operator"] not in ["exists", "not_exists"]: # 'exists' handles None directly.
                 # For other operators, if the field isn't there, it can't match a value.
                if cond["operator"] == "equals" and val_for_condition_check is None: # field is None == value is None
                    pass # This could be a match
                else:
                    return False # Field not present, so condition (other than exists) fails.

            if not self._check_condition(current_value, cond["operator"], val_for_condition_check):
                return False # Condition not met
        return True # All conditions met

    def _find_target_entities(self, knowledge_graph: KnowledgeGraphData, impact_def: Dict[str, Any], current_trigger_event: NarrativeEntity, initial_event_entity: NarrativeEntity) -> List[NarrativeEntity]:
        """
        Simulates finding target entities in the KG based on selector conditions.
        This is highly simplified. A real implementation needs robust KG querying.
        Args:
            knowledge_graph: The KG data.
            impact_def: The definition of the impact from a rule.
            current_trigger_event: The event (initial or conceptual impact) that triggered the current rule.
            initial_event_entity: The very first event that started the whole chain (for broader context if needed).
        """
        target_type = impact_def.get("target_entity_type")
        conditions = impact_def.get("target_selector_conditions", [])

        potential_targets = [e for e in knowledge_graph.entities if e.type == target_type]

        # If no specific conditions, but the target_type is Company and initial event mentioned a company
        # or is a financial report for a company, we can infer that company as a target.
        if not conditions and target_type == "Company":
            if isinstance(initial_event_entity, NewsItem) and initial_event_entity.key_entities_mentioned_ids:
                # Target the first mentioned company for simplicity if it exists in KG
                for mentioned_id in initial_event_entity.key_entities_mentioned_ids:
                    for entity in potential_targets: # potential_targets are all Companies
                        if entity.id == mentioned_id:
                            return [entity]
            elif isinstance(initial_event_entity, FinancialReportItem):
                 for entity in potential_targets:
                     if entity.id == initial_event_entity.company_id:
                         return [entity]

        # Very simplified condition matching for simulation
        # A real system would use a graph query language or complex attribute matching.
        if conditions:
            # Example: if a condition is {"field": "id", "operator": "equals", "value_ref": "target_company_id"}
            # This part is too complex to fully simulate here without more context on value_ref.
            # For now, if there are conditions, assume it finds one matching target for simulation.
            if potential_targets: return [potential_targets[0]] # Just return the first one of the type for demo

        # If no conditions and not a directly inferable company, and target_type is general (like 'Industry')
        # it might apply to the industry related to the initial event (if applicable)
        if not conditions and target_type == "Industry":
            if isinstance(initial_event_entity, NewsItem) and initial_event_entity.key_entities_mentioned_ids:
                 # Find first company mentioned, then its industry
                for mentioned_id in initial_event_entity.key_entities_mentioned_ids:
                    comp = next((e for e in knowledge_graph.entities if e.id == mentioned_id and e.type == "Company"), None)
                    if comp and hasattr(comp, 'industry_id') and getattr(comp, 'industry_id'):
                        ind = next((i for i in knowledge_graph.entities if i.id == getattr(comp, 'industry_id') and i.type == "Industry"), None)
                        if ind: return [ind]
                        break # Found a company, no need to check other mentions for industry

            # Fallback: if any targets of this type exist, pick one for simulation if no conditions.
            if not conditions and potential_targets: return [potential_targets[0]]

        # If conditions are present, try to filter (simplified)
        if conditions and potential_targets:
            # This is where the value_from_trigger_attribute would be used.
            # For simulation, we assume one condition like:
            # {"field": "industry_id", "operator": "equals", "value_from_trigger_attribute": "source_industry_id"}
            # And current_trigger_event.attributes might have "source_industry_id"
            filtered_targets = []
            for pt in potential_targets:
                match_all_conds = True
                for cond in conditions:
                    cond_field = cond.get("field")
                    cond_op = cond.get("operator")
                    cond_val_literal = cond.get("value")
                    cond_val_from_trigger_attr = cond.get("value_from_trigger_attribute")

                    target_attr_val = getattr(pt, cond_field, None)
                    if target_attr_val is None and pt.attributes: # Check attributes dict
                        target_attr_val = pt.attributes.get(cond_field)

                    val_to_check_against = None
                    if cond_val_from_trigger_attr:
                        # Get value from the current_trigger_event's attributes
                        if current_trigger_event.attributes:
                            val_to_check_against = current_trigger_event.attributes.get(cond_val_from_trigger_attr)
                        if val_to_check_against is None: # If not in attributes, maybe it's a direct field of current_trigger_event
                             val_to_check_against = getattr(current_trigger_event, cond_val_from_trigger_attr, None)
                    else:
                        val_to_check_against = cond_val_literal

                    if target_attr_val is None or val_to_check_against is None: # Cannot compare if one value is missing
                        match_all_conds = False; break

                    if not self._check_condition(target_attr_val, cond_op, val_to_check_against):
                        match_all_conds = False; break

                if match_all_conds:
                    filtered_targets.append(pt)
            return filtered_targets # Could be empty if no match

        return [] # No targets found


    def trace_impacts(
        self,
        initial_event_entity: NarrativeEntity, # The very first event that started the whole chain
        knowledge_graph: KnowledgeGraphData,
        depth_levels: int = 2,
        ruleset_id: Optional[str] = "rs_standard_financial_impacts_v1" # Default to main ruleset
    ) -> List[Dict[str, Any]]:
        """
        Refined placeholder for tracing multi-order impacts of an initial event.
        Uses more detailed rule matching and simulated target selection.
        """
        print(f"[ImpactAnalyzer] INFO: Simulating refined impact tracing for event: {initial_event_entity.id} ({initial_event_entity.name}).")
        print(f"  Depth: {depth_levels}, Ruleset: {ruleset_id}")

        all_generated_impacts: List[Dict[str, Any]] = []

        # Queue for (event_to_trace, current_depth, full_path_ids_list)
        # An "event_to_trace" can be the initial event, or a conceptual "impact event" derived from a previous impact.
        queue: List[Tuple[NarrativeEntity, int, List[str]]] = [(initial_event_entity, 0, [])]

        processed_event_ids_at_depth = set() # To avoid re-processing same event at same depth in cycles

        while queue:
            current_event, current_depth, current_path = queue.pop(0)

            if current_depth >= depth_levels:
                continue

            event_depth_key = (current_event.id, current_depth)
            if event_depth_key in processed_event_ids_at_depth:
                continue
            processed_event_ids_at_depth.add(event_depth_key)

            rules_to_apply = self.rulesets.get(ruleset_id, [])
            if not rules_to_apply:
                print(f"[ImpactAnalyzer] WARN: No rules found for ruleset_id: {ruleset_id}")
                # Removed break here, as other items in queue might use different rulesets if logic was extended
                # For now, with single ruleset_id, this effectively stops if ruleset is missing.

            for rule in rules_to_apply:
                if self._match_trigger(current_event, rule.get("trigger", {})):
                    # Rule's main trigger matches the current_event (which could be initial or a conceptual impact)
                    for impact_def in rule.get("impacts", []):
                        # All impacts defined in this rule are considered direct (order +1) consequences of current_event
                        # The 'order' field in impact_def is relative to this rule's trigger (should typically be 1)
                        # The overall order in the chain is determined by current_depth + 1.

                        target_entities = self._find_target_entities(
                            knowledge_graph,
                            impact_def,
                            current_event, # Pass the current event that triggered this rule
                            initial_event_entity # Pass the original event for broader context if needed
                        )

                        for target_entity in target_entities:
                            # Path construction needs to be careful to avoid duplicating current_event.id if it's already in current_path
                            # current_path is path TO current_event. new_full_path is path TO target_entity.
                            path_to_current_event = current_path + ([current_event.id] if current_event.id not in current_path else [])
                            new_full_path = path_to_current_event + [target_entity.id]

                            impact_data = {
                                "source_event_id": current_event.id,
                                "source_event_name": current_event.name,
                                "target_entity_id": target_entity.id,
                                "target_entity_name": target_entity.name,
                                "target_entity_type": target_entity.type,
                                "impact_type": impact_def.get("impact_type"),
                                "order_in_chain": current_depth + 1, # Overall order
                                "rule_defined_impact_order": impact_def.get("order", 1), # Order within the rule
                                "probability": impact_def.get("probability"),
                                "magnitude": impact_def.get("magnitude_qualitative"),
                                "timescale": impact_def.get("timescale"),
                                "justification_rule_id": rule.get("rule_id"),
                                "explanation_template": impact_def.get("explanation_template"),
                                "full_path_ids": new_full_path
                            }
                            all_generated_impacts.append(impact_data)

                            # For next level of tracing, create a conceptual "impact event"
                            if current_depth + 1 < depth_levels:
                                conceptual_next_event = NarrativeEntity(
                                    id=f"impact_{target_entity.id}_{impact_def.get('impact_type', 'unknown')}",
                                    name=f"Impact: {impact_def.get('impact_type')} on {target_entity.name}",
                                    type=impact_def.get("impact_type"), # Key: this impact type becomes the event type for next iteration
                                    # Pass attributes from the target entity that might be relevant for next rules
                                    attributes=target_entity.attributes.copy() if target_entity.attributes else {},
                                    # Could also add source_event_id or rule_id if needed for context in next step's rules
                                )
                                # Add original rule's target_selector_conditions to attributes if they might be useful for chained rule triggers
                                # For example, if a rule triggers on an "Industry" impact and needs to know which industry
                                if impact_def.get("target_entity_type") == "Industry":
                                     conceptual_next_event.attributes["source_industry_id"] = target_entity.id


                                queue.append((conceptual_next_event, current_depth + 1, path_to_current_event))

        print(f"[ImpactAnalyzer] INFO: Simulated {len(all_generated_impacts)} total impact items across all levels.")
        return all_generated_impacts

if __name__ == '__main__':
    from ..data.load_sample_data import load_knowledge_graph_from_json
    from ..core_models.python.base_types import NewsItem, PoliticalEvent

    analyzer = ImpactAnalyzer()
    sample_kg_data = load_knowledge_graph_from_json() # Load the actual KG to pass

    if sample_kg_data:
        print("\n--- Simulating Impact Analysis for Positive News ---")
        positive_news = NewsItem(
            id="news_ext_pos_001", name="Very Positive Report on AlphaCorp", type="NewsItem",
            sentiment_score=0.8, key_entities_mentioned_ids=["comp_alpha"]
        )
        impacts_news = analyzer.trace_impacts(positive_news, sample_kg_data, depth_levels=1, ruleset_id="rs_standard_financial_impacts_v1")
        for impact in impacts_news:
            print(impact)

        print("\n--- Simulating Impact Analysis for Political Event (Trade Restriction) ---")
        trade_event = PoliticalEvent(
            id="pol_trade_001", name="New Trade Tariffs Announced", type="PoliticalEvent",
            event_subtype="TradeRestriction", location="Global", # Matched rule's "value" for subtype
            attributes={"affected_sectors": ["ind_auto", "ind_tech"]} # Ensure this attribute exists for rule matching
        )
        impacts_political = analyzer.trace_impacts(trade_event, sample_kg_data, depth_levels=2, ruleset_id="rs_standard_financial_impacts_v1")
        for impact in impacts_political:
            print(impact)
    else:
        print("Could not load sample KG data for ImpactAnalyzer example.")
