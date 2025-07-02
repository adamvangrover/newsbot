# Developer Notes: Semantic Narrative Library

This document provides notes for developers working on or extending the Semantic Narrative Library.

## Project Structure Overview

The library is organized into the following main directories under `semantic_narrative_library/`:

-   **`api/`**: Contains the FastAPI backend application (`main.py`) and its README.
-   **`cli/`**: Houses the Click-based command-line interface (`main_cli.py`).
-   **`core_models/`**: Defines the core data structures.
    -   `python/`: Pydantic models (`base_types.py`) used by the backend, reasoner, and CLI. Includes base entities and extended types like `NewsItem`, `PoliticalEvent`, etc.
    -   `typescript/`: TypeScript interfaces (`base_types.ts`) for conceptual alignment and potential use by TypeScript clients (like the React frontend). Includes corresponding extended types.
    -   `java/`: Placeholder Java class definitions (`BaseTypes.java`).
-   **`data/`**: Includes sample data (`sample_knowledge_graph.json`) and the Python script to load it (`load_sample_data.py`).
-   **`docs/`**: Project documentation files (like this one).
-   **`frontend/`**: Contains the React + TypeScript frontend application.
-   **`knowledge_graph_schema/`**: Contains schema definition examples for the knowledge graph.
-   **`llm_ops/`**: Scripts and prompts for LLM integration (`narrative_generator.py`, `prompts/`).
-   **`processing/`**: Placeholder Python modules for advanced processing components (`DataIngestor`, `NLProcessor`, `SignificanceScorer`, `ImpactAnalyzer`, `ScenarioModeler`). See `processing/README.md`.
-   **`reasoning_engine/`**: The Python-based `SimpleReasoner` (`simple_reasoner.py`). This would be complemented or superseded by the advanced processing components for more complex tasks.
-   **`tests/`**: Pytest unit tests for the Python components.
-   **`workflows/`**: Conceptual design and examples for a workflow and template engine (`workflow_template_example.json`, `rule_template_example.json`). See `workflows/README.md`.
-   `Dockerfile`: For containerizing the FastAPI backend.
-   `requirements.txt`: Python dependencies for the backend, CLI, and related scripts.

## Core Data Structures (Python - Pydantic)

Located in `semantic_narrative_library/core_models/python/base_types.py`.
Key Pydantic models include:
-   `NarrativeEntity`: Base class for all entities. Its `type` field is `str`.
-   Concrete entity subtypes like `Company`, `Industry`, `MacroIndicator`, `NewsItem`, `PoliticalEvent`, `FinancialReportItem`, `MarketSignal`, `RegulatoryChange`, `Security`. Each of these defines its `type` field as a `Literal` (e.g., `type: Literal["Company"] = "Company"`) to enable Pydantic's discriminated union functionality.
-   `Driver`: Represents influencing factors.
-   `Relationship`: Defines connections between entities/drivers.
-   `SemanticLink`: Connects narrative elements to observable metrics.
-   `KnowledgeGraphData`: Root model for holding lists of entities, drivers, relationships, etc. Its `entities` field uses `ConcreteEntityUnion = Annotated[Union[Company, Industry, ...], Field(discriminator='type')]` to ensure Pydantic correctly parses dictionary data into specific entity Pydantic model instances based on the `type` field.

All core Pydantic models are configured with `model_config = ConfigDict(frozen=True)` to make them hashable and (largely) immutable after creation.

## Advanced Framework Design Patterns (Conceptual)

The introduction of the `processing/` and `workflows/` directories points towards a more sophisticated architecture:

-   **Pipeline Processing**: The components in `processing/` (e.g., `DataIngestor`, `NLProcessor`, `ImpactAnalyzer`) are envisioned as stages in a data processing and analysis pipeline.
-   **Workflow Orchestration**: A (currently conceptual) workflow engine would use templates from `workflows/workflow_template_example.json` to define and execute sequences of operations using the components from `processing/`.
-   **Rule-Based Analysis**: The `ImpactAnalyzer` and `ScenarioModeler` would leverage rule definitions (like those in `workflows/rule_template_example.json`) to determine cause-and-effect, probabilities, and magnitudes of impacts.
-   **Extensibility**: This design allows for adding new processing components, workflow types, and rule sets as the library's capabilities grow.

## Main Components Interaction (Updated View)

1.  **Data Loading (`data/load_sample_data.py`)**:
    -   Loads `sample_knowledge_graph.json`.
    -   Parses the JSON into `KnowledgeGraphData` Pydantic model, performing validation.
    -   This function is called by the `SimpleReasoner` upon initialization, which in turn is used by the API and CLI.

2.  **Reasoning Engine (`reasoning_engine/simple_reasoner.py`)**:
    -   `SimpleReasoner` class takes `KnowledgeGraphData` as input.
    -   Builds internal indexes (dictionaries) for quick lookups of entities and drivers.
    -   Provides methods like `get_entity_by_id`, `find_direct_drivers_for_company`, `generate_simple_narrative_for_company_drivers`.

3.  **API (`api/main.py`)**:
    -   FastAPI application.
    -   On startup, loads data and initializes `SimpleReasoner`.
    -   Exposes HTTP endpoints that call methods on the `SimpleReasoner` instance.
    -   Uses Pydantic models from `core_models` for request/response validation and serialization.
    -   Auto-generates OpenAPI documentation (`/docs`, `/redoc`, `/openapi.json`).

4.  **CLI (`cli/main_cli.py`)**:
    -   Uses the `click` library.
    -   Also loads data and initializes `SimpleReasoner` (lazily on first command needing it).
    -   Provides commands to query company info, drivers, and generate narratives (simple or LLM-simulated).

5.  **LLM Integration (`llm_ops/`)**:
    -   `SimulatedNarrativeGenerator` takes data (e.g., from `SimpleReasoner`) and uses prompt templates from `llm_ops/prompts/` to generate a *simulated* LLM narrative.
    -   The CLI's `explain-company --use-llm` command demonstrates this.
    -   `README.md` in `llm_ops/` discusses API key management for real LLM integration.

6.  **Frontend (`frontend/`)**:
    -   React + TypeScript application.
    -   `services/api.ts` uses `axios` to call the backend FastAPI.
    -   `types/api_types.ts` defines frontend types (aligned with backend Pydantic models).
    -   Components like `CompanyExplorer.tsx` display data fetched from the API.

## Conventions

-   **Python Type Hinting**: Used throughout the Python codebase.
-   **Pydantic**: For data validation and modeling in Python.
-   **Relative Imports**: Python modules within `semantic_narrative_library` use relative imports (e.g., `from ..data.load_sample_data import ...`) to maintain package integrity.
-   **Testing**: `pytest` for Python unit tests located in `semantic_narrative_library/tests/`. Test files are named `test_*.py`.
-   **Modularity**: Components are designed to be as self-contained as possible within their respective directories.

## Running the System

-   **Backend API**: See `semantic_narrative_library/api/README.md`.
-   **Frontend UI**: See `semantic_narrative_library/frontend/README.md`.
-   **CLI**: See `semantic_narrative_library/cli/main_cli.py` comments or run `python -m semantic_narrative_library.cli.main_cli --help`.
-   **Python Tests**: From the repository root, run `python -m pytest semantic_narrative_library/tests/`.

## Potential Areas for Future Development/Refinement

-   **Data Model Refinements**:
    -   Align JSON data structure more closely with Pydantic model fields (e.g., `ticker_symbol` directly on Company object vs. in `attributes`) or use Pydantic field aliases / validators for mapping.
    -   More granular entity types and relationship definitions.
-   **Reasoner Enhancements**: More complex reasoning logic, multi-hop analysis, scoring mechanisms.
-   **Real LLM Integration**: Replace `SimulatedNarrativeGenerator` with actual LLM API calls, including robust error handling and async operations.
-   **Persistent Storage**: Integrate a graph database (e.g., Neo4j) or other database for storing and querying the knowledge graph data, instead of loading from JSON on startup. The `load_sample_data.py` could then be adapted to populate this database.
-   **API Enhancements**: Authentication, pagination for large datasets, more query parameters.
-   **Frontend UI/UX**: More interactive visualizations, user input forms for querying, improved state management.
-   **CI/CD Pipeline**: Automate testing, building Docker images, and deployment.
-   **Configuration Management**: Centralized configuration for data paths, API URLs, etc., instead of hardcoded paths or defaults in multiple places.
-   **Error Handling**: More comprehensive and user-friendly error handling across all layers.
-   **Logging**: Structured logging throughout the backend and other components.
-   **Asynchronous Operations**: For potentially long-running tasks in the reasoner or LLM calls, especially in the API.
-   **Java/TypeScript Core Model Usage**: Currently, Python Pydantic models are central. True cross-language use of core models would require a more robust synchronization or generation strategy (e.g., using OpenAPI schema as the source of truth for data models).

This document should serve as a starting point for developers. Refer to individual module READMEs and code comments for more specific details.
