from pydantic import BaseModel
from typing import Optional

class AttachmentSchema(BaseModel):
    path: Optional[str] = None
    content: Optional[str] = None
    filename: str