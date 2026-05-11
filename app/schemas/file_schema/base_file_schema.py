from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, timedelta
from typing import Optional

from app.core.config import settings

class BaseFileSchema(BaseModel):
    expires_at: Optional[datetime] = Field(default=datetime.now() + timedelta(seconds=settings.EXPIRES_IN_FILE))
    path: str

    model_config = ConfigDict(from_attributes=True)

