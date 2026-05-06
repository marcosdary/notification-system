from pydantic import BaseModel, ConfigDict, field_serializer
from typing import List
from enum import Enum

from app.core.constants import Template
from app.schemas.email_schema.variables_schema import VariablesSchema
from app.schemas.email_schema.recipient_schema import RecipientSchema
from app.schemas.email_schema.attachment_schema import AttachmentSchema

class EmailSchema(BaseModel):
    to: List[RecipientSchema]
    subject: str
    template: Template
    variables: VariablesSchema
    attachments: List[AttachmentSchema]

    model_config = ConfigDict(from_attributes=True)


    @field_serializer("template", mode="plain")
    def serialize_enuns(value: Enum) -> str:
        return value.value
    
