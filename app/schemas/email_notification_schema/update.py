from pydantic import field_serializer, Field
from datetime import datetime
from enum import Enum

from app.constants import StatusEmail
from app.schemas.webhook_schema.base import BaseWebhookSchema

class UpdateEmailNotificationSchema(BaseWebhookSchema):
    idEmail: str
    status: StatusEmail
    providerResponse: str | None = None
    processedAt: datetime | None = Field(default_factory=datetime.now)

    @field_serializer("status", mode="plain")
    def serialize_enum(self, value: Enum) -> str:
        return value.value