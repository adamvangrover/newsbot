# AGENTS.md - Guide for Autonomous Contributors

Welcome, Agent. This repository is structured to support "Forward Aligned" development.

## Core Architecture

-   **Backend**: FastAPI (`app/`) using AsyncIO.
-   **Frontend**: React + Vite (`frontend/`).
-   **Logic**:
    -   `semantic_narrative_library/`: Core reasoning engines.
    -   `ImpactAnalyzer`: Deterministic/Probabilistic causal chaining.
    -   `EvolutionarySimulator`: Future scenario projection.
    -   `AsyncAgents`: Autonomous workers.

## Development Guidelines

1.  **Additive Only**: Prefer creating new modules over rewriting old ones unless necessary for bug fixes.
2.  **Async First**: Use `async/await` for all I/O bound operations.
3.  **Event Driven**: Use `app.core.event_bus` to decouple components.
4.  **Verification**: Always run `python -m pytest` or custom verification scripts before submitting.

## Key Files

-   `app/core/async_utils.py`: Task management.
-   `semantic_narrative_library/processing/evolutionary_engine.py`: Future projections.
-   `frontend/src/pages/AgentsOrchestrator.tsx`: Monitor your agents here.

## How to Add an Agent

1.  Inherit from `AsyncAgent` in `semantic_narrative_library/processing/async_agent.py`.
2.  Implement `process()`.
3.  Instantiate and start it in `app/main.py` (or a dedicated orchestrator service).
