from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from datetime import datetime

class BaseModel(DeclarativeBase):
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    