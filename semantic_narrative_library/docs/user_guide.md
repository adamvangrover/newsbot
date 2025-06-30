# Semantic Narrative Library - User Guide (Draft)

Welcome to the Semantic Narrative Library! This guide helps you understand and use its components.

## Table of Contents

1.  [Introduction](#introduction)
2.  [System Overview](#system-overview)
3.  [Prerequisites](#prerequisites)
4.  [Running the Backend API](#running-the-backend-api)
5.  [Using the Command-Line Interface (CLI)](#using-the-command-line-interface-cli)
    *   [Accessing Help](#accessing-help)
    *   [Testing Data Load](#testing-data-load)
    *   [Querying Company Information](#querying-company-information)
    *   [Generating Explanations/Narratives for a Company](#generating-explanationsnarratives-for-a-company)
6.  [Using the Web Interface (Frontend Explorer)](#using-the-web-interface-frontend-explorer)
    *   [Running the Frontend](#running-the-frontend)
    *   [Exploring Entities and Companies](#exploring-entities-and-companies)
7.  [Interpreting Outputs](#interpreting-outputs)
    *   [Structured Data (JSON)](#structured-data-json)
    *   [Narratives](#narratives)
8.  [Troubleshooting (Basic)](#troubleshooting-basic)
9.  [Further Information](#further-information)

---

## 1. Introduction

The Semantic Narrative Library is a system designed to store information about entities (like companies, industries), their influencing drivers, and relationships. It can then generate explanations and narratives based on this data. This guide focuses on how to run and interact with its primary interfaces: the backend API, the Command-Line Interface (CLI), and the basic Web Interface.

## 2. System Overview

The library consists of:
-   A **Knowledge Graph Core**: Manages data about entities, drivers, and relationships (currently loaded from a sample JSON file).
-   A **Reasoning Engine** (`SimpleReasoner` for basic tasks, with a framework for more advanced processing components like `ImpactAnalyzer`, `ScenarioModeler`, etc.): Analyzes data to find connections, trace impacts, model scenarios, and generate insights.
-   A **Backend API**: Provides HTTP access to the system's functionalities.
-   A **Command-Line Interface (CLI)**: Allows interaction via terminal commands, including access to basic and planned advanced analyses.
-   A **Web Interface**: A simple React-based frontend for exploring data (primarily for demonstration and testing).
-   An **LLM Integration (Simulated)**: For generating more human-like narratives from basic or advanced analyses.
-   A **Workflow Engine (Conceptual)**: Designed to orchestrate complex analytical tasks using defined templates and rules.

The library is designed to evolve towards more dynamic analyses such as real-time news impact assessment and predictive scenario modeling.

## 3. Prerequisites

-   **Python**: Version 3.8 or higher.
-   **Node.js and npm/yarn**: For running the frontend (recent LTS version of Node.js recommended).
-   **Git**: For cloning the repository.
-   **Docker (Optional)**: For running the backend API in a container (see `semantic_narrative_library/Dockerfile`).
-   Dependencies listed in `semantic_narrative_library/requirements.txt` (for Python parts) and `semantic_narrative_library/frontend/package.json` (for frontend).

**Initial Setup:**
1.  Clone the repository.
2.  Install Python dependencies: `pip install -r semantic_narrative_library/requirements.txt` (from repository root).
3.  Install frontend dependencies: `cd semantic_narrative_library/frontend && npm install` (or `yarn install`).

## 4. Running the Backend API

The backend API must be running for the CLI (some parts, if it were to call the API) and the Web Interface to function fully. The CLI currently uses the Python modules directly.

-   Navigate to the repository root.
-   Run: `uvicorn semantic_narrative_library.api.main:app --reload --port 8000`
-   The API will be available at `http://127.0.0.1:8000`.
-   Interactive documentation: `http://127.0.0.1:8000/docs`.

(Refer to `semantic_narrative_library/api/README.md` for more details).

## 5. Using the Command-Line Interface (CLI)

The CLI provides direct access to some of the library's functionalities.

-   All commands are run from the **repository root directory**.
-   The base command is `python -m semantic_narrative_library.cli.main_cli`.

### Accessing Help
```bash
python -m semantic_narrative_library.cli.main_cli --help
python -m semantic_narrative_library.cli.main_cli [COMMAND] --help
```
Example: `python -m semantic_narrative_library.cli.main_cli query-company --help`

### Testing Data Load
This command verifies that the sample knowledge graph data can be loaded.
```bash
python -m semantic_narrative_library.cli.main_cli test-load
```
You can also specify a custom data file:
```bash
python -m semantic_narrative_library.cli.main_cli --data-file path/to/your_data.json test-load
```

### Querying Company Information
Retrieve details for a specific company by its ID (e.g., `comp_alpha`, `comp_beta` from sample data).
```bash
python -m semantic_narrative_library.cli.main_cli query-company <COMPANY_ID>
```
Example:
```bash
python -m semantic_narrative_library.cli.main_cli query-company comp_alpha
```
To also show its direct drivers:
```bash
python -m semantic_narrative_library.cli.main_cli query-company comp_alpha --show-drivers
```
The output will be in JSON format.

### Generating Explanations/Narratives for a Company
Generate a narrative explanation for a company.
```bash
python -m semantic_narrative_library.cli.main_cli explain-company <COMPANY_ID>
```
Example (using simple reasoner's narrative):
```bash
python -m semantic_narrative_library.cli.main_cli explain-company comp_alpha
```
To use the (simulated) LLM for narrative generation:
```bash
python -m semantic_narrative_library.cli.main_cli explain-company comp_alpha --use-llm
```
This will show the prompt sent to the simulated LLM and its templated response.

### Future CLI Commands (Placeholders)
The CLI includes placeholder commands for more advanced future functionalities. These commands currently print a description of what they would do but are not yet implemented:

-   **`analyze-news`**:
    -   Purpose: To analyze a specific news item's impact on a target company.
    -   Conceptual Usage: `python -m semantic_narrative_library.cli.main_cli analyze-news --news-item-id <NEWS_ID> --target-company-id <COMPANY_ID>`
-   **`run-scenario`**:
    -   Purpose: To run a "what-if" scenario based on a scenario definition file.
    -   Conceptual Usage: `python -m semantic_narrative_library.cli.main_cli run-scenario --scenario-def-path path/to/scenario.json`

You can see help for these with the `--help` flag as well.

## 6. Using the Web Interface (Frontend Explorer)

The web interface provides a basic graphical way to explore the data.

### Running the Frontend
1.  Ensure the Backend API is running (see section 4).
2.  Navigate to the frontend directory: `cd semantic_narrative_library/frontend`
3.  Start the development server: `npm run dev` (or `yarn dev`)
4.  Open your browser to `http://localhost:3000` (or the port indicated by Vite).

(Refer to `semantic_narrative_library/frontend/README.md` for more details).

### Exploring Entities and Companies
-   The main page of the web UI will have sections to:
    -   View predefined entities/drivers (e.g., "ind_tech", "drv_cloud_adoption") using the `EntityViewer`.
    -   Input a Company ID (e.g., `comp_alpha`, `comp_beta`) to see its details, direct drivers, and the simple narrative generated by the backend, displayed by the `CompanyExplorer`.
-   Data is typically shown as raw JSON or simple text for transparency and testing.

## 7. Interpreting Outputs

-   **Structured Data (JSON)**: Many CLI commands and UI components will output data in JSON format. This represents the entities, drivers, and relationships as defined in the system.
-   **Narratives**:
    -   **Simple Narratives**: Generated by the `SimpleReasoner`, these are template-based summaries of a company's key drivers.
    -   **Simulated LLM Narratives**: Generated by the `SimulatedNarrativeGenerator`, these also use templates but mimic the style of an LLM output based on a more detailed prompt. They will be clearly marked as simulated.

## 8. Troubleshooting (Basic)

-   **Python Errors (`ModuleNotFoundError`, etc.)**: Ensure you have installed requirements from `semantic_narrative_library/requirements.txt` and are running commands from the correct directory (usually the repository root). Check your `PYTHONPATH` if issues persist.
-   **Frontend Errors (Cannot connect to API, etc.)**:
    -   Verify the backend API is running and accessible (try `http://localhost:8000/docs` in your browser).
    -   Check the browser's developer console (F12) for error messages.
    -   Ensure the `API_BASE_URL` in `semantic_narrative_library/frontend/src/services/api.ts` matches where your backend is served.
-   **Data Not Found**: If querying for an ID (e.g., `comp_gamma`), ensure it exists in `semantic_narrative_library/data/sample_knowledge_graph.json` or your custom data file.

## 9. Further Information

-   **Developer Notes**: `semantic_narrative_library/docs/developer_notes.md`
-   **API Documentation (Auto-generated)**: Available at `/docs` when the API is running (e.g., `http://localhost:8000/docs`).
-   Individual `README.md` files in subdirectories like `api/`, `frontend/`, `llm_ops/`.

This guide provides a starting point. Explore the different components to get a better feel for the library's capabilities.
