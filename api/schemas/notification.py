from enum import Enum
from json import loads

from pydantic import BaseModel, field_serializer, field_validator, ConfigDict
from datetime import datetime
from uuid import uuid4

from api.constants import Status, TypeSend, Templates

class NotificationSchema(BaseModel):
    idSend: str = str(uuid4())
    typeSend: TypeSend = TypeSend.REGISTER
    templateName: Templates = Templates.REGISTER # Nome do template
    info: dict # Informações para incluir no template
    status: Status = Status.PENDING # Status da notificação
    responseServer: dict | None = None
    createdAt: datetime = datetime.now() # Data criação
    endIn: datetime = datetime.now()
    
    model_config = ConfigDict(from_attributes=True)

    @field_validator("info", "responseServer", mode="before")
    def validate_fields(cls, value) -> dict:
        if isinstance(value, str):
            return loads(value) 
        return value

    @field_serializer("templateName", "typeSend", "status", mode="plain")
    def serielize_enum(self, type_enum: Enum) -> str:
        return type_enum.value
    
    @field_serializer("createdAt", "endIn", mode="plain")
    def serialize_date(self, value: datetime) -> str:
        return value.isoformat()
    
    
    




