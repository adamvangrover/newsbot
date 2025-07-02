import click
import json
from pathlib import Path
from typing import Optional

# Assuming the CLI is run from the root of the 'semantic_narrative_library'
# or the library is installed/PYTHONPATH is set up.
from ..data.load_sample_data import load_knowledge_graph_from_json, DEFAULT_DATA_PATH
from ..core_models.python.base_types import KnowledgeGraphData, Company
from ..reasoning_engine.simple_reasoner import SimpleReasoner
from ..llm_ops.narrative_generator import SimulatedNarrativeGenerator


# --- Global state for loaded data & reasoner ---
# This is a simple way to load data once for multiple commands.
# For more complex CLIs, consider Click's context object or other state management.
_kg_data: KnowledgeGraphData = None
_reasoner: SimpleReasoner = None
_narrative_generator: SimulatedNarrativeGenerator = None

def get_reasoner(data_path_str: Optional[str] = None) -> SimpleReasoner:
    """Initializes and returns the reasoner, loading data if not already loaded."""
    global _kg_data, _reasoner
    if _reasoner is None:
        data_path = Path(data_path_str) if data_path_str else DEFAULT_DATA_PATH
        click.echo(f"Loading knowledge graph data from: {data_path.resolve()}...")
        _kg_data = load_knowledge_graph_from_json(data_path)
        if not _kg_data:
            raise click.ClickException(f"Failed to load knowledge graph data from {data_path.resolve()}. CLI cannot proceed.")
        _reasoner = SimpleReasoner(_kg_data)
        click.echo("Knowledge graph loaded and reasoner initialized.")
    return _reasoner

def get_narrative_generator() -> SimulatedNarrativeGenerator:
    """Initializes and returns the narrative generator."""
    global _narrative_generator
    if _narrative_generator is None:
        _narrative_generator = SimulatedNarrativeGenerator()
    return _narrative_generator

# --- CLI Command Group ---
@click.group()
@click.option('--data-file', default=None, type=click.Path(exists=True, dir_okay=False, readable=True),
              help=f"Path to the knowledge graph JSON data file. Defaults to sample data.")
@click.pass_context
def cli(ctx, data_file):
    """
    Command-Line Interface for the Semantic Narrative Library.
    """
    ctx.ensure_object(dict)
    # Initialize reasoner here so it's available for all subcommands if needed
    # and data_file option is processed at group level.
    try:
        # Pass data_file to a context object or ensure get_reasoner uses it.
        # For simplicity, get_reasoner will be called by each command that needs it,
        # and it will use the data_file if provided (or default).
        # This is a bit tricky with global state; Click context is better for this.
        # Let's ensure get_reasoner can be called with the specific path from the option.
        ctx.obj['DATA_FILE_PATH'] = data_file # Store for subcommands if they need to trigger loading
        pass
    except Exception as e:
        raise click.ClickException(f"Error during CLI setup: {e}")


@cli.command("test-load")
@click.pass_context
def test_load_data(ctx):
    """Tests loading the knowledge graph data and prints stats."""
    data_file_path = ctx.obj.get('DATA_FILE_PATH')
    reasoner = get_reasoner(data_file_path) # Trigger loading with specific path if provided
    if reasoner.kg_data:
        click.echo("Knowledge graph data loaded successfully.")
        click.echo(f"Entities: {len(reasoner.kg_data.entities)}")
        click.echo(f"Drivers: {len(reasoner.kg_data.drivers)}")
        click.echo(f"Relationships: {len(reasoner.kg_data.relationships)}")
        if reasoner.kg_data.semantic_links:
            click.echo(f"Semantic Links: {len(reasoner.kg_data.semantic_links)}")
    else:
        click.echo("Failed to load knowledge graph data.", err=True)


@cli.command("query-company")
@click.argument("company_id")
@click.option('--show-drivers', is_flag=True, help="Show direct drivers for the company.")
@click.pass_context
def query_company(ctx, company_id: str, show_drivers: bool):
    """
    Retrieves and displays information for a specific COMPANY_ID.
    Optionally shows its direct drivers.
    """
    data_file_path = ctx.obj.get('DATA_FILE_PATH')
    reasoner = get_reasoner(data_file_path)

    company = reasoner.get_entity_by_id(company_id)

    if not company:
        click.echo(f"Error: Company with ID '{company_id}' not found.", err=True)
        return

    if company.type != "Company":
        click.echo(f"Error: Entity with ID '{company_id}' is a {company.type}, not a Company.", err=True)
        return

    click.echo(f"--- Company Details: {company.name} ({company.id}) ---")
    # Pydantic models have .model_dump_json() in v2
    click.echo(json.dumps(company.model_dump(), indent=2))

    if show_drivers:
        click.echo("\n--- Direct Drivers ---")
        drivers_info = reasoner.find_direct_drivers_for_company(company_id)
        if drivers_info:
            click.echo(json.dumps(drivers_info, indent=2))
        else:
            click.echo(f"No direct drivers found for {company.name}.")


@cli.command("explain-company")
@click.argument("company_id")
@click.option('--use-llm', is_flag=True, help="Use the (simulated) LLM for narrative generation.")
@click.pass_context
def explain_company(ctx, company_id: str, use_llm: bool):
    """
    Generates and displays an explanation/narrative for a specific COMPANY_ID.
    Uses SimpleReasoner's basic narrative by default, or simulated LLM if --use-llm is passed.
    """
    data_file_path = ctx.obj.get('DATA_FILE_PATH')
    reasoner = get_reasoner(data_file_path)

    company_entity = reasoner.get_entity_by_id(company_id)

    if not company_entity:
        click.echo(f"Error: Company with ID '{company_id}' not found.", err=True)
        return

    if company_entity.type != "Company": # Should be Company model due to Pydantic v2 discriminated union
        click.echo(f"Error: Entity '{company_id}' is not a Company (type: {company_entity.type}).", err=True)
        return
    # Now we are sure company_entity is a Company Pydantic model instance
    # No need to cast typically, but for type hinting or explicit access:
    # current_company: Company = company_entity

    click.echo(f"--- Explanation for: {company_entity.name} ({company_entity.id}) ---")
    if use_llm:
        click.echo("Using Simulated LLM Narrative Generator...")
        narr_gen = get_narrative_generator()
        drivers_info = reasoner.find_direct_drivers_for_company(company_id)
        narrative = narr_gen.generate_narrative(
            company_name=company_entity.name,
            company_id=company_entity.id,
            company_description=company_entity.description,
            drivers_info=drivers_info
        )
    else:
        click.echo("Using SimpleReasoner Narrative Generator...")
        narrative = reasoner.generate_simple_narrative_for_company_drivers(company_id)

    click.echo(narrative)


# --- Placeholder CLI Commands for Advanced Framework ---

@cli.command("analyze-news")
@click.option('--news-item-id', required=True, help="ID of the NewsItem to analyze.")
@click.option('--target-company-id', required=True, help="ID of the Company to assess impact on.")
@click.pass_context
def analyze_news(ctx, news_item_id: str, target_company_id: str):
    """
    (Future Command) Analyzes a news item for its impact on a company.
    This would conceptually use NLProcessor, SignificanceScorer, ImpactAnalyzer, NarrativeGenerator.
    """
    click.echo(f"--- (Placeholder) News Impact Analysis ---")
    click.echo(f"News Item ID: {news_item_id}")
    click.echo(f"Target Company ID: {target_company_id}")
    click.echo("This command would perform the following (conceptual steps):")
    click.echo("  1. Fetch NewsItem and Company entities from the Knowledge Graph.")
    click.echo("  2. (NLProcessor) Enhance NewsItem with NLP data (sentiment, entities) if needed.")
    click.echo("  3. (SignificanceScorer) Score the significance of the news for the company.")
    click.echo("  4. (ImpactAnalyzer) Trace potential multi-order impacts on the company using rules.")
    click.echo("  5. (NarrativeGenerator) Generate a detailed narrative of the findings.")
    click.echo("\nThis functionality is not yet implemented.")
    # Example of how it might be structured:
    # reasoner = get_reasoner(ctx.obj.get('DATA_FILE_PATH'))
    # news_item = reasoner.get_entity_by_id(news_item_id)
    # company = reasoner.get_entity_by_id(target_company_id)
    # if not news_item or news_item.type != "NewsItem" or not company or company.type != "Company":
    #     click.echo("Error: Valid NewsItem and Company IDs required.", err=True)
    #     return
    # ... instantiate processing components ...
    # ... call their methods ...
    # ... print results ...


@cli.command("run-scenario")
@click.option('--scenario-def-path', required=True, type=click.Path(exists=True, dir_okay=False, readable=True),
              help="Path to a JSON file defining the what-if scenario.")
@click.pass_context
def run_scenario(ctx, scenario_def_path: str):
    """
    (Future Command) Runs a 'what-if' scenario from a scenario definition file.
    This would conceptually use the ScenarioModeler.
    """
    click.echo(f"--- (Placeholder) What-If Scenario Analysis ---")
    try:
        with open(scenario_def_path, 'r') as f:
            scenario_def = json.load(f)
        click.echo(f"Loaded scenario definition: {scenario_def.get('name', 'Unnamed Scenario')}")
    except Exception as e:
        click.echo(f"Error loading scenario definition from {scenario_def_path}: {e}", err=True)
        return

    click.echo("This command would perform the following (conceptual steps):")
    click.echo("  1. Load the base Knowledge Graph.")
    click.echo("  2. (ScenarioModeler) Apply modifications from the scenario definition to a copy of the KG.")
    click.echo("  3. (ImpactAnalyzer) Trace impacts of the scenario's triggers/changes within the modified KG.")
    click.echo("  4. Report potential outcomes and generate a scenario narrative.")
    click.echo("\nThis functionality is not yet implemented.")


if __name__ == '__main__':
    # To make this CLI runnable for development:
    # 1. Ensure you are in the repository root.
    # 2. Run: python -m semantic_narrative_library.cli.main_cli [COMMANDS]
    # Example: python -m semantic_narrative_library.cli.main_cli query-company comp_alpha --show-drivers
    # Example: python -m semantic_narrative_library.cli.main_cli explain-company comp_alpha --use-llm
    cli()
