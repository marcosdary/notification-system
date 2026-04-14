import strawberry
from typing import TypeVar, Generic


D = TypeVar("D")
E = TypeVar("E")

@strawberry.type
class ApiResponseType(Generic[D, E]):
    success: bool
    data: D | None = None
    error: E | None = None

