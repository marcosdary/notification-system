from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, DateTime
from datetime import datetime

class BaseModel(DeclarativeBase):
    """Classe base abstrata para modelos SQLAlchemy.

    Fornece campos de auditoria comuns a todas as tabelas herdando desta
    classe, como data de criação e data de atualização.

    Attributes:
    """

    __abstract__ = True

    createdAt = Column(DateTime, default=datetime.now)
    processedAt = Column(DateTime, default=datetime.now, onupdate=datetime.now)

