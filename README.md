# AI Company Analyzer

This project is a web-based AI application for aggregating and analyzing comprehensive news and financial data about companies.

## Project Structure

-   `/app`: Main application directory for the FastAPI backend.
-   `/app/main.py`: Main FastAPI application instance.
-   `/app/api`: API endpoint definitions (routers).
-   `/app/core`: Core logic, configuration, and settings.
-   `/app/models`: Pydantic models for data structures.
-   `/app/services`: Modules for interacting with external APIs (API abstraction layer).
-   `/frontend`: Directory for the chosen frontend framework (React/Vue).
-   `/tests`: Unit and integration tests.

## Setup (Manual - for now)

1.  Create the directory structure as outlined above.
2.  Create a Python virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scriptsctivate
    ```
3.  Create `requirements.txt` with the content provided and install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  (Instructions for running the backend and frontend will be added here later)

## Technology Stack

*   **Backend:** Python, FastAPI
*   **Frontend:** React or Vue (to be finalized)
*   **AI:** Hugging Face Transformers
*   **Data Sources:** Various news and financial APIs (e.g., Finnhub, NewsAPI.org/NewsAPI.ai, Alpha Vantage, SEC EDGAR)
