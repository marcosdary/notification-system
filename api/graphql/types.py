from strawberry.experimental.pydantic import type as pydantic_type
import strawberry
from typing import TypeVar, Generic

from api.schemas import (
    NotificationSchema,
    ApiErrorSchema
)

@pydantic_type(NotificationSchema)
class NotificationType:
    idSend: strawberry.auto
    typeSend: strawberry.auto
    templateName: strawberry.auto
    status: strawberry.auto
    createdAt: strawberry.auto
    endIn: strawberry.auto

D = TypeVar("D")
E = TypeVar("E")

@strawberry.type
class ApiResponseType(Generic[D, E]):
    success: bool
    data: D | None = None
    error: E | None = None

@pydantic_type(ApiErrorSchema, all_fields=True)
class ApiErrorType:
    pass