from strawberry.experimental.pydantic import input as pydantic_input

from app.schemas.email_schema import (
    EmailSchema, 
    AttachmentSchema, 
    VariablesSchema, 
    RecipientSchema,
    AttachmentsSchema
)

@pydantic_input(AttachmentSchema, all_fields=True)
class AttachmentInput:
    pass

@pydantic_input(AttachmentsSchema, all_fields=True)
class AttachmentsInput:
    pass

@pydantic_input(RecipientSchema, all_fields=True)
class RecipientInput:
    pass


@pydantic_input(VariablesSchema, all_fields=True)
class VariablesInput:
    pass


@pydantic_input(EmailSchema, all_fields=True)
class EmailInput:
    pass
