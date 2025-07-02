import json
from pathlib import Path
from typing import Optional

# Assuming base_types.py is in semantic_narrative_library.core_models.python
# Adjust import path if your project structure or PYTHONPATH is different
from ..core_models.python.base_types import KnowledgeGraphData, NarrativeEntity, Driver, Relationship, SemanticLink

# Path to the sample data file
# This assumes the script is run from within the 'semantic_narrative_library/data' directory
# or that the path is adjusted accordingly if run from elsewhere.
DEFAULT_DATA_PATH = Path(__file__).parent / "sample_knowledge_graph.json"

def load_knowledge_graph_from_json(file_path: Path = DEFAULT_DATA_PATH) -> Optional[KnowledgeGraphData]:
    """
    Loads knowledge graph data from a JSON file and parses it into Pydantic models.

    Args:
        file_path (Path): The path to the JSON data file.

    Returns:
        Optional[KnowledgeGraphData]: An instance of KnowledgeGraphData if successful, None otherwise.
    """
    if not file_path.exists():
        print(f"Error: Data file not found at {file_path}")
        return None

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Pydantic will validate the data against the KnowledgeGraphData model
        kg_data = KnowledgeGraphData(**data)
        print(f"Successfully loaded and validated data from {file_path}")
        return kg_data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {file_path}: {e}")
        return None
    except Exception as e: # Catch Pydantic validation errors and other issues
        print(f"Error processing data from {file_path}: {e}")
        return None

def main():
    """
    Main function to demonstrate loading the sample knowledge graph data.
    """
    print(f"Attempting to load data from: {DEFAULT_DATA_PATH.resolve()}")

    kg_data = load_knowledge_graph_from_json()

    if kg_data:
        print(f"\nLoaded {len(kg_data.entities)} entities.")
        for entity in kg_data.entities:
            if isinstance(entity, NarrativeEntity): # Ensure it's the base or a subtype we expect
                 print(f"  - Entity ID: {entity.id}, Name: {entity.name}, Type: {entity.type}")
            else:
                # This handles the case where Pydantic might return dicts if type discrimination isn't perfect
                # For this setup with discriminated unions, it should be fine.
                print(f"  - Entity (raw dict): {entity}")


        print(f"\nLoaded {len(kg_data.drivers)} drivers.")
        for driver in kg_data.drivers:
            print(f"  - Driver ID: {driver.id}, Name: {driver.name}")

        print(f"\nLoaded {len(kg_data.relationships)} relationships.")
        for rel in kg_data.relationships:
            print(f"  - Relationship ID: {rel.id}, Type: {rel.type}, From: {rel.source_id} To: {rel.target_id}")

        if kg_data.semantic_links:
            print(f"\nLoaded {len(kg_data.semantic_links)} semantic links.")
            for slink in kg_data.semantic_links:
                print(f"  - SemanticLink ID: {slink.id}, Metric: {slink.metric_observed}, Element: {slink.narrative_element_id}")

        # Example: Find a specific company
        target_company_id = "comp_alpha"
        company_alpha = next((e for e in kg_data.entities if e.id == target_company_id), None)
        if company_alpha:
            print(f"\nFound company AlphaSoft Inc.: {company_alpha.name}")
            # Further demonstration of accessing attributes if needed
            # if company_alpha.attributes:
            #    print(f"Ticker: {company_alpha.attributes.get('tickerSymbol')}")

        # Example: Find relationships for AlphaSoft Inc.
        print(f"\nRelationships involving {target_company_id}:")
        for rel in kg_data.relationships:
            if rel.source_id == target_company_id or rel.target_id == target_company_id:
                print(f"  - {rel.source_id} --[{rel.type}]--> {rel.target_id}")

if __name__ == "__main__":
    main()
