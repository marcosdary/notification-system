from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    REDIS_URL: str
    API_KEY_RESEND: str
    API_KEY: str
    SENDER: str
    DATABASE_URL: str
    WEBHOOK_SECRET: str 
    URL_WEBHOOK: str

    REDIS_URL_LOCALHOST_ASYNC: str
    DATABASE_URL_LOCALHOST: str
    DATABASE_URL_LOCALHOST_ASYNC: str


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()

settings = get_settings()