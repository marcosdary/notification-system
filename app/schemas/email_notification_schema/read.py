from datetime import datetime
from enum import Enum
from pydantic import field_serializer


from app.schemas.email_notification_schema.base import BaseEmailNotificationSchema
from app.constants import StatusEmail, SendType

class ReadEmailNotificationSchema(BaseEmailNotificationSchema):
    idEmail: str | None = None
    recipientEmail: str
    status: StatusEmail | None = StatusEmail.PENDING # Status da notificação
    providerResponse: str | None = None

    actionLink: str | None = None
    code: str | None = None
    token: str | None = None
    expiresAt: int | None = None

    sendType: SendType
    createdAt: datetime | None = None
    processedAt: datetime | None = None


    @field_serializer("sendType", "status", mode="plain")
    def serialize_enum(self, value: Enum) -> str:
        return value.value 