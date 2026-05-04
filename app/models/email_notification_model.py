from sqlalchemy import Enum
from sqlalchemy.orm import mapped_column, Mapped
from uuid import uuid4
from datetime import datetime

from app.models.base_model import BaseModel
from app.core.constants import SendType, StatusEmail

class EmailNotificationsModel(BaseModel):

    __tablename__ = "email_notification"

    idEmail: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    recipientEmail: Mapped[str] = mapped_column(nullable=False)

    actionLink: Mapped[str] = mapped_column(nullable=False)
    code: Mapped[str] = mapped_column(nullable=False)
    token: Mapped[str] = mapped_column(nullable=False)
    expiresAt: Mapped[int] = mapped_column(nullable=False)

    sendType: Mapped[SendType] = mapped_column(Enum(SendType, name="send_type"), nullable=False)
    status: Mapped[StatusEmail] = mapped_column(Enum(StatusEmail, name="status_email"), nullable=False, default=StatusEmail.PENDING)
    providerResponse: Mapped[str] = mapped_column(default="No response")


    