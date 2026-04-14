from pydantic import field_serializer
from enum import Enum
from datetime import datetime

from app.constants import StatusWebhook
from app.schemas.webhook_schema.base import BaseWebhookSchema

class CreateWebhookSchema(BaseWebhookSchema):
    idWebhook: str 
    status: StatusWebhook | None = StatusWebhook.PENDING
    response: str | None = None

    @field_serializer("status", mode="plain")
    def serialize_enum(self, value: Enum) -> str:
        return value.value