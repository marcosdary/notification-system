from pydantic import BaseModel
from typing import List

class FileUploadSchema(BaseModel):
    files: List[str]