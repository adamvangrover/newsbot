import json
from pathlib import Path
from typing import Dict, Any, Optional

# Assuming this script is in semantic_narrative_library/llm_ops/
# and prompts are in semantic_narrative_library/llm_ops/prompts/
PROMPT_DIR = Path(__file__).parent / "prompts"

class SimulatedNarrativeGenerator:
    def __init__(self, prompt_template_name: str = "company_narrative_prompt.md"):
        self.prompt_template = self._load_prompt_template(prompt_template_name)

    def _load_prompt_template(self, template_name: str) -> str:
        """Loads a prompt template from the predefined directory."""
        template_file = PROMPT_DIR / template_name
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"Warning: Prompt template '{template_name}' not found at {template_file}.")
            # Return a default basic template or raise an error
            return "Summarize the following data for {{company_name}}:\n{{drivers_json}}"
        except Exception as e:
            print(f"Warning: Error loading prompt template '{template_name}': {e}")
            return "Summarize the following data for {{company_name}}:\n{{drivers_json}}"

    def _fill_prompt(self, template_data: Dict[str, Any]) -> str:
        """Fills the prompt template with provided data."""
        prompt = self.prompt_template
        for key, value in template_data.items():
            placeholder = f"{{{{ {key} }}}}" # Matches {{ key }}
            if isinstance(value, (dict, list)):
                prompt = prompt.replace(placeholder, json.dumps(value, indent=2))
            else:
                prompt = prompt.replace(placeholder, str(value))
        return prompt

    def generate_narrative(self, company_name: str, company_id: str, company_description: str, drivers_info: list) -> str:
        """
        Simulates generating a narrative using an LLM.
        In a real scenario, this function would make an API call to an LLM service.
        """
        template_data = {
            "company_name": company_name,
            "company_id": company_id,
            "company_description": company_description or "N/A",
            "drivers_json": drivers_info
        }

        filled_prompt = self._fill_prompt(template_data)

        print("--- Filled Prompt (Simulated LLM Input) ---")
        print(filled_prompt)
        print("--------------------------------------------")

        # --- SIMULATED LLM CALL ---
        # Replace this with actual LLM API call (e.g., OpenAI, Anthropic, local model)
        # For now, using a template-based response.

        positive_drivers = [d for d in drivers_info if "positive" in d.get("relationship_type", "").lower()]
        negative_drivers = [d for d in drivers_info if "negative" in d.get("relationship_type", "").lower() or "pressure" in d.get("relationship_type", "").lower()]

        narrative = f"**Simulated LLM Narrative for {company_name} ({company_id}):**\n\n"
        narrative += f"{company_name}, {company_description.lower() if company_description else 'a notable entity in its sector'}, faces a dynamic environment shaped by several key drivers. "

        if positive_drivers:
            narrative += "On the positive side, "
            for i, driver_info in enumerate(positive_drivers):
                narrative += f"the '{driver_info['driver_name']}' ({driver_info['relationship_type']})"
                if driver_info.get('impact_potential'):
                    narrative += f" with {driver_info['impact_potential'].lower()} impact potential"
                narrative += " is expected to bolster its performance"
                narrative += ". " if i == len(positive_drivers) - 1 else ", and "

        if negative_drivers:
            narrative += "However, challenges exist. "
            for i, driver_info in enumerate(negative_drivers):
                narrative += f"The driver '{driver_info['driver_name']}' ({driver_info['relationship_type']})"
                if driver_info.get('impact_potential'):
                    narrative += f", which carries a {driver_info['impact_potential'].lower()} impact potential,"
                narrative += " could exert downward pressure or introduce risks"
                narrative += ". " if i == len(negative_drivers) - 1 else ", while "

        if not positive_drivers and not negative_drivers and drivers_info:
            narrative += "Several factors are at play, including " + ", ".join([f"'{d['driver_name']}'" for d in drivers_info]) + ", which require careful monitoring. "
        elif not drivers_info:
             narrative += "There are currently no specific major drivers identified in the provided data, suggesting a stable but potentially uneventful outlook, or a need for more granular data."

        narrative += f"\n\nOverall, the interplay of these factors will be crucial in determining {company_name}'s trajectory. Strategic responses to these influences are paramount."
        narrative += "\n\n(This is a simulated LLM response based on a template.)"

        print("--- Simulated LLM Output ---")
        print(narrative)
        print("-----------------------------")
        return narrative

def example_usage():
    """Example of how to use the SimulatedNarrativeGenerator."""
    # This would typically come from the SimpleReasoner
    from ..data.load_sample_data import load_knowledge_graph_from_json
    from ..reasoning_engine.simple_reasoner import SimpleReasoner

    print("LLM Narrative Generation Example:")
    kg_data = load_knowledge_graph_from_json()
    if not kg_data:
        print("Failed to load KG data for LLM example.")
        return

    reasoner = SimpleReasoner(kg_data)

    company_id_to_test = "comp_alpha"
    company_entity = reasoner.get_entity_by_id(company_id_to_test)

    if company_entity and company_entity.type == "Company": # Basic type check
        company_drivers_info = reasoner.find_direct_drivers_for_company(company_id_to_test)

        generator = SimulatedNarrativeGenerator()
        generated_text = generator.generate_narrative(
            company_name=company_entity.name,
            company_id=company_entity.id,
            company_description=company_entity.description,
            drivers_info=company_drivers_info
        )
        # The generated_text can then be used or displayed.
    else:
        print(f"Could not find company '{company_id_to_test}' or it's not a Company type for LLM example.")

if __name__ == "__main__":
    example_usage()
