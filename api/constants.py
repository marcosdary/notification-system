from enum import Enum
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from redis import Redis
from pathlib import Path
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações da aplicação carregadas a partir do arquivo .env.

    Esta classe herda de `BaseSettings` do Pydantic, garantindo que todas as
    variáveis de ambiente obrigatórias sejam carregadas corretamente.

    Attributes:
        REDIS_URL (str): URL de conexão com o Redis.
        SUPER_ADMIN_KEY (str): Chave para super administradores.
        SESSION_KEY (str): Chave utilizada para sessões.
        KEY_ADMIN (str): Chave de acesso administrativo.
        API_KEY_RESEND (str): Chave para reenvio de API.
        SENDER (str): E-mail ou remetente padrão.
        CREATE_API_KEY (str): Chave para criação de novas APIs.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    REDIS_URL: str
    API_KEY_RESEND: str
    TOKEN: str
    SENDER: str
    DATABASE_URL: str

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Retorna uma instância de `Settings` com cache.

    Utiliza LRU cache para garantir que a configuração seja carregada
    apenas uma vez, evitando múltiplas leituras do arquivo .env.

    Returns:
        Settings: Instância única das configurações da aplicação.
    """
    return Settings()


settings = get_settings()


# Configuração do Redis
redisClient = Redis.from_url(settings.REDIS_URL, decode_responses=True)

# Configurações de banco de dados
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session = SessionLocal

# Caminho do Templates
TEMPLATES_DIR = Path(__file__).parent / "templates"

class ExpirationApiKey(Enum):
    """Enumeração de períodos de expiração para chaves de API."""

    ONE_HOUR = 60 * 60
    ONE_DAY = 1 * 24 * 60 * 60
    TWO_DAYS = 2 * 24 * 60 * 60
    SEVEN_DAYS = 7 * 24 * 60 * 60
    THIRTY_DAYS = 30 * 24 * 60 * 60
    NINETY_DAYS = 90 * 24 * 60 * 60
    ONE_YEAR = 365 * 24 * 60 * 60


class ExpirationTimes(Enum):
    """Enumeração de tempos de expiração para sessões e tokens."""

    SESSION_EXPIRATION = 10_800  # 3 horas
    TWO_FA_EXPIRATION = 600       # 10 minutos
    PASSWORD_RESET_EXPIRATION = 900  # 15 minutos


class RolesRouters(Enum):
    """Enumeração de rotas acessíveis por cada papel de usuário."""

    ADMIN = (
        "listUsers",
        "getAllPosts",
    )

    SUPER_ADMIN = (
        "listUsers",
        "createAdmin",
        "getAllPosts",
        "createApiKey"
    )


class RoutersProtects(Enum):
    """Enumeração de rotas protegidas."""

    ROUTERS = (
        "listUsers",
        "createAdmin",
        "getAllPosts",
        "createApiKey"
    )


class Roles(Enum):
    """Enumeração de papéis de usuário."""

    USER = "USER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"

class TypeSend(Enum):
    REGISTER = "REGISTER"
    PASSWORD_CHANGE = "PASSWORD_CHANGE"
    TWO_FACTOR_AUTH = "TWO_FACTOR_AUTH"
    PASSWORD_RESET = "PASSWORD_RESET"

class Status(Enum):
    PENDING = "PENDING"
    DONE = "DONE"
    ERROR = "ERROR"
    REJECTED = "REJECTED"

class Templates(Enum):
    PASSWORD_CHANGE = "password_change.html"
    REGISTER = "register.html"
    PASSWORD_RESET = "password_reset.html"
    TWO_F_AUTH = "two_f_auth.html"