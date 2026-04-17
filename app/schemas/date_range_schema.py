from pydantic import BaseModel
from datetime import datetime

class DateRangeSchema(BaseModel):
    startDate: datetime
    endDate: datetime
