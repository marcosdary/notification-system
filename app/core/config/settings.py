from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    API_KEY_RESEND: str
    API_KEY: str
    SENDER: str
    WEBHOOK_SECRET: str 
    URL_WEBHOOK: str

    REDIS_URL: str

    POSTGRES_DB: str
    POSTGRES_DB_ASYNC: str
    
    SUPABASE_URL: str
    SUPABASE_KEY: str

    BUCKET_FILES_PUBLIC: str

    EXPIRES_IN_SIGNED_URL: int
    EXPIRES_IN_FILE: int

    
@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()

settings = get_settings()