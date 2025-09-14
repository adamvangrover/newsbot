# NewsBot System Architecture

## 1. Overview

NewsBot is a web-based AI application designed to aggregate, analyze, and synthesize news and basic financial data for user-specified companies. It provides a clean, interactive UI to display insights, including sentiment analysis, news categorization, and summaries.

The system is designed as a classic two-tier application:

*   **Frontend:** A React (TypeScript) single-page application (SPA) providing the user interface.
*   **Backend:** A FastAPI (Python) application serving as the API layer, handling business logic, data aggregation, and AI processing.

## 2. Components

### 2.1. Frontend ()

*   **Technology:** React with TypeScript, Material-UI for components, Vite for bundling.
*   **Responsibilities:**
    *   User input (company ticker symbol).
    *   Displaying company profile, stock price charts, and news articles.
    *   Rendering AI-driven insights (sentiment, categories, summaries).
    *   Communicating with the backend API via HTTP requests (using Axios).
    *   Client-side state management (React Context API / local state, React Query for server state).

### 2.2. Backend ()

*   **Technology:** Python with FastAPI, Pydantic for data validation, Uvicorn for serving. Hugging Face Transformers for AI tasks.
*   **Responsibilities:**
    *   **API Layer ():** Exposes RESTful endpoints for the frontend. Handles request validation and orchestration.
    *   **Service Layer ():**
        *   : Fetches data from external APIs (Finnhub.io for company news/profile, Alpha Vantage for stock prices). Includes caching and error handling.
        *   : Performs AI-related tasks on news data (sentiment analysis, categorization, summarization) using models from Hugging Face.
    *   **Processing Layer ():** Contains the core logic for individual AI tasks (sentiment, categorization, summarization functions).
    *   **Core ():** Configuration management (environment variables), logging setup.
    *   **Schemas ():** Pydantic models for data validation and serialization (API requests/responses, data structures).

### 2.3. Data Sources (External)

*   **Finnhub.io:** Used for fetching company profiles, news articles.
*   **Alpha Vantage:** Used for fetching historical stock prices.
*   **Hugging Face Model Hub:** Source for pre-trained AI models for NLP tasks.

## 3. Data Flow (Example: Company Analysis Request)

1.  User enters a ticker symbol in the Frontend UI.
2.  Frontend makes a GET request to  on the Backend.
3.  Backend API endpoint receives the request.
4.   is called to fetch:
    *   Company profile from Finnhub.
    *   Recent news from Finnhub.
    *   Historical stock prices from Alpha Vantage.
5.  Raw news articles are passed to the .
6.   uses functions in the  layer to:
    *   Perform sentiment analysis on each article.
    *   Categorize each article.
    *   Generate an AI summary for each article.
7.  The Backend API combines all fetched and processed data into a structured JSON response.
8.  Frontend receives the JSON response and updates the UI to display the information.

## 4. Deployment (Conceptual for MVP)

*   **Docker:** Both frontend and backend applications are containerized using Docker.
*   **:** Used for local development to orchestrate the services.
*   **Production:** Docker images can be deployed to various platforms (e.g., cloud services like AWS ECS, Google Cloud Run, Azure App Service, or a VPS with Docker).
    *   The frontend (Nginx server with static files) and backend (Uvicorn server) run as separate containers.
    *   A reverse proxy (like Nginx or Traefik) might be used in front of the backend in a production setup.

## 5. Key Architectural Considerations

*   **Modularity:** Separation of concerns between frontend, backend, and individual services/modules within the backend.
*   **Scalability:** While the MVP is simple, the containerized nature and service-oriented backend allow for future scaling (e.g., running multiple instances of the backend API).
*   **API-Driven:** The frontend relies entirely on the backend API for data and functionality.
*   **Configuration Management:** API keys and other sensitive settings are managed via environment variables (loaded from  files for local development).

## 6. Portfolio Management Feature (New)

The architecture is extended to support portfolio management with the following additions:

*   **Database:** A new set of tables (`portfolios`, `portfolio_assets`) are added to the database to store user-defined portfolios.
*   **Backend:**
    *   A new API endpoint (`/api/v1/portfolios`) is added to manage portfolios (CRUD operations).
    *   A new service is introduced to handle portfolio-related business logic.
*   **Frontend:**
    *   A new "Portfolio Management" page is added to the UI for creating and managing portfolios.
    *   The "Company Analysis" page is updated to allow users to select a portfolio and view aggregated analysis.

### Data Flow (Example: Portfolio Analysis Request)

1.  User selects a portfolio from the dropdown on the "Company & Portfolio Analysis" page.
2.  Frontend makes a GET request to a new endpoint like `/api/v1/portfolio-analysis/{portfolio_id}` on the Backend.
3.  Backend API endpoint receives the request.
4.  The backend service fetches the list of companies in the portfolio from the database.
5.  For each company in the portfolio, the `DataAggregatorService` fetches news and other relevant data.
6.  The aggregated news from all companies is passed to the `AIProcessingService` for analysis (sentiment, topics, etc.).
7.  The Backend API combines all fetched and processed data into a structured JSON response.
8.  Frontend receives the JSON response and updates the UI to display the aggregated information for the portfolio.

This architecture provides a solid foundation for the MVP and allows for future expansion and refinement.
