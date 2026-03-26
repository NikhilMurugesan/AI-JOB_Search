from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Job Search Copilot API"
    env: str = "dev"
    api_v1_prefix: str = "/api/v1"
    database_url: str = "sqlite:///./aijobsearch.db"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
