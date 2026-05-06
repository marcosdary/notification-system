from pydantic import BaseModel, field_serializer
from enum import Enum

from app.core.constants import StatusEmail

class ResponseSchema(BaseModel):
    id: str
    status: StatusEmail
    message: str 

    @field_serializer("status", mode="plain")
    def serialize_enuns(value: Enum) -> str:
        return value.value
    
