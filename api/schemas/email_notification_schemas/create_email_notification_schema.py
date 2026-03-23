from pydantic import (
    model_validator, field_serializer
)
from enum import Enum

from api.schemas.email_notification_schemas.base_email_notification_schema import BaseEmailNotificationSchema
from api.constants import Status, SendType, ExpirationAt
from api.exceptions import InvalidFieldsException

class CreateEmailNotificationSchema(BaseEmailNotificationSchema):
    
    actionLink: str | None = None
    code: str | None = None
    sendType: SendType
    expiresAt: ExpirationAt | None = ExpirationAt.FIFTEEN_MINUTES

    @field_serializer("sendType", "status", "expiresAt", mode="plain")
    def serialize_enum(self, value: Enum) -> str | int:
        return value.value if value else None
    
    



