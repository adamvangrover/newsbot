from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "NewsBot Nexus"
    VERSION: str = "2.0.0"
    API_V1_STR: str = "/api/v1"

    # External APIs
    FINNHUB_API_KEY: Optional[str] = None
    ALPHA_VANTAGE_API_KEY: Optional[str] = None

    # HuggingFace
    HF_TOKEN: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

settings = Settings()
