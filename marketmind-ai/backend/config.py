"""
MarketMind AI – Central configuration (reads .env)
"""
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List
import os


class Settings(BaseSettings):
    # IBM watsonx.ai
    watsonx_api_key: str = Field(default="", env="WATSONX_API_KEY")
    watsonx_project_id: str = Field(default="", env="WATSONX_PROJECT_ID")
    watsonx_url: str = Field(default="https://us-south.ml.cloud.ibm.com", env="WATSONX_URL")
    granite_model_id: str = Field(default="ibm/granite-13b-instruct-v2", env="GRANITE_MODEL_ID")

    # LangFlow
    langflow_host: str = Field(default="127.0.0.1", env="LANGFLOW_HOST")
    langflow_port: int = Field(default=7860, env="LANGFLOW_PORT")
    langflow_api_key: str = Field(default="", env="LANGFLOW_API_KEY")

    # Backend
    backend_host: str = Field(default="0.0.0.0", env="BACKEND_HOST")
    backend_port: int = Field(default=8000, env="BACKEND_PORT")
    debug: bool = Field(default=True, env="DEBUG")

    # RAG / Vector Store
    vector_store: str = Field(default="chromadb", env="VECTOR_STORE")
    chroma_persist_dir: str = Field(default="./chroma_db", env="CHROMA_PERSIST_DIR")
    embedding_model: str = Field(default="all-MiniLM-L6-v2", env="EMBEDDING_MODEL")

    # Demo mode
    demo_mode: bool = Field(default=True, env="DEMO_MODE")
    demo_market: str = Field(default="indian_ev", env="DEMO_MARKET")

    # File upload
    max_upload_size_mb: int = Field(default=50, env="MAX_UPLOAD_SIZE_MB")
    allowed_extensions: str = Field(default="pdf,csv,txt,docx", env="ALLOWED_EXTENSIONS")

    # CORS
    allowed_origins: str = Field(
        default="http://localhost:3000,http://127.0.0.1:5500,http://localhost:5500",
        env="ALLOWED_ORIGINS",
    )

    @property
    def allowed_origins_list(self) -> List[str]:
        return [o.strip() for o in self.allowed_origins.split(",")]

    @property
    def allowed_extensions_list(self) -> List[str]:
        return [e.strip().lower() for e in self.allowed_extensions.split(",")]

    @property
    def langflow_base_url(self) -> str:
        return f"http://{self.langflow_host}:{self.langflow_port}"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
