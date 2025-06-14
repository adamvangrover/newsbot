# NewsBot Setup and Deployment Guide

## 1. Development Environment Setup

### 1.1. Prerequisites

*   **Git:** For cloning the repository.
*   **Python:** Version 3.9 or higher (as specified in ).
*   **Node.js:** Version 18 or higher (as specified in ), with npm or yarn.
*   **Docker & Docker Compose:** For running the application in containers (recommended).
*   **API Keys:**
    *   Finnhub.io API Key
    *   Alpha Vantage API Key

### 1.2. Local Setup (Without Docker - for individual component development)

This approach is suitable if you want to run the frontend and backend servers directly on your host machine.

**Backend:**

1.  Navigate to the  directory.
2.  Create a Python virtual environment:
    ```bash
    # Create a Python virtual environment (e.g., named 'myenv_directory')
    # (replace <name_of_module_for_venv_creation> with 'venv')
    python -m <name_of_module_for_venv_creation> myenv_directory
    source myenv_directory/bin/activate  # On Windows: myenv_directory\Scripts\activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    *Note: This will download Hugging Face models on first run of AI features, which can take time.*
4.  Create a  file in the  directory by copying :
    ```bash
    cp .env.example .env
    ```
5.  Edit  and add your actual API keys:
    ```
    FINNHUB_API_KEY="your_actual_finnhub_key"
    ALPHA_VANTAGE_API_KEY="your_actual_alphavantage_key"
    ```
6.  Run the backend server:
    ```bash
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```
    The API will be accessible at .

**Frontend:**

1.  Navigate to the  directory.
2.  Install dependencies:
    ```bash
    npm install  # or yarn install
    ```
3.  Create a  file in the  directory by copying :
    ```bash
    cp .env.example .env
    ```
4.  Verify  in . For local backend running on port 8000, it should be:
    ```
    VITE_API_BASE_URL="http://localhost:8000/api/v1"
    ```
5.  Run the frontend development server (Vite):
    ```bash
    npm run dev # or yarn dev
    ```
    The frontend will be accessible at  (or another port if specified by Vite).

### 1.3. Local Setup (With Docker Compose - Recommended)

This is the recommended way to run the full application locally, as it mirrors a production-like containerized environment.

1.  Ensure Docker and Docker Compose are installed and running.
2.  Navigate to the root  directory.
3.  **Backend Environment:** Create a  file by copying  and fill in your API keys as described in section 1.2.
    ```bash
    cp backend/.env.example backend/.env
    # Then edit backend/.env with your keys
    ```
4.  **Frontend Environment (Optional for Docker Compose):** The  for the frontend when running in Docker Compose needs to point to the backend service name.
    *   **Option A (Build-time argument - More Robust):**
        Modify  under  to pass the correct URL:
        ```yaml
        services:
          frontend:
            build:
              context: ./frontend
              dockerfile: Dockerfile
              args: # Add this
                - VITE_API_BASE_URL=http://backend:8000/api/v1
        ```
        And modify  to accept this argument:
        ```dockerfile
        # Stage 1: Build the React application
        FROM node:18-alpine AS build
        ARG VITE_API_BASE_URL # Declare the argument
        ENV VITE_API_BASE_URL= # Set it as an environment variable for Vite
        WORKDIR /app
        # ... rest of the build stage ...
        RUN npm run build # Vite will pick up VITE_API_BASE_URL
        ```
        Ensure  uses .
    *   **Option B (Modify .env for local Docker build):** If you build images locally before , ensure  has . This is less flexible if the service name changes. The current  does not automatically pass a custom  file to the frontend build context.

5.  Build and run the application using Docker Compose:
    ```bash
    docker-compose up --build
    ```
    *   : Forces Docker to rebuild images if Dockerfiles or their contexts have changed.
    *   The first build might take some time, especially for the backend due to Python package installations and model downloads (if not cached by Docker layers).
6.  Access:
    *   Frontend:
    *   Backend API:  (e.g., health check at )

7.  To stop the application:
    ```bash
    docker-compose down
    ```

## 2. Running Linters

**Backend (flake8, black):**

1.  Navigate to .
2.  Ensure virtual environment is active and dev dependencies installed (or install them: Defaulting to user installation because normal site-packages is not writeable
Collecting flake8
  Downloading flake8-7.2.0-py2.py3-none-any.whl.metadata (3.8 kB)
Collecting black
  Downloading black-25.1.0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64.whl.metadata (81 kB)
Collecting mccabe<0.8.0,>=0.7.0 (from flake8)
  Downloading mccabe-0.7.0-py2.py3-none-any.whl.metadata (5.0 kB)
Collecting pycodestyle<2.14.0,>=2.13.0 (from flake8)
  Downloading pycodestyle-2.13.0-py2.py3-none-any.whl.metadata (4.5 kB)
Collecting pyflakes<3.4.0,>=3.3.0 (from flake8)
  Downloading pyflakes-3.3.2-py2.py3-none-any.whl.metadata (3.5 kB)
Requirement already satisfied: click>=8.0.0 in /usr/local/lib/python3.10/dist-packages (from black) (8.1.8)
Collecting mypy-extensions>=0.4.3 (from black)
  Downloading mypy_extensions-1.1.0-py3-none-any.whl.metadata (1.1 kB)
Requirement already satisfied: packaging>=22.0 in /usr/local/lib/python3.10/dist-packages (from black) (25.0)
Collecting pathspec>=0.9.0 (from black)
  Downloading pathspec-0.12.1-py3-none-any.whl.metadata (21 kB)
Requirement already satisfied: platformdirs>=2 in /usr/local/lib/python3.10/dist-packages (from black) (4.3.7)
Requirement already satisfied: tomli>=1.1.0 in /usr/local/lib/python3.10/dist-packages (from black) (2.2.1)
Requirement already satisfied: typing-extensions>=4.0.1 in /usr/local/lib/python3.10/dist-packages (from black) (4.13.2)
Downloading flake8-7.2.0-py2.py3-none-any.whl (57 kB)
Downloading mccabe-0.7.0-py2.py3-none-any.whl (7.3 kB)
Downloading pycodestyle-2.13.0-py2.py3-none-any.whl (31 kB)
Downloading pyflakes-3.3.2-py2.py3-none-any.whl (63 kB)
Downloading black-25.1.0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64.whl (1.8 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.8/1.8 MB 33.2 MB/s eta 0:00:00
Downloading mypy_extensions-1.1.0-py3-none-any.whl (5.0 kB)
Downloading pathspec-0.12.1-py3-none-any.whl (31 kB)
Installing collected packages: pyflakes, pycodestyle, pathspec, mypy-extensions, mccabe, flake8, black

Successfully installed black-25.1.0 flake8-7.2.0 mccabe-0.7.0 mypy-extensions-1.1.0 pathspec-0.12.1 pycodestyle-2.13.0 pyflakes-3.3.2).
3.  Run linters:
    ```bash
    flake8 .
    black . --check # Or black . to reformat
    ```

**Frontend (ESLint):**

1.  Navigate to .
2.  Ensure Node modules are installed ().
3.  Run linter (script should be in ):
    ```bash
    npm run lint
    ```

The CI workflow () also runs these linters.

## 3. Deployment (Conceptual for MVP)

This MVP is designed to be deployed using Docker containers.

1.  **Build Docker Images:**
    *   Backend:
    *   Frontend:
        *   Replace  with the actual URL where your backend will be accessible in production.

2.  **Push Images to a Registry:** (e.g., Docker Hub, AWS ECR, Google GCR, Azure ACR)
    ```bash
    docker tag newsbot-backend:latest your-registry/newsbot-backend:latest
    docker push your-registry/newsbot-backend:latest
    # Repeat for frontend
    ```

3.  **Deployment Platform:** Choose a platform that supports Docker containers. Examples:
    *   **Cloud Providers:**
        *   AWS: ECS, EKS, App Runner
        *   Google Cloud: Cloud Run, GKE, App Engine Flex
        *   Azure: App Service, AKS, Container Instances
    *   **Virtual Private Server (VPS):** Install Docker and Docker Compose, then adapt  for production (e.g., remove development volumes, use production CMDs in Dockerfiles, manage .env files securely).
    *   **Kubernetes:** For more complex orchestration.

4.  **Configuration in Production:**
    *   **API Keys:** Provide  and  as environment variables to the backend container securely (e.g., using secrets management tools of your cloud provider).
    *   ** (Frontend):** This needs to be correctly set at build time for the frontend image to point to the deployed backend's public URL.
    *   **Database/Caching:** For a production app, you would likely add a persistent database and a caching layer (e.g., Redis), which would also be configured via environment variables.
    *   **HTTPS:** Configure HTTPS, typically at the load balancer or reverse proxy level.

5.  **Serving:**
    *   The backend container runs Uvicorn (without ).
    *   The frontend container runs Nginx to serve static files.
    *   A load balancer or reverse proxy would route traffic to the appropriate service (e.g.,  to backend, everything else to frontend).

This setup guide provides a starting point. Production deployments require careful consideration of security, scalability, monitoring, and logging.
