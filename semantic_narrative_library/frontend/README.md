# Semantic Narrative Library - Frontend Explorer

This directory contains a basic React + TypeScript frontend application built with Vite to explore and interact with the Semantic Narrative Library's backend API.

## Overview

The frontend provides a simple user interface to:
- View details of entities (like industries, companies, drivers).
- Explore drivers and narratives associated with specific companies.
- Serve as a test harness for the backend API functionality.

## Key Components:

-   **`src/`**: Contains the main source code.
    -   **`App.tsx`**: The root React component, orchestrating the layout and main views.
    -   **`main.tsx`**: The entry point for the React application.
    -   **`components/`**: Reusable React components.
        -   `EntityViewer.tsx`: A component to display details of a generic entity or driver.
        -   `CompanyExplorer.tsx`: A component to display details, drivers, and narratives for a specific company.
    -   **`services/api.ts`**: Contains functions for making HTTP requests to the backend API using `axios`.
    -   **`types/api_types.ts`**: TypeScript type definitions for API request/response payloads, largely mirroring the backend's Pydantic models.
    -   `index.html`: The main HTML page.
    -   Styling files (`index.css`, `App.css`).
-   **`package.json`**: Defines project metadata, dependencies (React, Vite, Axios, TypeScript, etc.), and scripts.
-   **`vite.config.ts`**: Configuration for the Vite build tool, including development server settings and path aliases.
-   **`tsconfig.json`**: TypeScript compiler options for the project.

## Running the Frontend:

1.  **Prerequisites**:
    *   Node.js (which includes npm) or Yarn. It's recommended to use a recent LTS version of Node.js.
    *   The backend API from `semantic_narrative_library/api/` must be running (typically on `http://localhost:8000`).

2.  **Setup**:
    *   Navigate to this frontend directory:
        ```bash
        cd semantic_narrative_library/frontend
        ```
    *   Install dependencies:
        ```bash
        npm install
        # or
        # yarn install
        ```

3.  **Execution (Development Mode)**:
    *   Run the Vite development server:
        ```bash
        npm run dev
        # or
        # yarn dev
        ```
    *   This will typically start the frontend application on `http://localhost:3000` (or another port if 3000 is busy) and open it in your default web browser.
    *   The Vite dev server uses Hot Module Replacement (HMR) for a fast development experience.
    *   API requests are proxied to `http://localhost:8000` as configured in `vite.config.ts` (if proxy is enabled and backend is on a different port/setup), or directly if `API_BASE_URL` in `src/services/api.ts` is set accordingly. Currently, `api.ts` points directly to `http://localhost:8000`.

4.  **Building for Production**:
    *   To create an optimized static build:
        ```bash
        npm run build
        # or
        # yarn build
        ```
    *   The production-ready files will be placed in the `dist/` directory. These can then be served by any static file server.

## Using the Interface:

-   The main page (`App.tsx`) provides input fields or selections to specify entities or companies.
-   `EntityViewer` and `CompanyExplorer` components fetch data from the backend API and display it, primarily as formatted JSON strings. This serves to demonstrate and verify backend functionality.

## Current Focus:

This frontend is currently focused on:
-   Providing a basic, functional interface for interacting with the backend.
-   Demonstrating end-to-end data flow.
-   Acting as a test harness for API endpoints.

It is not (yet) a polished, feature-rich user interface with advanced visualizations.

## Future Enhancements:

-   More sophisticated UI components and user experience.
-   Visualizations for the knowledge graph (e.g., using libraries like `react-flow` or `vis-network`).
-   State management solutions (e.g., Zustand, Redux Toolkit) for more complex applications.
-   More comprehensive error handling and user feedback.
-   User authentication integration if the backend implements it.
-   More robust testing with Vitest/Jest.
