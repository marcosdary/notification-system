from sqlalchemy.orm import mapped_column, Mapped
from datetime import datetime
from uuid import uuid4

from app.models.base_model import BaseModel
from app.core.constants import Status

class EmailModel(BaseModel):
    __tablename__ = "email"

    id_email: Mapped[str] = mapped_column(default=lambda: str(uuid4()), primary_key=True)
    status: Mapped[Status] = mapped_column(default=Status.sent.value)
    message: Mapped[str] = mapped_column(default="Sem resposta")

    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
    

    