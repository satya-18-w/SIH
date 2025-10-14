# FloatChat Architecture

This document provides a detailed overview of the FloatChat system architecture, including the data flow, component interactions, and infrastructure.

## C4 Model Diagrams

We use the C4 model to describe the architecture at different levels of detail.

### Level 1: System Context Diagram

This diagram shows how the FloatChat system fits into its environment and interacts with users and external systems.

```mermaid
C4Context
  title System Context Diagram for FloatChat

  Person(user, "Oceanographer / Researcher", "A user who wants to explore ARGO data using natural language.")

  System_Ext(argo_data_system, "ARGO Data System (e.g., Ifremer FTP)", "Provides ARGO float data in NetCDF format.")
  System_Ext(llm_provider, "Large Language Model (e.g., OpenAI, Hugging Face)", "Provides embedding and generation models.")

  System(floatchat, "FloatChat", "Allows users to query and visualize ARGO oceanographic data via a web interface.")

  Rel(user, floatchat, "Uses")
  Rel(floatchat, argo_data_system, "Ingests data from")
  Rel(floatchat, llm_provider, "Uses API for embeddings and chat")

```

### Level 2: Container Diagram

This diagram zooms into the FloatChat system to show its major containers (applications, services, databases).

```mermaid
C4Container
  title Container Diagram for FloatChat

  Person(user, "User")

  System_Ext(argo_data_system, "ARGO Data System")
  System_Ext(llm_provider, "LLM API")

  System_Boundary(floatchat_system, "FloatChat System") {

    Container(frontend, "Frontend Web App", "Streamlit / React", "Provides the user interface for chat and data visualization.")
    Container(backend, "Backend API", "FastAPI, Python", "Handles user requests, orchestrates the RAG pipeline, and serves data.")

    ContainerDb(postgres, "Relational Database", "PostgreSQL + PostGIS", "Stores structured ARGO float metadata and profile data.")
    ContainerDb(vector_db, "Vector Database", "ChromaDB / FAISS", "Stores vector embeddings of profile summaries for fast retrieval.")
    ContainerDb(object_storage, "Object Storage", "S3 / GCS / MinIO", "Stores raw NetCDF files and processed Parquet files.")

    Container(etl_pipeline, "ETL Pipeline", "Python, xarray, pandas", "Ingests, processes, and vectorizes ARGO data.")
  }

  Rel(user, frontend, "Uses", "HTTPS")
  Rel(frontend, backend, "Makes API calls to", "REST API (JSON)")

  Rel(backend, llm_provider, "Generates SQL and answers using", "HTTPS/API")
  Rel(backend, vector_db, "Retrieves relevant profiles from")
  Rel(backend, postgres, "Executes SQL queries against")
  Rel(backend, object_storage, "Reads Parquet data from")

  Rel(etl_pipeline, argo_data_system, "Downloads NetCDF files from")
  Rel(etl_pipeline, object_storage, "Stores raw and processed files in")
  Rel(etl_pipeline, postgres, "Writes structured data to")
  Rel(etl_pipeline, vector_db, "Upserts embeddings to")
  Rel(etl_pipeline, llm_provider, "Generates embeddings using", "HTTPS/API")

```

## Data Flow and RAG Pipeline

This diagram illustrates the flow of data from ingestion to user query.

### 1. Data Ingestion Flow

```mermaid
graph TD
    A[ARGO NetCDF Files] --> B{ETL Pipeline};
    B --> C[Parse & Normalize];
    C --> D[Store Raw in Object Storage];
    C --> E{Structured Data};
    E --> F[Store Metadata in PostgreSQL/PostGIS];
    E --> G[Store Observations as Parquet in Object Storage];
    C --> H[Create Profile Summaries];
    H --> I{Embedding Model};
    I --> J[Generate Vector Embeddings];
    J --> K[Store in Vector DB];
```

### 2. RAG Query Flow

```mermaid
graph TD
    subgraph User Interface
        A[User Enters Natural Language Query]
    end

    subgraph Backend API
        B{Chat Endpoint}
        C{RAG Orchestrator}
        D{Retriever}
        E{LLM for SQL & Answer Generation}
        F{SQL Validator & Executor}
    end

    subgraph Data Stores
        G[Vector DB]
        H[PostgreSQL]
    end

    A --> B;
    B --> C;
    C --> D;
    D -- Query Embedding --> G;
    G -- Relevant Profile IDs --> D;
    D -- Retrieved Documents --> C;
    C -- Context + Query --> E;
    E -- Generated SQL --> F;
    F -- Validated SQL --> H;
    H -- Query Results --> F;
    F -- Table Data --> C;
    E -- Natural Language Answer & Plot Spec --> C;
    C -- Final Response --> B;
    B --> A;
```

## Infrastructure and Deployment

The application is designed to be deployed on the cloud using modern infrastructure practices.

*   **Containerization:** All services are containerized using Docker.
*   **Local Development:** A `docker-compose.yml` file is provided for easy local setup.
*   **Cloud Provisioning:** Terraform scripts are used to provision the necessary cloud resources (VPC, Kubernetes cluster, managed databases, object storage).
*   **Orchestration:** Kubernetes is used for container orchestration, managing deployments, services, and scaling.
*   **CI/CD:** GitHub Actions are used to automate the build, test, and deployment process.
