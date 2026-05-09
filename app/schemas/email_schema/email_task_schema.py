from pydantic import BaseModel, field_serializer
from enum import Enum

from app.core.constants import Status

class EmailTaskSchema(BaseModel):
    id_email: str
    status: Status
    message: str 

    @field_serializer("status", mode="plain")
    def serialize_enuns(value: Enum) -> str:
        return value.value
    
    