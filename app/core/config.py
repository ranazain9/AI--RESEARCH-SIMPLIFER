from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os

class Settings(BaseSettings):
    # API Settings
    PROJECT_NAME: str = "AI Research Paper Simplifier"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # Security
    GROQ_API_KEY: str
    
    # Model Settings
    LLM_MODEL: str = "llama-3.3-70b-versatile"
    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"
    
    # File Storage
    UPLOAD_DIR: str = "temp_uploads"
    
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
