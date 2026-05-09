from strawberry.experimental.pydantic import type as pydantic_type

from app.schemas.email_schema import EmailResponseSchema


@pydantic_type(EmailResponseSchema, all_fields=True)
class EmailResponseType:
    pass 
