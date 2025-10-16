# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for geospatial libraries
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    pipx \
    && rm -rf /var/lib/apt/lists/*

# Install uv using pipx
RUN pipx install uv

# Ensure uv is in the PATH
ENV PATH="/root/.local/bin:${PATH}"
ENV UV_HTTP_TIMEOUT=300

# Copy the project files
COPY pyproject.toml README.md ./
COPY app ./app

# Install the CPU-only version of torch first
RUN uv pip install --system torch --index-url https://download.pytorch.org/whl/cpu


# Install the rest of the dependencies from pyproject.toml using uv
RUN uv pip install --system .

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]