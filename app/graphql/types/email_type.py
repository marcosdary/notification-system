from strawberry.experimental.pydantic import type as pydantic_type

from app.schemas.email_schema import ResponseSchema


@pydantic_type(ResponseSchema, all_fields=True)
class EmailResponseType:
    pass 
