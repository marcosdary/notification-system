from pydantic import Field
from typing import Optional

from app.schemas.file_schema.base_file_schema import BaseFileSchema
class FileReadSchema(BaseFileSchema):
    
    signed_url: Optional[str] = Field(alias="signedURL", default="oi")
    token: Optional[str] = None

    

