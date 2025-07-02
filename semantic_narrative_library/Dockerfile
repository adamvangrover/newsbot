# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app/semantic_narrative_library

# Install system dependencies (if any were needed, e.g., for certain DB drivers)
# RUN apt-get update && apt-get install -y --no-install-recommends some-package && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
# First, copy only the requirements file to leverage Docker cache
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the semantic_narrative_library application code into the container
# This includes the main library and all its submodules (api, core_models, data, etc.)
COPY . .

# Expose port 8000 (or whatever port your FastAPI app runs on)
EXPOSE 8000

# Command to run the Uvicorn server for the FastAPI application
# This assumes your FastAPI 'app' instance is in 'semantic_narrative_library.api.main'
# The host 0.0.0.0 makes it accessible from outside the container.
CMD ["uvicorn", "semantic_narrative_library.api.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Note on running this Dockerfile:
# 1. Build the image from the repository root:
#    docker build -t semantic-narrative-api -f semantic_narrative_library/Dockerfile .
#    (The trailing '.' indicates the build context is the repository root, so Docker can find semantic_narrative_library/)
#
# 2. Run the container:
#    docker run -p 8000:8000 semantic-narrative-api
#
# The API should then be accessible at http://localhost:8000 on the host machine.
# The sample_knowledge_graph.json will be loaded from within the container's file system as part of the copied library.
#
# If your semantic_narrative_library was intended to be a standalone package installed via pip,
# the Dockerfile would look different (e.g. COPY setup.py, RUN pip install .).
# For now, it's structured as copying the source code directly.
