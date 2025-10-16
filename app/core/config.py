from pydantic_settings import BaseSettings
from pydantic import Field, computed_field
from pydantic.networks import PostgresDsn

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

    @computed_field
    @property
    def DATABASE_URL(self) -> PostgresDsn:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


    # Vector DB
    PINECONE_API_KEY: str = Field(..., env="PINECONE_API_KEY")
    PINECONE_ENVIRONMENT: str = Field(..., env="PINECONE_ENVIRONMENT")
    PINECONE_INDEX_NAME: str = "floatchat-profiles"

    # LLM
    GOOGLE_API_KEY: str = Field(..., env="GOOGLE_API_KEY")
    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"

settings = Settings()
