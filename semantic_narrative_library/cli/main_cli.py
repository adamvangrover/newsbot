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

if __name__ == '__main__':
    # To make this CLI runnable for development:
    # 1. Ensure you are in the repository root.
    # 2. Run: python -m semantic_narrative_library.cli.main_cli [COMMANDS]
    # Example: python -m semantic_narrative_library.cli.main_cli query-company comp_alpha --show-drivers
    # Example: python -m semantic_narrative_library.cli.main_cli explain-company comp_alpha --use-llm
    cli()
