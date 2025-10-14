# FloatChat - Retrieval-Augmented Generation for ARGO Oceanographic Data

FloatChat is a production-grade, scalable Retrieval-Augmented Generation (RAG) application for exploring and visualizing ARGO oceanographic data. It allows users to ask natural language questions about ARGO float data and receive answers in the form of text, tables, and interactive visualizations.

![Architecture Diagram](architecture.md)

## Table of Contents

- [FloatChat - Retrieval-Augmented Generation for ARGO Oceanographic Data](#floatchat---retrieval-augmented-generation-for-argo-oceanographic-data)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Architecture Overview](#architecture-overview)
  - [Tech Stack](#tech-stack)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Quickstart with Docker Compose](#quickstart-with-docker-compose)
    - [Accessing the Application](#accessing-the-application)
  - [Data Ingestion](#data-ingestion)
  - [Deployment](#deployment)
    - [Terraform (AWS)](#terraform-aws)
    - [Kubernetes (Helm)](#kubernetes-helm)
  - [CI/CD](#cicd)
  - [Development](#development)
    - [Makefile Commands](#makefile-commands)
  - [Testing](#testing)
  - [Observability](#observability)
  - [Security](#security)
  - [Cost Considerations](#cost-considerations)
  - [Future Work](#future-work)

## Features

*   **Natural Language Queries:** Ask questions about ARGO data in plain English.
*   **RAG Pipeline:** Utilizes a robust RAG pipeline with vector search and a powerful LLM for generating accurate answers.
*   **SQL Generation:** Automatically generates safe, read-only SQL queries to fetch data from a relational database.
*   **Interactive Visualizations:** Generates interactive plots and maps using Plotly and Leaflet.
*   **Geospatial Capabilities:** Supports geospatial queries and visualizations of float trajectories.
*   **Scalable Architecture:** Built on a microservices architecture using Docker and Kubernetes for scalability.
*   **Infrastructure as Code:** Uses Terraform to provision cloud infrastructure.
*   **CI/CD:** Automated build, test, and deployment pipeline using GitHub Actions.

## Architecture Overview

The application is composed of the following key components:

*   **Frontend:** A Streamlit web application providing the user interface for chat and visualizations.
*   **Backend:** A FastAPI application that exposes a REST API for handling chat requests, executing queries, and serving data.
*   **RAG Pipeline:** The core of the application, responsible for retrieving relevant information and generating responses.
*   **Vector Database:** ChromaDB (by default) for storing and searching vector embeddings of ARGO data.
*   **Relational Database:** PostgreSQL with PostGIS for storing structured ARGO data and performing geospatial queries.
*   **ETL Pipeline:** A set of scripts for ingesting NetCDF files, processing them, and loading them into the databases.
*   **Object Storage:** S3 or GCS for storing raw and processed data files (Parquet).

For a detailed diagram, see [architecture.md](architecture.md).

## Tech Stack

*   **Data Processing:** Python, xarray, netCDF4, pandas, pyarrow, geopandas
*   **Relational DB:** PostgreSQL + PostGIS
*   **Vector DB:** ChromaDB / FAISS (swappable adapter)
*   **Embeddings:** sentence-transformers
*   **RAG & LLM:** OpenAI/GPT or self-hosted models
*   **Backend:** FastAPI
*   **Frontend:** Streamlit (for PoC)
*   **Serving:** Docker, Docker Compose, Kubernetes
*   **CI/CD:** GitHub Actions
*   **Infra-as-code:** Terraform
*   **Monitoring:** Prometheus + Grafana (planned)
*   **Testing:** pytest

## Getting Started

### Prerequisites

*   Docker and Docker Compose
*   Git
*   An environment file with your credentials (see `.env.example`)

### Quickstart with Docker Compose

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/floatchat.git
    cd floatchat
    ```

2.  **Set up your environment:**
    Copy the example environment file and fill in your details (e.g., OpenAI API key).
    ```bash
    cp .env.example .env
    ```

3.  **Build and run the application:**
    This single command will build the Docker images, start all the services (backend, frontend, databases), and run the initial data ingestion.
    ```bash
    make up
    ```

### Accessing the Application

*   **Frontend (Streamlit):** [http://localhost:8501](http://localhost:8501)
*   **Backend API Docs (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)

## Data Ingestion

The initial data ingestion is run automatically when you first run `make up`. The ETL pipeline fetches the latest ARGO data from the ArgoVis API.

To run ingestion manually:

```bash
make ingest
```

The ETL pipeline is idempotent and will skip profiles that have already been processed.

## Deployment

### Terraform (AWS)

The Terraform scripts in the `terraform/` directory can be used to provision the necessary infrastructure on AWS.

1.  **Navigate to the terraform directory:**
    ```bash
    cd terraform/aws
    ```

2.  **Initialize Terraform:**
    ```bash
    terraform init
    ```

3.  **Plan the deployment (dry-run):**
    ```bash
    terraform plan
    ```

4.  **Apply the changes:**
    ```bash
    terraform apply
    ```

### Kubernetes (Helm)

Helm charts for deploying the application to a Kubernetes cluster are located in the `k8s/` directory.

## CI/CD

The project includes a GitHub Actions workflow in `.github/workflows/ci.yml` that runs on every push and pull request. The workflow performs the following actions:

*   Lints the code with `flake8` and `black`.
*   Runs unit tests with `pytest`.
*   Builds Docker images for the backend and frontend.

## Development

### Makefile Commands

A `Makefile` is provided for common development tasks:

*   `make build`: Build the Docker images.
*   `make up`: Start the application using Docker Compose.
*   `make down`: Stop the application.
*   `make test`: Run the test suite.
*   `make lint`: Lint the codebase.
*   `make ingest`: Run the data ingestion process.

## Testing

The test suite is located in the `tests/` directory and uses `pytest`. To run the tests:

```bash
make test
```

## Observability

*   **Logging:** All services use structured JSON logging.
*   **Metrics:** The backend exposes Prometheus metrics at `/metrics`.
*   **Tracing:** OpenTelemetry is integrated for distributed tracing.

## Security

*   **Secrets Management:** Credentials are managed via environment variables and a `.env` file, with support for cloud secret managers.
*   **SQL Injection:** The RAG pipeline uses a SQL validator to prevent SQL injection attacks. All generated queries are read-only.
*   **Authentication:** The API is secured with API keys.

## Cost Considerations

*   **Cloud vs. Self-Hosted LLM:** The application can be configured to use a cloud-hosted LLM (e.g., OpenAI) or a self-hosted model. Self-hosting requires a GPU instance and can be more expensive in terms of infrastructure but avoids per-token API costs.
*   **Instance Sizing:** The `terraform/` scripts use cost-effective instance types by default. Adjust these based on your performance and budget requirements.

## Future Work

*   Full-fledged React/Next.js frontend.
*   Support for more vector databases.
*   Advanced re-ranking models in the RAG pipeline.
*   Real-time data ingestion pipeline.
*   Comprehensive Grafana dashboards for monitoring.
