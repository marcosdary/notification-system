from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FileUploadSchema(BaseModel):
    expires_at: datetime
    signed_url: str
    path: str
    error: Optional[str] = None



