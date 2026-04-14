from strawberry.experimental.pydantic import type as pydantic_type

from app.schemas import ApiErrorSchema

@pydantic_type(ApiErrorSchema, all_fields=True)
class ApiErrorType:
    pass