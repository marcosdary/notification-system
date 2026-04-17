from pydantic import BaseModel

class PaginationSchema(BaseModel):
    page: int | None = 1
    limit: int | None = 10
    all_: bool | None = False