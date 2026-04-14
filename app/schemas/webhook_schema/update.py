from pydantic import field_serializer, Field
from datetime import datetime
from enum import Enum

from app.constants import StatusWebhook
from app.schemas.webhook_schema.base import BaseWebhookSchema

class UpdateWebhookSchema(BaseWebhookSchema):
    idWebhook: str
    status: StatusWebhook
    response: str | None = None
    processedAt: datetime | None = Field(default_factory=datetime.now)

    @field_serializer("status", mode="plain")
    def serialize_enum(self, value: Enum) -> str:
        return value.value