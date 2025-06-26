# NewsBot - AI-Powered Company News Analysis MVP

NewsBot is a web-based AI application that aggregates, analyzes, and synthesizes news and basic financial data for user-specified companies. It provides a clean, interactive UI to display insights, including sentiment analysis, news categorization, and summaries.

This project is an MVP (Minimum Viable Product) built with a production-aware mindset, incorporating best practices for API management, AI model integration, and a robust (containerized) architecture.

## Features

*   **Modular UI:** Navigation via a sidebar to access different analysis modules.
*   **Company Analysis Module:**
    *   Search for companies by stock ticker and specify news aggregation period (3-30 days).
    *   View company profile, historical stock prices (chart), and aggregated news.
    *   AI-powered news analysis including:
        *   **Sentiment Analysis:** Positive, negative, or neutral sentiment for each article.
        *   **News Categorization:** Assigns relevant categories (e.g., "Financial Performance").
        *   **AI Summarization:** Generates concise summaries.
        *   **Named Entity Recognition (NER):** Extracts key organizations, persons, locations from news.
        *   **Event Detection:** Flags news related to earnings, M&A, product launches, etc.
*   **Market Outlook Module:**
    *   Provides an overview of general market news (selectable categories like General, Crypto, Forex).
    *   Displays overall market sentiment, key themes derived from news categories and entities, and highlighted market events.
    *   Lists recent market news articles with their full AI analysis (sentiment, NER, events, summary).
*   **Web Scrape & Analyze Module:**
    *   Allows users to input any URL.
    *   The system scrapes the main textual content from the URL.
    *   Performs AI analysis (sentiment, summary, NER, event detection) on the scraped text.
    *   Displays the analysis along with a snippet of the scraped text.
*   **Dockerized:** Both backend and frontend are containerized for easy setup and deployment.

## Tech Stack

*   **Backend:**
    *   Python 3.9+
    *   FastAPI (for the REST API)
    *   Uvicorn (ASGI server)
    *   Hugging Face Transformers (NLP models for sentiment, categorization, summarization, NER, event detection patterns)
    *   Pydantic (data validation and settings)
    *   Requests (HTTP client for external APIs like Finnhub, AlphaVantage)
    *   HTTPX (async HTTP client, used by WebScrapingService)
    *   BeautifulSoup4 (for web scraping HTML content)
    *   Tenacity (for retries)
    *   Python-dotenv (environment variable management)
*   **Frontend:**
    *   React 18+ with TypeScript
    *   React Router DOM (for client-side routing and navigation)
    *   Vite (build tool and dev server)
    *   Material-UI (MUI v5 for UI components)
    *   Axios (HTTP client)
    *   React Query (client-side data fetching and caching)
    *   Chart.js (for stock price charts via `react-chartjs-2`)
*   **Data Sources:**
    *   Finnhub.io (company news, general market news, profiles)
    *   Alpha Vantage (historical stock prices)
*   **Development & Deployment:**
    *   Docker & Docker Compose
    *   Nginx (for serving frontend static files)
    *   GitHub Actions (basic CI for linting)

## Project Structure

The project is organized into two main directories:

*   `backend/`: Contains the FastAPI application.
*   `frontend/`: Contains the React application.

Detailed project structure information can be found in the [Architecture Document](./docs/01-architecture.md).

## Getting Started

### Prerequisites

*   Git
*   Python 3.9+
*   Node.js 18+ (with npm or yarn)
*   Docker & Docker Compose
*   API Keys for:
    *   Finnhub.io
    *   Alpha Vantage

### Local Development (Recommended: Docker Compose)

1.  **Clone the repository:**
    \`\`\`bash
    # Assuming you have access to this repository
    # git clone <repository_url>
    # cd <repository_directory>/newsbot_project_files
    # If you are already in newsbot_project_files, skip cd
    \`\`\`

2.  **Configure Backend API Keys:**
    Copy the example environment file for the backend and add your API keys:
    \`\`\`bash
    cp backend/.env.example backend/.env
    \`\`\`
    Now, edit `backend/.env` with your actual Finnhub and Alpha Vantage API keys.

3.  **Build and Run with Docker Compose:**
    From the `newsbot_project_files/` directory (where this README is located):
    \`\`\`bash
    docker-compose up --build
    \`\`\`
    *   The `--build` flag ensures images are rebuilt if there are changes.
    *   The first build might take several minutes due to dependency installations and AI model downloads.

4.  **Access the Application:**
    *   **Frontend UI:** [http://localhost:3000](http://localhost:3000)
    *   **Backend API Base:** [http://localhost:8000](http://localhost:8000)
    *   **API Health Check:** [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)

For detailed setup instructions, including non-Docker local setup and deployment guidelines, please refer to the [Setup and Deployment Document](./docs/04-setup-and-deployment.md).

## Documentation

This project includes the following detailed documentation in the `docs/` folder:

*   [**01-architecture.md**](./docs/01-architecture.md): System architecture overview.
*   [**02-api-strategy.md**](./docs/02-api-strategy.md): Backend API endpoint details and data models.
*   [**03-ai-models.md**](./docs/03-ai-models.md): Information about the AI models used.
*   [**04-setup-and-deployment.md**](./docs/04-setup-and-deployment.md): Comprehensive setup and deployment instructions.

## Contributing

This is an MVP project. Contributions are welcome! If you'd like to contribute, please consider:

*   **Testing:** Implementing comprehensive unit and integration tests for both backend and frontend.
*   **Error Handling:** Enhancing robustness of error handling across the application, especially in scraping and API interactions.
*   **AI Capabilities:**
    *   Expanding event detection with more sophisticated models or rules.
    *   Adding Topic Modeling for news and scraped content.
    *   Implementing cross-article analysis (e.g., trend detection over time).
    *   Refining "signal from noise" algorithms.
*   **Data Sources:** Integrating more diverse financial and alternative data sources (e.g., SEC EDGAR, social media trends, economic indicators).
*   **Web Scraping:** Improving the web scraping service for better accuracy across diverse websites (e.g., using advanced libraries like Trafilatura, or site-specific adapters).
*   **UI/UX:**
    *   Adding more advanced data visualizations.
    *   Implementing user preferences and dashboard customization.
    *   Refining mobile responsiveness and accessibility.
*   **Newsletter Feature:** Implementing the originally envisioned newsletter generation module.
*   **CI/CD:** Enhancing the CI/CD pipeline with more checks, automated testing, and deployment strategies.
*   Exploring more advanced financial data sources.

Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
