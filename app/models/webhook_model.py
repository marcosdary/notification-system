from sqlalchemy import Column, VARCHAR, Enum, Text
from uuid import uuid4

from app.models.base_model import BaseModel
from app.constants import StatusWebhook

class WebhookModel(BaseModel):

    __tablename__ = "webhook"

    idWebhook = Column(VARCHAR(255), primary_key=True, default=lambda: str(uuid4()))
    status = Column(Enum(StatusWebhook, name="status_webhook"), nullable=False)
    response = Column(Text, default="No response")




    