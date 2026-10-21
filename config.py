from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    brewcreator_api_url: str = "https://api.brewcreator.com/v1"
    brewcreator_api_key: str = ""
    brewcreator_batch_id: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

@lru_cache
def get_settings() -> Settings:
    """Cacher konfigurationen, så .env kun læses fra disken én gang."""
    return Settings()

settings = get_settings()