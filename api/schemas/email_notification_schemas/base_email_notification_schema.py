from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator, field_serializer
from datetime import datetime
from api.constants import Status, SendType
from api.exceptions import InvalidFieldsException

class BaseEmailNotificationSchema(BaseModel):
    idEmail: str | None = None
    recipientEmail: str
    status: Status | None = Status.PENDING # Status da notificação
    providerResponse: str | None = None
    sendType: SendType
    createdAt: datetime = Field(default_factory=datetime.now)
    processedAt: datetime = Field(default_factory=datetime.now)

    model_config = ConfigDict(from_attributes=True)

    @field_validator("recipientEmail", mode="before")
    @classmethod
    def validate_email(cls, value: str) -> str:
        if not value:
            raise InvalidFieldsException("E-mail não pode ser vazio.")
        return value

    @field_serializer("sendType", "status", mode="plain")
    def serialize_enum(self, value: Enum) -> str:
        return value.value