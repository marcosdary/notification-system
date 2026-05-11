from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Enum
from uuid import uuid4
from datetime import datetime, timedelta

from app.models.base_model import BaseModel
from app.core.constants import StatusFile
from app.core.config import settings

class FileModel(BaseModel):
    __tablename__ = "file"

    path: Mapped[str] = mapped_column(default=lambda: str(uuid4()), primary_key=True)
    status: Mapped[StatusFile] = mapped_column(Enum(StatusFile, name="status_file"), default=StatusFile.not_used.value)
    expires_at: Mapped[datetime] = mapped_column(default=datetime.now() + timedelta(seconds=settings.EXPIRES_IN_SIGNED_URL))
    

    