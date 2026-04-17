from pydantic import (
    field_serializer, field_validator
)
from enum import Enum
from uuid import uuid4

from app.schemas.email_notification_schema.base import BaseEmailNotificationSchema
from app.constants import SendType, ExpirationTime
from app.exceptions import InvalidFieldsException

class CreateEmailNotificationSchema(BaseEmailNotificationSchema):

    idEmail: str | None = None
    recipientEmail: str
    sendType: SendType
    
    actionLink: str | None = None
    code: str | None = None
    token: str | None = None
    expiresAt: ExpirationTime | None = ExpirationTime.FIFTEEN_MINUTES

    @field_serializer("sendType", "expiresAt", mode="plain")
    def serialize_enum(self, value: Enum) -> str | int:
        return value.value if value else None
    
    @field_validator("recipientEmail", mode="before")
    @classmethod
    def validate_email(cls, value: str) -> str:
        if not value:
            raise InvalidFieldsException("E-mail não pode ser vazio.")
        return value
    
    

