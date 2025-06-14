# NewsBot - AI-Powered Company News Analysis MVP

NewsBot is a web-based AI application that aggregates, analyzes, and synthesizes news and basic financial data for user-specified companies. It provides a clean, interactive UI to display insights, including sentiment analysis, news categorization, and summaries.

This project is an MVP (Minimum Viable Product) built with a production-aware mindset, incorporating best practices for API management, AI model integration, and a robust (containerized) architecture.

## Features

*   **Company Search:** Look up companies by their stock ticker symbol.
*   **Company Profile:** View basic company information (name, industry, exchange, logo, etc.).
*   **Historical Stock Prices:** Display a chart of recent stock performance.
*   **Aggregated News:** Fetches recent news articles from financial sources.
*   **AI-Powered News Analysis:**
    *   **Sentiment Analysis:** Determines the sentiment (positive, negative, neutral) of each news article.
    *   **News Categorization:** Assigns relevant categories (e.g., "Financial Performance," "Product Launch") to news articles.
    *   **AI Summarization:** Generates concise summaries of news articles.
*   **Interactive UI:** Clean and responsive user interface built with React and Material-UI.
*   **Dockerized:** Both backend and frontend are containerized for easy setup and deployment.

## Tech Stack

*   **Backend:**
    *   Python 3.9+
    *   FastAPI (for the REST API)
    *   Uvicorn (ASGI server)
    *   Hugging Face Transformers (for NLP models: sentiment, categorization, summarization)
    *   Pydantic (data validation and settings)
    *   Requests (HTTP client for external APIs)
    *   Tenacity (for retries)
    *   Python-dotenv (environment variable management)
*   **Frontend:**
    *   React 18+ with TypeScript
    *   Vite (build tool and dev server)
    *   Material-UI (MUI v5 for UI components)
    *   Axios (HTTP client)
    *   React Query (client-side data fetching and caching)
    *   Chart.js (for stock price charts via `react-chartjs-2`)
*   **Data Sources:**
    *   Finnhub.io (company news, profiles)
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

*   Implementing more robust error handling.
*   Adding unit and integration tests for backend and frontend.
*   Expanding the AI capabilities (e.g., Named Entity Recognition, Topic Modeling).
*   Improving UI/UX and adding more data visualizations.
*   Enhancing the CI/CD pipeline.
*   Exploring more advanced financial data sources.

Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
