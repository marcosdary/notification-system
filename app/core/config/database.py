from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.settings import settings


engine_sync = create_engine(settings.DATABASE_URL_LOCALHOST)

SessionLocalSync = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine_sync
)

engine_async = create_async_engine(
    settings.DATABASE_URL_LOCALHOST_ASYNC,
    pool_size=10,           # Mantém até 10 conexões abertas
    max_overflow=20,        # Permite até 20 conexões extras em picos
    pool_recycle=3600,      # Recicla conexões a cada hora
    pool_pre_ping=True      # Verifica se a conexão está viva antes de usar (evita erros 500)
)

SessionLocalAsync = sessionmaker(
    bind=engine_async,
    class_=AsyncSession,
    expire_on_commit=False
)