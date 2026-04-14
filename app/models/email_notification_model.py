from sqlalchemy import Column, VARCHAR, INTEGER, Enum, Text
from uuid import uuid4

from app.models.base_model import BaseModel
from app.constants import SendType, StatusEmail

class EmailNotificationsModel(BaseModel):

    __tablename__ = "email_notification"

    idEmail = Column(VARCHAR(255), primary_key=True, default=lambda: str(uuid4()))
    recipientEmail = Column(VARCHAR(400), nullable=False)

    actionLink = Column(VARCHAR(500), nullable=False)
    code = Column(VARCHAR(10), nullable=False)
    token = Column(VARCHAR(400), nullable=False)
    expiresAt = Column(INTEGER, nullable=False)

    sendType = Column(Enum(SendType, name="send_type"), nullable=False)
    status = Column(Enum(StatusEmail, name="status_email"), nullable=False, default=StatusEmail.PENDING)
    providerResponse = Column(Text, default="No response")


    