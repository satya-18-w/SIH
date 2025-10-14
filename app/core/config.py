from pydantic_settings import BaseSettings
from pydantic import Field, PostgresDsn

class Settings(BaseSettings):
    PROJECT_NAME: str = "FloatChat"
    PROJECT_VERSION: str = "0.1.0"
    PROJECT_DESCRIPTION: str = "A RAG application for ARGO oceanographic data."

    # Database
    POSTGRES_USER: str = Field(..., env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(..., env="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field(..., env="POSTGRES_DB")
    POSTGRES_HOST: str = Field(..., env="POSTGRES_HOST")
    POSTGRES_PORT: int = Field(..., env="POSTGRES_PORT")
    DATABASE_URL: PostgresDsn = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

    # Vector DB
    CHROMA_HOST: str = Field(..., env="CHROMA_HOST")
    CHROMA_PORT: int = Field(..., env="CHROMA_PORT")
    VECTOR_DB_COLLECTION: str = "floatchat_profiles"

    # LLM
    GOOGLE_API_KEY: str = Field(..., env="GOOGLE_API_KEY")
    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"

settings = Settings()
