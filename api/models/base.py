from sqlalchemy.orm import DeclarativeBase

class BaseModel(DeclarativeBase):
    """Classe base abstrata para modelos SQLAlchemy.

    Fornece campos de auditoria comuns a todas as tabelas herdando desta
    classe, como data de criação e data de atualização.

    Attributes:
    """

    __abstract__ = True
