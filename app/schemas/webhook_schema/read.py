from pydantic import field_serializer
from datetime import datetime
from enum import Enum

from app.constants import StatusWebhook
from app.schemas.webhook_schema.base import BaseWebhookSchema

class ReadWebhookSchema(BaseWebhookSchema):
    idWebhook: str
    status: StatusWebhook
    response: str | None = None
    createdAt: datetime 
    processedAt: datetime 

    @field_serializer("status", mode="plain")
    def serialize_enum(self, value: Enum) -> str:
        return value.value