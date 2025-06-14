# NewsBot API Strategy

## 1. Overview

The NewsBot backend provides a RESTful API built with FastAPI to serve data and insights to the frontend application. The API is designed to be simple, efficient, and easy to consume.

## 2. Base URL

All API endpoints are prefixed with . For local development, the full base URL is typically .

## 3. Authentication

For the MVP, the API endpoints are unauthenticated. In a production scenario, authentication (e.g., JWT-based, OAuth2) would be implemented to secure the API, especially if user-specific data or rate limiting is required.

## 4. Key Endpoints

### 4.1. Company Analysis

*   **Endpoint:**
*   **Description:** Fetches comprehensive analysis for a given company ticker symbol. This includes company profile, recent news (with AI processing), and historical stock data.
*   **Path Parameters:**
    *    (string, required): The stock ticker symbol for the company (e.g., "AAPL", "MSFT").
*   **Query Parameters:**
    *    (integer, optional, default: 7): Specifies how many days of recent news to fetch. Min: 1, Max: 30.
*   **Successful Response (200 OK):**
    *   **Content-Type:**
    *   **Body:** A JSON object containing the following fields:
        ```json
        {
          "ticker": "string", // The requested ticker symbol
          "profile": { // Optional: CompanyProfile schema
            "country": "string",
            "currency": "string",
            "exchange": "string",
            "name": "string",
            "ticker": "string",
            "ipo": "string",
            "marketCapitalization": "number",
            "shareOutstanding": "number",
            "logo": "string (url)",
            "phone": "string",
            "weburl": "string (url)",
            "finnhubIndustry": "string"
          },
          "news": { // Optional: CompanyNews schema
            "ticker": "string",
            "articles": [ // List of NewsArticle schema
              {
                "id": "string",
                "category": "string", // Original category from source
                "datetime": "integer (unix timestamp)",
                "headline": "string",
                "image": "string (url)",
                "related": "string", // Ticker
                "source": "string",
                "summary": "string",
                "url": "string (url)",
                "sentiment_label": "string (e.g., POSITIVE, NEGATIVE, NEUTRAL, ERROR)",
                "sentiment_score": "number (float)",
                "analyzed_category": "string (e.g., Financial Performance, Product Launch)",
                "ai_summary": "string (AI-generated summary)"
              }
            ]
          },
          "stock_data": { // Optional: HistoricalStockData schema
            "ticker": "string",
            "prices": [ // List of StockDataPoint schema
              {
                "date": "string (YYYY-MM-DD)",
                "open": "number",
                "high": "number",
                "low": "number",
                "close": "number",
                "volume": "integer"
              }
            ]
          }
        }
        ```
*   **Error Responses:**
    *   : If  is invalid.
        ```json
        { "detail": "Invalid ticker symbol format. Use alphanumeric characters." }
        ```
    *   : If the company profile or other critical data for the ticker cannot be found (behavior might vary; currently, it might return partial data).
        ```json
        { "detail": "Company profile not found for ticker: XYZ" } // Example
        ```
    *   : If an unexpected error occurs on the server.
        ```json
        { "detail": "An internal server error occurred: <error_message>" }
        ```
    *   : If an external API (Finnhub, Alpha Vantage) is down or returns an error.
        ```json
        { "detail": "External API service unavailable: <error_message>" }
        ```

### 4.2. Health Check

*   **Endpoint:**
*   **Description:** A simple health check endpoint to verify if the API is running.
*   **Successful Response (200 OK):**
    ```json
    {
      "status": "healthy",
      "timestamp": "string (ISO 8601 datetime)"
    }
    ```

## 5. Data Models (Pydantic Schemas)

The API uses Pydantic models for request and response validation and serialization. Key schemas are defined in:

*   : , , .
*   : , .
*   The combined response model  is defined within .

Refer to these files for detailed field definitions.

## 6. API Key Management

*   The backend manages API keys for external services (Finnhub, Alpha Vantage).
*   These keys are loaded from environment variables (via  file in development) using Pydantic settings ().
*   API keys are **not** exposed to the frontend or in API responses.

## 7. Future Considerations

*   **Pagination:** For endpoints returning lists of items (e.g., news articles if not limited by date).
*   **Rate Limiting:** To prevent abuse of the API.
*   **More Granular Endpoints:** If specific pieces of data (e.g., just profile, just news) are needed independently.
*   **User Accounts & Personalization:** If user-specific settings or saved companies are implemented.
*   **Webhook Support:** For real-time news updates (more advanced).
