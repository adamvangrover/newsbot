import json
from pathlib import Path
from typing import Dict, Any, Optional, List

# Assuming this script is in semantic_narrative_library/llm_ops/
# and prompts are in semantic_narrative_library/llm_ops/prompts/
PROMPT_DIR = Path(__file__).parent / "prompts"

DEFAULT_PROMPT_NAME = "company_narrative_prompt.md" # This is now the detailed impact prompt

class SimulatedNarrativeGenerator:
    def __init__(self, prompt_template_name: str = DEFAULT_PROMPT_NAME):
        self.prompt_template = self._load_prompt_template(prompt_template_name)
        if not self.prompt_template:
            # Fallback if primary prompt fails to load, to prevent errors later
            self.prompt_template = "Error: Main prompt failed to load. Data: {{ company_name }}, Trigger: {{ triggering_event_json }}, Impacts: {{ impact_chains_json }}"


    def _load_prompt_template(self, template_name: str) -> Optional[str]:
        """Loads a prompt template from the predefined directory."""
        template_file = PROMPT_DIR / template_name
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"Warning: Prompt template '{template_name}' not found at {template_file}.")
            # Return a default basic template or raise an error
            return None
        except Exception as e:
            print(f"Warning: Error loading prompt template '{template_name}': {e}")
            return None

    def _fill_prompt(self, template_data: Dict[str, Any]) -> str:
        """Fills the prompt template with provided data."""
        if not self.prompt_template:
            return "Error: Prompt template not loaded."

        prompt = self.prompt_template
        for key, value in template_data.items():
            placeholder = f"{{{{ {key} }}}}" # Matches {{ key }}
            if isinstance(value, (dict, list)):
                prompt = prompt.replace(placeholder, json.dumps(value, indent=2))
            else:
                prompt = prompt.replace(placeholder, str(value))
        return prompt

    def generate_detailed_impact_narrative(
        self,
        company_name: str,
        company_id: str,
        company_description: Optional[str],
        triggering_event_json: Dict[str, Any], # Should be a dict representation of the event
        significance_explanation: Optional[str],
        impact_chains_json: List[Dict[str, Any]]
    ) -> str:
        """
        Simulates generating a detailed impact narrative using an LLM.
        """
        template_data = {
            "company_name": company_name,
            "company_id": company_id,
            "company_description": company_description or "N/A",
            "triggering_event_json": triggering_event_json,
            "significance_explanation": significance_explanation or "Not explicitly assessed.",
            "impact_chains_json": impact_chains_json
        }

        filled_prompt = self._fill_prompt(template_data)

        print("\n--- Filled Detailed Impact Prompt (Simulated LLM Input) ---")
        print(filled_prompt)
        print("----------------------------------------------------------")

        # --- SIMULATED LLM CALL ---
        narrative = f"**Simulated Detailed Impact Narrative for {company_name} ({company_id}):**\n\n"
        narrative += f"An analysis was conducted regarding {company_name} ({company_description or 'no description provided'}) "
        narrative += f"in response to the event: '{triggering_event_json.get('name', 'Unknown Event')}' (ID: {triggering_event_json.get('id', 'N/A')}).\n"
        narrative += f"The significance of this event was determined as: {significance_explanation or 'not available'}\n\n"

        if impact_chains_json:
            narrative += "The potential impact analysis identified the following chains:\n"
            for i, chain_item in enumerate(impact_chains_json):
                narrative += f"- **Order {chain_item.get('order', 'N/A')} Impact:** Type '{chain_item.get('impact_type', 'N/A')}' "
                narrative += f"on entity/target '{chain_item.get('impacted_entity_id', 'N/A')}'. "
                if chain_item.get('probability') is not None:
                    narrative += f"Estimated probability: {chain_item.get('probability')*100:.0f}%. "
                if chain_item.get('magnitude'):
                    narrative += f"Potential magnitude: {chain_item.get('magnitude')}. "
                if chain_item.get('justification_rule_id'):
                    narrative += f"(Justification: {chain_item.get('justification_rule_id')}). "
                narrative += "\n"

            narrative += "\nThis cascade suggests a complex interplay of factors. "
            if any(item.get('probability', 0) > 0.7 for item in impact_chains_json):
                narrative += "Some effects have a notable likelihood. "
            if any(item.get('magnitude', '').lower() in ['high', 'severe'] for item in impact_chains_json):
                narrative += "Certain impacts could be quite significant. "

        else:
            narrative += "The impact analysis did not identify significant cascading effects based on the current rules and data for this specific event.\n"

        narrative += f"\nOverall, {company_name} should carefully monitor developments related to '{triggering_event_json.get('name', 'the triggering event')}' and consider mitigation strategies for the identified potential impacts."
        narrative += "\n\n(This is a simulated LLM response based on a template for detailed impact.)"

        print("\n--- Simulated Detailed Impact LLM Output ---")
        print(narrative)
        print("-------------------------------------------")
        return narrative

def example_detailed_usage():
    """Example of how to use the generator for detailed impact narratives."""
    from ..core_models.python.base_types import Company, NewsItem # For creating sample objects
    from ..processing.impact_analysis_engine import ImpactAnalyzer # To get sample impact chains
    from ..processing.significance_engine import SignificanceScorer
    from ..data.load_sample_data import load_knowledge_graph_from_json


    print("LLM Detailed Impact Narrative Generation Example:")

    # Setup
    kg_data = load_knowledge_graph_from_json()
    if not kg_data:
        print("Failed to load KG data for LLM example.")
        return

    analyzer = ImpactAnalyzer()
    scorer = SignificanceScorer()
    generator = SimulatedNarrativeGenerator() # Uses the updated prompt by default

    # Sample data (in a real workflow, this comes from other components)
    sample_company = Company(id="comp_xyz", name="XYZ Corp", type="Company", description="A global manufacturing leader.")
    sample_trigger_event = NewsItem(
        id="news_xyz_earnings_surprise",
        name="XYZ Corp Reports Unexpectedly Strong Earnings",
        type="NewsItem",
        description="XYZ Corp announced quarterly earnings that surpassed analyst expectations, citing strong demand.",
        sentiment_score=0.85,
        key_entities_mentioned_ids=["comp_xyz"]
    )

    significance_result = scorer.score_event_significance(sample_trigger_event, context_entities=[sample_company])

    # Get sample impact chains (these are simulated within ImpactAnalyzer)
    impact_chains = analyzer.trace_impacts(
        initial_event_entity=sample_trigger_event,
        knowledge_graph=kg_data, # Pass the loaded KG
        depth_levels=2,
        ruleset_id="rs_standard_financial_impacts_v1" # Example ruleset
    )

    # Generate detailed narrative
    generated_text = generator.generate_detailed_impact_narrative(
        company_name=sample_company.name,
        company_id=sample_company.id,
        company_description=sample_company.description,
        triggering_event_json=sample_trigger_event.model_dump(), # Pass as dict
        significance_explanation=significance_result["explanation"],
        impact_chains_json=impact_chains
    )
    # The generated_text can then be used or displayed.

if __name__ == "__main__":
    example_detailed_usage()
