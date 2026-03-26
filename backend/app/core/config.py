from functools import lru_cache
from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Job Application Copilot API"
    app_env: str = "development"
    app_debug: bool = True
    api_v1_prefix: str = "/api/v1"
    database_url: str = "sqlite:///./job_applications.db"
    allowed_origins: List[str] = ["http://localhost:4200"]
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_allowed_origins(cls, value):
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()


@field_validator("allowed_origins", mode="before")
@classmethod
def parse_allowed_origins(cls, value):
    if isinstance(value, str):
        # handle JSON OR comma-separated
        if value.startswith("["):
            import json
            return json.loads(value)
        return [origin.strip() for origin in value.split(",") if origin.strip()]
    return value