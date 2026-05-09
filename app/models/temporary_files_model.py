from sqlalchemy.orm import mapped_column, Mapped
from uuid import uuid4
from datetime import datetime

from app.models.base_model import BaseModel

class TemporaryFilesModel(BaseModel):
    __tablename__ = "temporary_files"

    id_file: Mapped[str] = mapped_column(default=lambda: str(uuid4()), primary_key=True)
    expires_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
    

    