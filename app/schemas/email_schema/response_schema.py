from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from app.core.constants import Status

class EmailResponseSchema(BaseModel):
    id_task: str
    status: Optional[Status] = Status.received
    created_at: datetime = Field(default=datetime.now())
    
    
    