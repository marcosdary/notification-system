from sqlalchemy import Column, VARCHAR, Enum, TIMESTAMP, Text, func 
from uuid import uuid4

from api.models.base_model import BaseModel
from api.constants import SendType, Status

class EmailNotificationsModel(BaseModel):

    __tablename__ = "email_notification"

    idEmail = Column(VARCHAR(255), primary_key=True, default=lambda: str(uuid4()))
    recipientEmail = Column(VARCHAR(400), nullable=False)

    sendType = Column(Enum(SendType), nullable=False)
    status = Column(Enum(Status), nullable=False)
    providerResponse = Column(Text, default="No response")
    createdAt = Column(TIMESTAMP, server_default=func.current_timestamp())
    processedAt = Column(TIMESTAMP, server_default=func.current_timestamp())



    