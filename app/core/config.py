from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    app_name: str = "Advanced AI Medical Intelligence Platform"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = True

    api_host: str = "0.0.0.0"
    api_port: int = 8000

    database_url: str = "sqlite:///./medical_intelligence.db"

    model_path: str = "models/checkpoints/best_efficientnet_b0.pth"

    groq_api_key: str = ""
    groq_model: str = "llama-3.1-8b-instant"

    max_image_size_mb: int = 10

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()
