from strawberry.experimental.pydantic import input as pydantic_input

from app.schemas import DateRangeSchema

@pydantic_input(DateRangeSchema, all_fields=True)
class DateRangeInput:
    pass