# NewsBot: AI-Powered Company News Analysis MVP

NewsBot is a web-based AI application designed to aggregate, analyze, and synthesize news and basic financial data for user-specified companies. This MVP focuses on providing core analysis features with a clean user interface.

## Project Goals
- Aggregate company news and financial data from Finnhub and Alpha Vantage.
- Perform AI-powered sentiment analysis on news articles.
- Implement basic keyword-based news categorization.
- Offer a simple React-based frontend to search for companies and view insights.

## Setup

### API Keys
This project requires API keys from the following services:
- **Finnhub.io:** For company profile and general company news.
- **Alpha Vantage:** For historical stock prices.

1.  Create a file named \`.env\` in the root of the project.
2.  Copy the contents of \`.env.example\` into your new \`.env\` file.
3.  Replace the placeholder values in \`.env\` with your actual API keys.

    Example \`.env\` content:
    \`\`\`
    FINNHUB_API_KEY="YOUR_ACTUAL_FINNHUB_KEY"
    ALPHA_VANTAGE_API_KEY="YOUR_ACTUAL_ALPHA_VANTAGE_KEY"
    \`\`\`

### Running the Application (Placeholder)
Detailed instructions for running the application using Docker Compose will be added once the backend and frontend are further developed.

## Technology Stack (Initial)
*   **Backend:** Python, FastAPI, Pydantic, Hugging Face Transformers
*   **Frontend:** React, TypeScript, Material-UI
*   **Data Sources (MVP):** Finnhub.io, Alpha Vantage

## Project Structure
-   \`/app\`: Main application directory for the FastAPI backend.
-   \`/app/main.py\`: Main FastAPI application instance.
-   \`/app/api\`: API endpoint definitions (routers).
-   \`/app/core\`: Core logic, configuration, and settings.
-   \`/app/models\`: Pydantic models for data structures.
-   \`/app/services\`: Modules for business logic and interacting with external APIs.
-   \`/frontend\`: Directory for the React frontend.
-   \`/tests\`: Unit and integration tests (to be added).

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
