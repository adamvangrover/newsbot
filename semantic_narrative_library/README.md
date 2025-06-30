# Semantic Narrative Library

This library aims to provide a modular and comprehensive system for understanding and generating explainable narratives related to various domains, with an initial focus on financial and business contexts. It links core drivers to observable metrics or trading levels, functioning like a knowledge graph combined with a decision tree.
The framework is designed to be extensible towards more dynamic analysis, including news impact assessment, scenario modeling, and continuous learning from new data.

## Core Components:

-   **`api/`**: FastAPI backend application.
-   **`cli/`**: Click-based Command-Line Interface.
-   **`core_models/`**: Data structure definitions (Python Pydantic, TypeScript, Java placeholders).
-   **`data/`**: Sample data (`sample_knowledge_graph.json`) and data loading scripts.
-   **`docs/`**: Project documentation, including developer notes, user guide, and future enhancement details.
-   **`frontend/`**: Basic React + TypeScript frontend explorer.
-   **`knowledge_graph_schema/`**: Schema definitions for the knowledge graph.
-   **`llm_ops/`**: Scripts and prompts for Large Language Model integration (currently simulated).
-   **`reasoning_engine/`**: Python-based `SimpleReasoner` for basic analysis.
-   **`tests/`**: Pytest unit tests for Python components.
-   `Dockerfile`: For containerizing the FastAPI backend.
-   `requirements.txt`: Python dependencies.

## Guiding Principles:

-   **Modular:** Components are designed to be as independent as possible.
-   **Portable:** The backend is containerizable via Docker.
-   **Explainable:** Focus on making the reasoning process and outputs transparent.
-   **LLM-Friendly Core:** Data structures and logic are designed with LLM interaction in mind.

## Getting Started

1.  **Prerequisites**: Python 3.8+, Node.js (for frontend), Docker (optional for backend).
2.  **Installation**:
    -   Clone the repository.
    -   Install Python dependencies: `pip install -r semantic_narrative_library/requirements.txt` (from repo root).
    -   Install frontend dependencies: `cd semantic_narrative_library/frontend && npm install`.
3.  **Running the Backend API**: From repo root: `uvicorn semantic_narrative_library.api.main:app --reload`
4.  **Running the Frontend**: From `semantic_narrative_library/frontend`: `npm run dev`
5.  **Using the CLI**: From repo root: `python -m semantic_narrative_library.cli.main_cli --help`

Refer to the `docs/user_guide.md` and specific README files in subdirectories for more details.

## Future Considerations:

While this initial version provides a functional core, several enhancements are envisioned for the future, including:
-   Integration with persistent graph databases.
-   Advanced reasoning capabilities.
-   Real LLM integration with robust LLMOps.
-   Enhanced frontend UI/UX with visualizations.
-   **Federated Learning capabilities** for privacy-preserving collaborative model improvement.

See `docs/future_enhancements.md` for more details on these and other potential enhancements.

This library is intended to be a self-contained unit within the main project repository.
