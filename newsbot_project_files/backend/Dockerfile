# Stage 1: Build stage (if needed for compilation or specific setups, otherwise can be simpler)
# For Python, often a single stage is fine unless there are complex build steps.

# Official Python runtime as a parent image
FROM python:3.9-slim-buster AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies (if any, e.g., for certain Python packages)
# RUN apt-get update && apt-get install -y --no-install-recommends some-package && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
# Using --no-cache-dir to reduce image size slightly
# Consider using a virtual environment inside Docker if preferred, though often not necessary for containerization.
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port (Uvicorn default is 8000)
EXPOSE 8000

# Command to run the application using Uvicorn
# Use 0.0.0.0 to bind to all interfaces, making it accessible from outside the container
# --reload is for development; remove or disable for production builds
# Add --workers for production if needed, e.g., --workers 4
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
# For development with reload:
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
