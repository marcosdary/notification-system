from pydantic import Field
from typing import Optional

from app.schemas.file_schema.base_file_schema import BaseFileSchema
class FileReadSchema(BaseFileSchema):
    
    signed_url: str = Field(alias="signedURL")
   
    error: Optional[str] = None

    

